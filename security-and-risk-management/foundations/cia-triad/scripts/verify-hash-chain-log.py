# Python 3.10, standard library only. Run: python3 verify-hash-chain-log.py
# Integrity example: a tamper-evident log built as a hash chain, and what an external anchor adds.
import hashlib
import json


def entry_hash(prev, record):
    return hashlib.sha256((prev + json.dumps(record, sort_keys=True)).encode()).hexdigest()


def build(records):
    chain, prev = [], "0" * 64
    for r in records:
        h = entry_hash(prev, r)
        chain.append({"record": r, "hash": h})
        prev = h
    return chain


def verify(chain, anchor=None):
    prev = "0" * 64
    for i, e in enumerate(chain):
        if entry_hash(prev, e["record"]) != e["hash"]:
            return f"BROKEN at entry {i}"
        prev = e["hash"]
    if anchor is not None and prev != anchor:
        return "chain is internally consistent but the head does not match the external anchor"
    return "ok"


records = [
    {"t": "09:00", "user": "alice", "action": "grant", "target": "bob", "role": "viewer"},
    {"t": "09:05", "user": "bob", "action": "read", "target": "payroll"},
    {"t": "09:10", "user": "alice", "action": "grant", "target": "carol", "role": "admin"},
    {"t": "09:20", "user": "carol", "action": "export", "target": "payroll"},
]
chain = build(records)
anchor = chain[-1]["hash"]          # published somewhere the log writer cannot edit (another account, a ticket, a signed email)
print("1 untouched          :", verify(chain, anchor))

# Attacker edits one entry in place
t1 = json.loads(json.dumps(chain))
t1[2]["record"]["role"] = "viewer"
print("2 edit one entry     :", verify(t1, anchor))

# Smarter attacker recomputes every hash after the edit, so the chain is internally consistent again
t2 = json.loads(json.dumps(chain))
t2[2]["record"]["role"] = "viewer"
prev = t2[1]["hash"]
for e in t2[2:]:
    e["hash"] = entry_hash(prev, e["record"])
    prev = e["hash"]
print("3 rewrite the chain  :", verify(t2), "(without an anchor)")
print("4 same, with anchor  :", verify(t2, anchor))
