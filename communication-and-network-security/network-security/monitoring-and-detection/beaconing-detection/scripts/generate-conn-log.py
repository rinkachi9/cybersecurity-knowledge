# Python 3.10, standard library only. Run: python3 generate-conn-log.py conn.tsv
# Writes 24 hours of synthetic connection records (a small subset of Zeek conn.log fields)
# for three hosts. It contains human browsing, a software updater that polls on a fixed
# schedule, and an implant that beacons every 300 s with 20 % jitter. The fixed seed makes
# the output reproducible. Addresses are documentation ranges (RFC 5737).
import random
import sys

random.seed(7)
START, DAY = 1_790_000_000.0, 86_400
rows = []

# Human browsing: bursts of activity during working hours, irregular gaps, varied sizes
sites = ["198.51.100.10", "198.51.100.11", "198.51.100.12", "198.51.100.13"]
t = START + 8 * 3600
while t < START + 18 * 3600:
    for _ in range(random.randint(3, 15)):
        rows.append((t, "192.0.2.21", random.choice(sites), 443, random.randint(800, 4000), random.randint(5_000, 900_000)))
        t += random.uniform(0.2, 20)
    t += random.expovariate(1 / 600)

# Updater: checks every 3600 s exactly, identical small requests, larger reply when an update exists
for i in range(24):
    rows.append((START + i * 3600 + random.uniform(0, 0.5), "192.0.2.22", "198.51.100.40", 443, 620, 1_450 if i != 9 else 2_400_000))

# Implant: sleep 300 s with +/- 20 % jitter, small fixed-size check-ins, all day long
t = START
while t < START + DAY:
    rows.append((t, "192.0.2.23", "203.0.113.80", 443, random.randint(300, 330), random.randint(200, 260)))
    t += 300 * random.uniform(0.8, 1.2)

rows.sort()
out = sys.argv[1] if len(sys.argv) > 1 else "conn.tsv"
with open(out, "w") as f:
    f.write("#fields\tts\tid.orig_h\tid.resp_h\tid.resp_p\torig_bytes\tresp_bytes\n")
    for r in rows:
        f.write(f"{r[0]:.6f}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[4]}\t{r[5]}\n")
print(f"wrote {len(rows)} connections to {out}")
