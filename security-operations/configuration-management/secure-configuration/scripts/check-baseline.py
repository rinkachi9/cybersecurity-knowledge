# Python 3.10, standard library only.
# Run: python3 check-baseline.py
# A miniature secure-configuration checker: a baseline (rules as data), an audit of two synthetic hosts,
# exceptions with an expiry date, and drift detection by hashing the effective configuration.
# Rule ids are local (SYN-...) and do not copy any published benchmark.
import hashlib
import json
from datetime import date

TODAY = date(2026, 10, 27)

RULES = [  # id, setting, expected, why
    ("SYN-SSH-01", "sshd.PermitRootLogin", "no", "no direct root login, actions stay attributable"),
    ("SYN-SSH-02", "sshd.PasswordAuthentication", "no", "keys only, removes password guessing"),
    ("SYN-SSH-03", "sshd.X11Forwarding", "no", "unused feature, least functionality"),
    ("SYN-KRN-01", "sysctl.kernel.randomize_va_space", "2", "full address space randomization"),
    ("SYN-NET-01", "sysctl.net.ipv4.ip_forward", "0", "host is not a router"),
    ("SYN-FS-01", "file./etc/shadow.mode", "0640", "password hashes readable by root and shadow group only"),
]

hosts = {
    "web-01": {"sshd.PermitRootLogin": "no", "sshd.PasswordAuthentication": "no", "sshd.X11Forwarding": "no",
               "sysctl.kernel.randomize_va_space": "2", "sysctl.net.ipv4.ip_forward": "0", "file./etc/shadow.mode": "0640"},
    "build-02": {"sshd.PermitRootLogin": "yes", "sshd.PasswordAuthentication": "yes", "sshd.X11Forwarding": "no",
                 "sysctl.kernel.randomize_va_space": "2", "sysctl.net.ipv4.ip_forward": "1", "file./etc/shadow.mode": "0644"},
}
# an exception: build-02 needs IP forwarding for a container network until a redesign, approved with an expiry
exceptions = {("build-02", "SYN-NET-01"): date(2026, 12, 31), ("build-02", "SYN-SSH-01"): date(2026, 9, 30)}

def audit(host, cfg):
    rows = []
    for rid, key, expected, why in RULES:
        actual = cfg.get(key, "<unset>")
        if actual == expected:
            rows.append((rid, "pass", ""))
            continue
        exp = exceptions.get((host, rid))
        if exp and exp >= TODAY:
            rows.append((rid, "excepted", f"until {exp}"))
        elif exp:
            rows.append((rid, "FAIL", f"exception expired {exp}; want {expected}, have {actual}"))
        else:
            rows.append((rid, "FAIL", f"want {expected}, have {actual}"))
    return rows

for host, cfg in hosts.items():
    rows = audit(host, cfg)
    score = sum(r[1] in ("pass", "excepted") for r in rows)
    print(f"{host}: {score}/{len(rows)} compliant")
    for rid, status, note in rows:
        if status != "pass":
            print(f"   {rid} {status} {note}")

# drift: hash of the effective configuration, compared with the hash recorded when the host was approved
def fingerprint(cfg): return hashlib.sha256(json.dumps(cfg, sort_keys=True).encode()).hexdigest()[:12]
approved = {h: fingerprint(c) for h, c in hosts.items()}
hosts["web-01"]["sshd.X11Forwarding"] = "yes"     # an unrecorded change made by hand
print("drift:", {h: ("DRIFTED" if fingerprint(c) != approved[h] else "same as approved") for h, c in hosts.items()})
