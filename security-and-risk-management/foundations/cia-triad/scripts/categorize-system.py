# Python 3.10, standard library only. Run: python3 categorize-system.py
# FIPS 199 style categorization: impact per information type and security objective, high-water mark per
# objective for the system, then the baseline impact level (SP 800-53B). Impact values are examples.
LEVEL = {"NA": 0, "LOW": 1, "MODERATE": 2, "HIGH": 3}
NAME = {v: k for k, v in LEVEL.items()}

info_types = {   # (confidentiality, integrity, availability)
    "press releases":            ("NA",       "MODERATE", "LOW"),
    "employee payroll records":  ("MODERATE", "MODERATE", "LOW"),
    "customer card tokens":      ("HIGH",     "MODERATE", "MODERATE"),
    "infusion pump dose limits": ("LOW",      "HIGH",     "HIGH"),
}


def system_category(types):
    result = {}
    for idx, objective in enumerate(("confidentiality", "integrity", "availability")):
        level = max(LEVEL[v[idx]] for v in types.values())
        if objective != "confidentiality" and level == 0:
            raise ValueError("NA is only allowed for confidentiality")      # FIPS 199 rule
        result[objective] = NAME[level]
    return result


def impact_level(sc):
    """Low-impact: all low. Moderate: at least one moderate, none high. High: at least one high (SP 800-53B)."""
    vals = [LEVEL[v] for v in sc.values()]
    return "HIGH" if max(vals) == 3 else "MODERATE" if max(vals) == 2 else "LOW"


for name, v in info_types.items():
    print(f"{name:28s} C={v[0]:9s} I={v[1]:9s} A={v[2]}")
for subset in (["press releases"], ["press releases", "employee payroll records"], list(info_types)):
    sc = system_category({k: info_types[k] for k in subset})
    print(f"\nsystem holding {subset}")
    print("  SC =", sc, "-> baseline impact level:", impact_level(sc))
