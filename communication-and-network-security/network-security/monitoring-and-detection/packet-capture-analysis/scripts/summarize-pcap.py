# Python 3.10, standard library only. Run: python3 summarize-pcap.py capture.pcap
# First-pass triage of a classic pcap file (Ethernet, IPv4): protocol mix, top talkers,
# TCP conversations with their handshake state, DNS query names and hosts that look like
# they are scanning. It reads the file itself instead of calling tshark, so every step of
# the parsing is visible. pcapng files must be converted first (editcap -F pcap in.pcapng out.pcap).
import collections
import math
import struct
import sys

FIN, SYN, RST, PSH, ACK = 0x01, 0x02, 0x04, 0x08, 0x10


def read_pcap(path):
    with open(path, "rb") as f:
        magic = f.read(4)
        # The magic number tells byte order and timestamp resolution (micro or nano seconds)
        endian = {b"\xd4\xc3\xb2\xa1": "<", b"\xa1\xb2\xc3\xd4": ">",
                  b"\x4d\x3c\xb2\xa1": "<", b"\xa1\xb2\x3c\x4d": ">"}.get(magic)
        if endian is None:
            sys.exit("not a classic pcap file (pcapng is not supported)")
        _, _, _, _, _, linktype = struct.unpack(endian + "HHiIII", f.read(20))
        if linktype != 1:
            sys.exit(f"link type {linktype} is not Ethernet")
        while hdr := f.read(16):
            sec, frac, incl, _ = struct.unpack(endian + "IIII", hdr)
            yield sec + frac / 1e6, f.read(incl)


def ip_str(b):
    return ".".join(str(x) for x in b)


def qname(payload):
    labels, i = [], 12
    while i < len(payload) and payload[i]:
        n = payload[i]
        labels.append(payload[i + 1:i + 1 + n].decode(errors="replace"))
        i += 1 + n
    return ".".join(labels)


def entropy(s):
    counts = collections.Counter(s)
    return -sum(c / len(s) * math.log2(c / len(s)) for c in counts.values()) if s else 0.0


protos, talkers, dns_names = collections.Counter(), collections.Counter(), []
convs = {}
syn_targets = collections.defaultdict(set)
first = last = None
frames = 0

for ts, frame in read_pcap(sys.argv[1]):
    frames += 1
    first, last = first or ts, ts
    if len(frame) < 34 or frame[12:14] != b"\x08\x00":
        protos["non-IPv4"] += 1
        continue
    ip = frame[14:]
    ihl = (ip[0] & 0x0F) * 4
    proto, src, dst = ip[9], ip_str(ip[12:16]), ip_str(ip[16:20])
    talkers[src] += len(frame)
    l4 = ip[ihl:]
    if proto == 6:
        sport, dport, _, _, off, flags = struct.unpack("!HHIIBB", l4[:14])
        protos["TCP"] += 1
        key = tuple(sorted([(src, sport), (dst, dport)]))
        c = convs.setdefault(key, {"client": None, "flags": set(), "bytes": 0, "data": b""})
        c["bytes"] += len(frame)
        if flags & SYN and not flags & ACK:
            c["client"] = c["client"] or (src, sport)
            syn_targets[src].add((dst, dport))
        c["flags"].add(flags)
        payload = l4[(off >> 4) * 4:]
        if payload and not c["data"]:
            c["data"] = payload[:40]
    elif proto == 17:
        sport, dport = struct.unpack("!HH", l4[:4])
        protos["UDP"] += 1
        if dport == 53:
            dns_names.append((src, qname(l4[8:])))
    elif proto == 1:
        protos["ICMP"] += 1
    else:
        protos[f"IP proto {proto}"] += 1

print(f"frames: {frames}, duration: {last - first:.3f} s")
print("protocols: " + ", ".join(f"{k} {v}" for k, v in protos.most_common()))
print("\ntop talkers (bytes sent):")
for host, b in talkers.most_common(5):
    print(f"  {host:<16} {b:>6}")

print("\nTCP conversations:")
for (a, b), c in convs.items():
    cli = c["client"] or a
    srv = b if cli == a else a
    fl = c["flags"]
    if (SYN | ACK) in fl and any(f & ACK and not f & SYN for f in fl) and not any(f & RST for f in fl):
        state = "established" + (", closed with FIN" if any(f & FIN for f in fl) else "")
    elif any(f & RST for f in fl) and (SYN | ACK) in fl:
        state = "half-open, reset by client (port open)"
    elif any(f & RST for f in fl):
        state = "rejected with RST (port closed)"
    else:
        state = "no reply"
    first_bytes = c["data"].split(b"\r\n")[0].decode(errors="replace")
    print(f"  {cli[0]}:{cli[1]} -> {srv[0]}:{srv[1]:<5} {c['bytes']:>5} B  {state}" + (f"  [{first_bytes}]" if first_bytes else ""))

print("\nDNS queries:")
for src, name in dns_names:
    first_label = name.split(".")[0]
    flag = "  <- long, high-entropy label" if len(first_label) > 24 and entropy(first_label) > 3.5 else ""
    print(f"  {src:<16} {name}{flag}")

print("\npossible scanners (SYNs to 10 or more distinct host:port pairs):")
found = False
for src, targets in syn_targets.items():
    if len(targets) >= 10:
        found = True
        print(f"  {src} sent SYNs to {len(targets)} targets, ports {sorted(p for _, p in targets)}")
if not found:
    print("  none")
