# Python 3.10, standard library only. Run: python3 generate-dns-log.py dns.tsv
# Writes one hour of synthetic resolver query logs (timestamp, client, query name, query type).
# It mixes ordinary lookups, a CDN and an anti-virus reputation service that both use long
# machine-generated labels (legitimate traffic that looks suspicious), and a tunnel that
# moves a 40 KB file out in base32-encoded labels. Domains use example.com/net/org and the
# reserved .example top-level domain (RFC 2606). The fixed seed makes the output reproducible.
import base64
import random
import sys

random.seed(11)
START = 1_790_000_000.0
rows = []

popular = ["www.example.com", "mail.example.com", "api.example.net", "static.example.net",
           "login.example.org", "news.example.com", "docs.example.org", "chat.example.net"]
for _ in range(3000):
    rows.append((START + random.uniform(0, 3600), f"192.0.2.{random.randint(20, 80)}",
                 random.choice(popular), random.choice(["A", "A", "A", "AAAA", "HTTPS"])))

# CDN: one hashed hostname per object, but a small set of them reused many times
cdn_names = [f"{random.randbytes(8).hex()}.edge.cdnprovider.example" for _ in range(40)]
for _ in range(600):
    rows.append((START + random.uniform(0, 3600), f"192.0.2.{random.randint(20, 80)}", random.choice(cdn_names), "A"))

# Reputation lookups: an anti-virus product asks about file hashes in DNS, unique every time
for _ in range(150):
    rows.append((START + random.uniform(0, 3600), f"192.0.2.{random.randint(20, 80)}",
                 f"{random.randbytes(16).hex()}.avqs.avvendor.example", "TXT"))

# Tunnel: 40 KB of data, 30 bytes per query encoded in base32 (48 characters), sequence number first
secret = random.randbytes(40_000)
t = START + 1200
for seq, i in enumerate(range(0, len(secret), 30)):
    label = base64.b32encode(secret[i:i + 30]).decode().rstrip("=").lower()
    rows.append((t, "192.0.2.99", f"{seq:05x}.{label}.t.exfil-lab.example", random.choice(["TXT", "NULL", "CNAME"])))
    t += random.uniform(0.05, 0.4)

rows.sort()
out = sys.argv[1] if len(sys.argv) > 1 else "dns.tsv"
with open(out, "w") as f:
    f.write("#fields\tts\tclient\tquery\tqtype\n")
    for r in rows:
        f.write(f"{r[0]:.6f}\t{r[1]}\t{r[2]}\t{r[3]}\n")
print(f"wrote {len(rows)} queries to {out}")
