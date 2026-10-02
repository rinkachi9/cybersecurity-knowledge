# Python 3.10, standard library only. Run: python3 correlate-incident-timeline.py
# Medium case: ransomware with data theft on a file server. Merge three log sources whose clocks disagree,
# then compute the elapsed-time measures that SP 800-61 Rev. 2 lists under "Time Per Incident".
from datetime import datetime, timedelta

FMT = "%H:%M:%S"
t = lambda s: datetime.strptime(s, FMT)

# Each source reports local time and has a known clock offset from true UTC (found by comparing with NTP-synced hosts).
SOURCES = {
    "vpn":  {"offset": timedelta(seconds=0),    "events": [("22:41:10", "login ok user=svc-backup from 198.51.100.23"),
                                                           ("22:41:55", "session assigned 10.0.4.17")]},
    "fs01": {"offset": timedelta(minutes=-6),   "events": [("22:50:03", "smb: user svc-backup copied 18 GB to 203.0.113.80"),
                                                           ("23:11:50", "mass rename *.docx -> *.locked begins"),
                                                           ("23:27:30", "host isolated from network (analyst action)")]},
    "edr":  {"offset": timedelta(minutes=+2),   "events": [("23:20:30", "alert: ransomware behavior on fs01"),
                                                           ("23:24:00", "incident declared by analyst"),
                                                           ("23:31:45", "svc-backup disabled, sessions revoked")]},
}


def normalized():
    rows = []
    for name, src in SOURCES.items():
        for local, text in src["events"]:
            rows.append((t(local) - src["offset"], name, text))   # true time = reported time minus the clock's offset
    return sorted(rows)


rows = normalized()
print("timeline (corrected to true time):")
for ts, src, text in rows:
    print(f"  {ts.strftime(FMT)}  {src:4s} {text}")

get = lambda needle: next(ts for ts, _, text in rows if needle in text)
initial = get("login ok")
exfil = get("copied 18 GB")
impact = get("mass rename")
detected = get("alert: ransomware")
declared = get("incident declared")
contained_host = get("host isolated")
contained_identity = get("svc-backup disabled")

mins = lambda a, b: round((b - a).total_seconds() / 60, 1)
print("\nelapsed time (minutes):")
print("  initial access -> exfiltration started :", mins(initial, exfil))
print("  initial access -> detection            :", mins(initial, detected), "(attacker dwell before any alert)")
print("  detection -> declaration               :", mins(detected, declared))
print("  detection -> host contained            :", mins(detected, contained_host))
print("  detection -> identity contained        :", mins(detected, contained_identity))

# What the uncorrected clocks would have told us about the two containment actions
host_local, ident_local = t("23:27:30"), t("23:31:45")           # as printed in the fs01 and edr logs
print("\nwithout clock correction: host isolated %s, identity revoked %s -> '%s first'" % (
    host_local.strftime(FMT), ident_local.strftime(FMT), "host" if host_local < ident_local else "identity"))
print("with clock correction   : host isolated %s, identity revoked %s -> '%s first'" % (
    contained_host.strftime(FMT), contained_identity.strftime(FMT), "host" if contained_host < contained_identity else "identity"))
