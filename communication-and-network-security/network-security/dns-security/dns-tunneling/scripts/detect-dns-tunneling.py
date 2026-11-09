# Python 3.10, standard library only. Run: python3 detect-dns-tunneling.py dns.tsv
# Groups resolver logs by parent domain and measures how much information clients push into
# query names. A tunnel has to encode its data in the labels, so it produces many unique,
# long, high-entropy names under one domain. Legitimate services with hashed names exist,
# so the output is a ranked list for an analyst, not a verdict.
import collections
import math
import sys


def parent_domain(name):
    # Simplification: last two labels. Real code must use the Public Suffix List
    # (example.co.uk has three labels in its registrable domain).
    return ".".join(name.split(".")[-2:])


def entropy(s):
    counts = collections.Counter(s)
    return -sum(c / len(s) * math.log2(c / len(s)) for c in counts.values()) if s else 0.0


stats = collections.defaultdict(lambda: {"queries": 0, "names": set(), "clients": set(), "qtypes": collections.Counter()})
with open(sys.argv[1]) as f:
    for line in f:
        if line.startswith("#"):
            continue
        _, client, qname, qtype = line.rstrip("\n").split("\t")
        s = stats[parent_domain(qname)]
        s["queries"] += 1
        s["names"].add(qname)
        s["clients"].add(client)
        s["qtypes"][qtype] += 1

print(f"{'domain':<20} {'queries':>7} {'unique':>6} {'clients':>7} {'sub len':>7} {'entropy':>7} {'bytes in names':>14}  qtypes")
rows = []
for dom, s in stats.items():
    subs = [n[: -len(dom) - 1] for n in s["names"] if n != dom]
    if not subs:
        continue
    avg_len = sum(map(len, subs)) / len(subs)
    avg_ent = sum(entropy(x.replace(".", "")) for x in subs) / len(subs)
    # Unique subdomain characters approximate how much data could have left through this domain
    payload = sum(len(x) for x in subs)
    rows.append((payload, dom, s, len(subs), avg_len, avg_ent))

for payload, dom, s, uniq, avg_len, avg_ent in sorted(rows, key=lambda r: r[0], reverse=True):
    suspicious = uniq > 500 and avg_len > 30 and avg_ent > 3.5
    qt = ", ".join(f"{k} {v}" for k, v in s["qtypes"].most_common(3))
    print(f"{dom:<20} {s['queries']:>7} {uniq:>6} {len(s['clients']):>7} {avg_len:>7.1f} {avg_ent:>7.2f} {payload:>14}  {qt}"
          + ("  <- review" if suspicious else ""))
