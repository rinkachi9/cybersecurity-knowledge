# Python 3.10, standard library only.
# Run: python3 reconcile-inventory.py
# Reconciles asset records from several discovery sources and reports the classic inventory problems:
# shadow assets, ghost records, assets without an owner, assets without endpoint coverage, end-of-life software.
# All hostnames use the reserved example.com domain and all data is synthetic.
from datetime import date

TODAY = date(2026, 10, 27)

cmdb = {   # the system of record: name -> attributes
    "web-01.example.com":  {"owner": "shop-team", "criticality": "high", "os": "Ubuntu 22.04"},
    "db-01.example.com":   {"owner": "shop-team", "criticality": "high", "os": "Ubuntu 22.04"},
    "old-ftp.example.com": {"owner": "",          "criticality": "low",  "os": "CentOS 7"},
    "hr-app.example.com":  {"owner": "hr-it",     "criticality": "med",  "os": "Windows Server 2019"},
}
cloud_api = {"web-01.example.com", "db-01.example.com", "ci-runner-9.example.com"}
scanner   = {"web-01.example.com", "db-01.example.com", "ci-runner-9.example.com", "hr-app.example.com", "print-3.example.com"}
edr       = {"web-01.example.com", "hr-app.example.com"}
last_seen = {"old-ftp.example.com": date(2026, 6, 2), "web-01.example.com": date(2026, 10, 27),
             "db-01.example.com": date(2026, 10, 27), "hr-app.example.com": date(2026, 10, 26)}
EOL = {"CentOS 7": date(2024, 6, 30)}          # end of maintenance dates are examples, check your vendor's calendar

discovered = cloud_api | scanner | edr
print("sources: cmdb", len(cmdb), "| cloud", len(cloud_api), "| scanner", len(scanner), "| edr", len(edr))
print("shadow assets (discovered, not in CMDB):", sorted(discovered - set(cmdb)))
ghosts = sorted(n for n in cmdb if n not in discovered or (TODAY - last_seen.get(n, TODAY)).days > 30)
print("ghost records (in CMDB, not seen for 30+ days or by any source):", ghosts)
print("assets without owner:", sorted(n for n, a in cmdb.items() if not a["owner"]))
print("critical or medium assets without EDR:", sorted(n for n, a in cmdb.items() if a["criticality"] in ("high", "med") and n not in edr))
print("end-of-life software:", sorted((n, a["os"]) for n, a in cmdb.items() if a["os"] in EOL and EOL[a["os"]] < TODAY))
coverage = len(set(cmdb) & scanner) / len(cmdb)
print(f"scanner coverage of CMDB assets: {coverage:.0%}; of all discovered assets: {len(discovered & scanner) / len(discovered):.0%}")
