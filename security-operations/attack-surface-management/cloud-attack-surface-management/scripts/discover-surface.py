# Python 3.10, standard library only.
# Run: python3 discover-surface.py
# Seed-based external discovery on a synthetic internet: DNS, certificates and open ports.
# Finds assets nobody registered, dangling DNS records (takeover risk) and exposed management services.
# All names use reserved domains (example.com, example.net, *.cloud.example) and TEST-NET addresses.
import ipaddress
from collections import deque
from datetime import date

TODAY = date(2026, 10, 27)
dns = {   # name -> (record type, value)
    "www.example.com":       ("A", "203.0.113.10"),
    "shop.example.com":      ("A", "203.0.113.11"),
    "api.example.com":       ("A", "198.51.100.20"),
    "old-demo.example.com":  ("CNAME", "demo-app-42.cloud.example"),      # target no longer claimed
    "staging.example.com":   ("A", "198.51.100.21"),
    "mail.example.com":      ("A", "203.0.113.12"),
}
claimed_cloud_names = {"shop-front.cloud.example", "api-gw.cloud.example"}  # resources that exist in some tenant
certs = {   # certificate subject alternative names and expiry, found by certificate transparency logs
    "cert-1": {"sans": {"www.example.com", "shop.example.com"}, "expires": date(2027, 3, 1)},
    "cert-2": {"sans": {"api.example.com", "internal-admin.example.com", "shop.example.com"}, "expires": date(2026, 9, 1)},
    "cert-3": {"sans": {"staging.example.com", "old-demo.example.com", "api.example.com"}, "expires": date(2027, 1, 15)},
}
open_ports = {"203.0.113.10": {443}, "203.0.113.11": {443}, "198.51.100.20": {443, 9200},
              "198.51.100.21": {443, 3389}, "203.0.113.12": {25, 443}}
inventory = {"www.example.com", "shop.example.com", "mail.example.com"}     # what the organization registered
MGMT = {22: "SSH", 3389: "RDP", 9200: "Elasticsearch API", 5984: "CouchDB API", 2375: "Docker API"}

seeds = ["www.example.com"]
owned_blocks = [ipaddress.ip_network("203.0.113.0/24")]   # an IP block registered to the organization (second seed type)
seen, queue = set(seeds), deque(seeds)
for name, (kind, value) in dns.items():                    # pivot 1: names that resolve into an owned block
    if kind == "A" and any(ipaddress.ip_address(value) in b for b in owned_blocks):
        seen.add(name); queue.append(name)
while queue:                                       # pivot 2: recursion through certificate co-occurrence
    name = queue.popleft()
    for cert in certs.values():
        if name in cert["sans"]:
            for other in cert["sans"] - seen:
                seen.add(other); queue.append(other)
print("discovered from the seeds:", sorted(seen))
print("candidate assets (not in inventory):", sorted(seen - inventory))

for name in sorted(seen):
    rec = dns.get(name)
    if rec is None:
        print(f"  {name:28} no public DNS record (internal name leaked through a certificate)")
        continue
    kind, value = rec
    if kind == "CNAME" and value not in claimed_cloud_names:
        print(f"  {name:28} DANGLING CNAME -> {value}: anyone who registers that name controls this host")
    if kind == "A":
        for port in sorted(open_ports.get(value, ())):
            if port in MGMT:
                print(f"  {name:28} exposes {MGMT[port]} on {value}:{port}")
for cid, c in certs.items():
    if c["expires"] < TODAY:
        print(f"  {cid} expired {c['expires']} for {sorted(c['sans'])}")
