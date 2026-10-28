# Python 3.10, standard library only.
# Run: python3 vector-exposure.py
# Groups a synthetic findings list by delivery vector and by the CVSS 3.1 Attack Vector (AV) metric, and ranks
# the entry points an outsider can use without any foothold. CVSS weights are from the FIRST CVSS v3.1 specification.
from collections import Counter, defaultdict

AV_WEIGHT = {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.2}
AV_NAME = {"N": "Network", "A": "Adjacent", "L": "Local", "P": "Physical"}

# (finding id, asset, CVSS 3.1 vector, entry path the finding belongs to). All entries are synthetic.
findings = [
    ("F-1", "vpn-gw-1",     "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", "external remote service"),
    ("F-2", "web-shop",     "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N", "public-facing application"),
    ("F-3", "web-shop",     "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N", "public-facing application"),
    ("F-4", "mail-client",  "CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H", "phishing attachment"),
    ("F-5", "file-server",  "CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N", "internal network"),
    ("F-6", "kiosk-pc",     "CVSS:3.1/AV:P/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", "physical access"),
    ("F-7", "build-runner", "CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H", "supply chain / CI"),
]

def parse(vector):
    return dict(part.split(":") for part in vector.split("/")[1:])

by_av = defaultdict(list)
for fid, asset, vec, path in findings:
    by_av[parse(vec)["AV"]].append(fid)
print("by CVSS Attack Vector metric:")
for av in "NALP":
    print(f"  {AV_NAME[av]:9} weight {AV_WEIGHT[av]:.2f} -> {by_av.get(av, [])}")

# Outsider-first view: network reachable and no privileges required means no foothold is needed.
outsider = [f for f in findings if parse(f[2])["AV"] == "N" and parse(f[2])["PR"] == "N"]
print("usable without any foothold (AV:N and PR:N):", [f[0] for f in outsider])

paths = Counter(path for _, _, _, path in findings)
print("findings per entry path:", dict(paths))
print("assets reachable by an outsider:", sorted({f[1] for f in outsider}))
