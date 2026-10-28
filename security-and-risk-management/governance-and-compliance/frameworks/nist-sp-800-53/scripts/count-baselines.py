# Python 3.10, standard library only, needs network access. Run: python3 count-baselines.py
# Counts SP 800-53 Rev. 5.2.0 controls per family and baseline from NIST OSCAL content.
import json
import urllib.request
from collections import Counter

BASE = ("https://raw.githubusercontent.com/usnistgov/oscal-content/main/"
        "nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_{}-baseline-resolved-profile_catalog.json")


def load(name):
    with urllib.request.urlopen(BASE.format(name), timeout=60) as r:
        return json.load(r)["catalog"]


def ids(catalog):
    out = set()

    def walk(node):
        for c in node.get("controls", []):
            out.add(c["id"])
            walk(c)

    for g in catalog["groups"]:
        walk(g)
    return out


baselines = {n: ids(load(n)) for n in ("LOW", "MODERATE", "HIGH", "PRIVACY")}
for n, s in baselines.items():
    print(f"{n:9s} total={len(s):4d}")

fam = lambda cid: cid.split("-")[0].upper()
print("\nfamily  low  mod  high  priv")
rows = {n: Counter(fam(c) for c in s) for n, s in baselines.items()}
for f in sorted(set().union(*[set(r) for r in rows.values()])):
    print(f"{f:6s} {rows['LOW'][f]:4d} {rows['MODERATE'][f]:4d} {rows['HIGH'][f]:5d} {rows['PRIVACY'][f]:5d}")

print("\nnested check, low in moderate:", baselines["LOW"] <= baselines["MODERATE"],
      "| moderate in high:", baselines["MODERATE"] <= baselines["HIGH"])
only_high = sorted(baselines["HIGH"] - baselines["MODERATE"])
print("high-only controls in SC family:", [c for c in only_high if c.startswith("sc-")][:12])
