# Python 3.10, standard library only, needs network access.
# Run: python3 render-control.py ac-6      (any base control id, lower case, for example sc-7, ia-2, si-4)
# Prints a control statement with its organization-defined parameters and its enhancements with baseline membership.
import json
import re
import sys
import urllib.request

ROOT = "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/"
CATALOG = ROOT + "NIST_SP-800-53_rev5_catalog.json"
BASELINE = ROOT + "NIST_SP-800-53_rev5_{}-baseline-resolved-profile_catalog.json"


def fetch(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)["catalog"]


def ids(catalog):
    out = set()

    def walk(node):
        for c in node.get("controls", []):
            out.add(c["id"]); walk(c)

    for g in catalog["groups"]:
        walk(g)
    return out


def find(catalog, cid):
    def walk(node):
        for c in node.get("controls", []):
            if c["id"] == cid:
                return c
            hit = walk(c)
            if hit:
                return hit

    for g in catalog["groups"]:
        hit = walk(g)
        if hit:
            return hit


def label(c):
    for p in c.get("props", []):
        if p["name"] == "label":
            return re.sub(r"\(0+(\d)\)", r"(\1)", re.sub(r"-0+(\d)", r"-\1", p["value"]))
    return c["id"].upper()


def statement(c):
    def prose(p, depth=0):
        lab = next((q["value"] for q in p.get("props", []) if q["name"] == "label"), "")
        lines = [("  " * depth + lab + " " + re.sub(r"\s+", " ", p["prose"])).rstrip()] if p.get("prose") else []
        for q in p.get("parts", []):
            lines += prose(q, depth + 1)
        return lines

    for part in c["parts"]:
        if part["name"] == "statement":
            return prose(part)
    return []


cid = sys.argv[1].lower()
cat = fetch(CATALOG)
base = {n: ids(fetch(BASELINE.format(n))) for n in ("LOW", "MODERATE", "HIGH", "PRIVACY")}
member = lambda i: "".join(ch if i in base[n] else "-" for ch, n in zip("LMHP", base))

c = find(cat, cid)
print(f"{label(c)}  {c['title']}   baselines [{member(cid)}] (L=low M=moderate H=high P=privacy)")
for line in statement(c):
    print("  ", re.sub(r"\{\{ insert: param, ([^}]+) \}\}", lambda m: "[" + m.group(1).split(", ")[-1] + "]", line))
params = c.get("params", [])
print(f"\norganization-defined parameters on the base control: {len(params)}")
print("\nenhancements:")
for e in c.get("controls", []):
    if any(p["name"] == "status" and p.get("value") == "withdrawn" for p in e.get("props", [])):
        continue
    print(f"  {label(e):9s} {e['title'][:60]:60s} [{member(e['id'])}]")
