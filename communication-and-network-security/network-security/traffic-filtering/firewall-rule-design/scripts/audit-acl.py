# Python 3.10, standard library only. Run: python3 audit-acl.py sample-acl.csv
# Audits a first-match access control list for the anomalies classified by Al-Shaer and Hamed
# (shadowing, redundancy, generalization, correlation) and for overly broad rules. A rule is shadowed when an
# earlier rule matches every packet it would match: it can never fire. If the earlier rule has
# the opposite action, the policy does not do what its author meant.
import csv
import ipaddress
import sys

RISKY_PORTS = {22: "SSH", 23: "Telnet", 445: "SMB", 3389: "RDP", 5985: "WinRM", 1433: "MSSQL"}


class Rule:
    def __init__(self, row):
        self.id, self.action, src, dst, self.proto, port = (x.strip() for x in row)
        self.src = ipaddress.ip_network("0.0.0.0/0" if src == "any" else src)
        self.dst = ipaddress.ip_network("0.0.0.0/0" if dst == "any" else dst)
        if port == "any":
            self.ports = (0, 65535)
        elif "-" in port:
            lo, hi = port.split("-")
            self.ports = (int(lo), int(hi))
        else:
            self.ports = (int(port), int(port))

    def covers(self, other):
        # True when every packet matched by "other" is also matched by self
        return (self.src.supernet_of(other.src) and self.dst.supernet_of(other.dst)
                and self.proto in ("any", other.proto)
                and self.ports[0] <= other.ports[0] and other.ports[1] <= self.ports[1])

    def overlaps(self, other):
        return (self.src.overlaps(other.src) and self.dst.overlaps(other.dst)
                and (self.proto == "any" or other.proto == "any" or self.proto == other.proto)
                and self.ports[0] <= other.ports[1] and other.ports[0] <= self.ports[1])

    def __str__(self):
        p = "any" if self.ports == (0, 65535) else f"{self.ports[0]}" if self.ports[0] == self.ports[1] else f"{self.ports[0]}-{self.ports[1]}"
        return f"rule {self.id} ({self.action} {self.src} -> {self.dst} {self.proto}/{p})"


with open(sys.argv[1]) as f:
    rules = [Rule(r) for r in csv.reader(line for line in f if not line.startswith("#"))]

findings = 0
for i, r in enumerate(rules):
    for earlier in rules[:i]:
        if earlier.covers(r):
            kind = "REDUNDANT" if earlier.action == r.action else "SHADOWED"
            print(f"{kind:<11} {r} never matches, {earlier} catches all of its traffic first")
            findings += 1
            break
        if earlier.overlaps(r) and earlier.action != r.action:
            catch_all = r.src.prefixlen == 0 and r.dst.prefixlen == 0
            if not r.covers(earlier):
                print(f"CORRELATED  {r} partly overlaps {earlier} with the opposite action, order decides the outcome")
                findings += 1
            elif not catch_all:
                # Usually intended (an exception before a general rule), but worth confirming
                print(f"GENERALIZES {r} is a wider version of {earlier} with the opposite action (check intent)")
                findings += 1
    wide_ports = r.ports[1] - r.ports[0] > 1000
    any_source = r.src.prefixlen == 0
    if r.action == "allow" and any_source and wide_ports:
        print(f"TOO BROAD   {r} allows a large port range from any source")
        findings += 1
    for port, name in RISKY_PORTS.items():
        if r.action == "allow" and any_source and r.ports[0] <= port <= r.ports[1] and r.ports[1] - r.ports[0] < 1000:
            print(f"EXPOSED     {r} opens {name} ({port}) to any source")
            findings += 1
print(f"\n{len(rules)} rules, {findings} findings")
