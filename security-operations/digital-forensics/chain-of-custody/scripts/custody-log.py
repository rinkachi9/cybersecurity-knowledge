# Python 3.10, standard library only.
# Run: python3 custody-log.py
# Builds a hash-chained chain of custody log for one evidence item, then verifies it and shows
# what each kind of tampering or process error looks like. All data is synthetic.
import hashlib
import json
import tempfile
from pathlib import Path

GENESIS = "0" * 64


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def entry_hash(prev, record):
    return hashlib.sha256((prev + json.dumps(record, sort_keys=True)).encode()).hexdigest()


def append(log, record):
    prev = log[-1]["hash"] if log else GENESIS
    log.append({"record": record, "hash": entry_hash(prev, record)})


def verify(log, evidence_path, expected_sha256):
    """Return a list of findings. An empty list means the log and the evidence are consistent."""
    findings, prev, holder, last_t = [], GENESIS, None, ""
    for i, e in enumerate(log):
        r = e["record"]
        if entry_hash(prev, r) != e["hash"]:
            findings.append(f"entry {i}: hash chain broken (record edited, removed or reordered)")
        prev = e["hash"]
        if r["time"] < last_t:  # ISO 8601 UTC strings sort in time order
            findings.append(f"entry {i}: time goes backwards")
        last_t = r["time"]
        if r["action"] == "transfer":
            if holder is not None and r["from"] != holder:
                findings.append(f"entry {i}: transfer from {r['from']} but {holder} held the item")
            holder = r["to"]
        elif holder is not None and r["by"] != holder:
            findings.append(f"entry {i}: {r['by']} acted on the item while {holder} held it")
        elif holder is None and r["action"] == "collect":
            holder = r["by"]
    if sha256_file(evidence_path) != expected_sha256:
        findings.append("evidence file hash does not match the hash recorded at collection")
    return findings


with tempfile.TemporaryDirectory() as d:
    item = Path(d) / "disk01.dd"
    item.write_bytes(b"synthetic disk image\n" * 1000)
    acquired = sha256_file(item)

    log = []
    append(log, {"time": "2026-10-27T09:12:00Z", "action": "collect", "by": "alice",
                 "item": "EV-001", "where": "server room rack 4", "sha256": acquired})
    append(log, {"time": "2026-10-27T09:40:00Z", "action": "transfer", "from": "alice", "to": "bob",
                 "item": "EV-001", "how": "hand to hand, sealed bag 0042"})
    append(log, {"time": "2026-10-27T10:05:00Z", "action": "verify-hash", "by": "bob",
                 "item": "EV-001", "sha256": sha256_file(item)})
    append(log, {"time": "2026-10-27T10:30:00Z", "action": "store", "by": "bob",
                 "item": "EV-001", "where": "evidence locker 2"})
    anchor = log[-1]["hash"]  # copy this value somewhere the log writer cannot edit

    print("1 untouched                :", verify(log, item, acquired) or "ok")

    forged = json.loads(json.dumps(log))
    forged[1]["record"]["to"] = "mallory"
    print("2 edited receiver          :", verify(forged, item, acquired))

    gap = json.loads(json.dumps(log))
    del gap[1]  # the transfer is missing: bob appears to act on an item held by alice
    print("3 missing transfer         :", verify(gap, item, acquired))

    # An attacker who recomputes the whole chain after editing passes step 2 but not the anchor check.
    rebuilt = []
    for e in forged:
        append(rebuilt, e["record"])
    print("4 chain rebuilt, no anchor :", verify(rebuilt, item, acquired) or "ok")
    print("4 chain rebuilt, anchor    :", "head matches anchor" if rebuilt[-1]["hash"] == anchor
          else "head differs from the anchor")

    item.write_bytes(item.read_bytes() + b"x")  # evidence modified after collection
    print("5 evidence file changed    :", verify(log, item, acquired))
