# Python 3.10, standard library only, needs network access. Run: python3 tailor-baseline.py
# Shows tailoring as data: start from the moderate baseline (SP 800-53B via NIST OSCAL, release 5.2.0),
# designate controls as inherited, add controls, set parameter values, then summarize the result.
# The scenario is synthetic: a SaaS payroll portal for example.com on a public cloud.
import json
import urllib.request
from collections import Counter

URL = ("https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/"
       "NIST_SP-800-53_rev5_MODERATE-baseline-resolved-profile_catalog.json")


def ids(catalog):
    out = set()

    def walk(node):
        for c in node.get("controls", []):
            out.add(c["id"]); walk(c)

    for g in catalog["groups"]:
        walk(g)
    return out


with urllib.request.urlopen(URL, timeout=60) as r:
    baseline = ids(json.load(r)["catalog"])
print("moderate baseline:", len(baseline), "controls and enhancements")

# 1. Designation: who implements each control (task S-3 in the RMF)
designation = {}
for cid in sorted(baseline):
    family = cid.split("-")[0]
    if family == "pe":                                   # physical protection of the data centers
        designation[cid] = "inherited (cloud provider authorization)"
    elif cid.split(".")[0] in ("ac-2", "ia-2"):          # accounts: we approve, the identity service provisions
        designation[cid] = "hybrid"
    else:
        designation[cid] = "system-specific"

# 2. Tailoring decisions, each with a reason (task S-2 and S-4)
added = {
    "sc-24": "fail in a known state: payroll approval must not fail open (threat model T-7)",
    "sc-7.18": "fail secure on boundary protection devices (threat model T-7)",
    "si-2.7": "root cause analysis of flaws (new in release 5.2.0, not in any baseline)",
}
for cid, why in added.items():
    designation[cid] = "system-specific (added)"
print("added by tailoring:", ", ".join(added))

# 3. Parameter values: an unset organization-defined parameter makes a control untestable
parameters = {
    "ac-2.3": {"ac-02.03_odp.01": "24 hours", "ac-02.03_odp.02": "45 days"},
}

count = Counter(designation.values())
print("\nresult:")
for kind, n in sorted(count.items(), key=lambda kv: -kv[1]):
    print(f"  {kind:42s} {n:4d}")
print("  total in the system security plan scope    ", sum(count.values()))
print("\nparameter values recorded:", json.dumps(parameters))
print("check: every added control is outside the moderate baseline ->", all(c not in baseline for c in added))
