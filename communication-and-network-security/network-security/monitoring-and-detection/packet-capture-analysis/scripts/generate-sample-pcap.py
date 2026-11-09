# Python 3.10, standard library only. Run: python3 generate-sample-pcap.py sample.pcap
# Writes a small synthetic capture for the packet capture analysis note: one HTTP session,
# a few DNS lookups, one ping and a SYN scan. All addresses are documentation ranges (RFC 5737),
# so the file is safe to share and cannot point at a real host.
import struct
import sys

LINKTYPE_ETHERNET = 1
MAC_CLIENT, MAC_SERVER, MAC_GW = b"\x02\x00\x00\x00\x00\x10", b"\x02\x00\x00\x00\x00\x20", b"\x02\x00\x00\x00\x00\x01"
CLIENT, SERVER, RESOLVER, SCANNER = "192.0.2.10", "198.51.100.20", "192.0.2.53", "203.0.113.66"


def ip_bytes(addr):
    return bytes(int(p) for p in addr.split("."))


def checksum(data):
    if len(data) % 2:
        data += b"\x00"
    s = sum(struct.unpack(f"!{len(data)//2}H", data))
    while s >> 16:
        s = (s & 0xFFFF) + (s >> 16)
    return ~s & 0xFFFF


def ipv4(src, dst, proto, payload, ident):
    hdr = struct.pack("!BBHHHBBH4s4s", 0x45, 0, 20 + len(payload), ident, 0x4000, 64, proto, 0, ip_bytes(src), ip_bytes(dst))
    hdr = hdr[:10] + struct.pack("!H", checksum(hdr)) + hdr[12:]
    return hdr + payload


def pseudo(src, dst, proto, length):
    return ip_bytes(src) + ip_bytes(dst) + struct.pack("!BBH", 0, proto, length)


def tcp(src, dst, sport, dport, seq, ack, flags, data=b""):
    hdr = struct.pack("!HHIIBBHHH", sport, dport, seq, ack, 5 << 4, flags, 64240, 0, 0)
    csum = checksum(pseudo(src, dst, 6, len(hdr) + len(data)) + hdr + data)
    return hdr[:16] + struct.pack("!H", csum) + hdr[18:] + data


def udp(src, dst, sport, dport, data):
    hdr = struct.pack("!HHHH", sport, dport, 8 + len(data), 0)
    csum = checksum(pseudo(src, dst, 17, len(hdr) + len(data)) + hdr + data)
    return hdr[:6] + struct.pack("!H", csum) + data


def icmp_echo(kind, ident, seq):
    body = struct.pack("!BBHHH", kind, 0, 0, ident, seq) + b"lab-ping"
    return body[:2] + struct.pack("!H", checksum(body)) + body[4:]


def dns_query(qid, name):
    q = b"".join(bytes([len(l)]) + l.encode() for l in name.split(".")) + b"\x00"
    return struct.pack("!HHHHHH", qid, 0x0100, 1, 0, 0, 0) + q + struct.pack("!HH", 1, 1)


def eth(src_mac, dst_mac, packet):
    return dst_mac + src_mac + b"\x08\x00" + packet


FIN, SYN, RST, PSH, ACK = 0x01, 0x02, 0x04, 0x08, 0x10
frames, t, ident = [], 1_790_000_000.0, 1


def add(src_mac, dst_mac, src, dst, proto, payload, gap=0.001):
    global t, ident
    t += gap
    ident += 1
    frames.append((t, eth(src_mac, dst_mac, ipv4(src, dst, proto, payload, ident))))


# DNS lookups from the client, one of them unusually long (looks like encoded data)
for qid, name in [(0x1A2B, "www.example.com"), (0x1A2C, "updates.example.net"),
                  (0x1A2D, "mzxw6ytboi2dsnrqgezdgnbvgy3tqojq.t.example.org")]:
    add(MAC_CLIENT, MAC_GW, CLIENT, RESOLVER, 17, udp(CLIENT, RESOLVER, 53000 + qid % 100, 53, dns_query(qid, name)), 0.2)

# One complete HTTP exchange: handshake, request, response, teardown
c, s = 1000, 5000
req = b"GET /index.html HTTP/1.1\r\nHost: www.example.com\r\nUser-Agent: lab-client\r\n\r\n"
resp = b"HTTP/1.1 200 OK\r\nContent-Length: 5\r\n\r\nhello"
add(MAC_CLIENT, MAC_GW, CLIENT, SERVER, 6, tcp(CLIENT, SERVER, 51515, 80, c, 0, SYN), 0.3)
add(MAC_GW, MAC_CLIENT, SERVER, CLIENT, 6, tcp(SERVER, CLIENT, 80, 51515, s, c + 1, SYN | ACK), 0.02)
add(MAC_CLIENT, MAC_GW, CLIENT, SERVER, 6, tcp(CLIENT, SERVER, 51515, 80, c + 1, s + 1, ACK))
add(MAC_CLIENT, MAC_GW, CLIENT, SERVER, 6, tcp(CLIENT, SERVER, 51515, 80, c + 1, s + 1, PSH | ACK, req))
add(MAC_GW, MAC_CLIENT, SERVER, CLIENT, 6, tcp(SERVER, CLIENT, 80, 51515, s + 1, c + 1 + len(req), PSH | ACK, resp), 0.02)
add(MAC_CLIENT, MAC_GW, CLIENT, SERVER, 6, tcp(CLIENT, SERVER, 51515, 80, c + 1 + len(req), s + 1 + len(resp), FIN | ACK))
add(MAC_GW, MAC_CLIENT, SERVER, CLIENT, 6, tcp(SERVER, CLIENT, 80, 51515, s + 1 + len(resp), c + 2 + len(req), FIN | ACK), 0.02)
add(MAC_CLIENT, MAC_GW, CLIENT, SERVER, 6, tcp(CLIENT, SERVER, 51515, 80, c + 2 + len(req), s + 2 + len(resp), ACK))

# A ping from the client to the server and its reply
add(MAC_CLIENT, MAC_GW, CLIENT, SERVER, 1, icmp_echo(8, 0x77, 1), 0.5)
add(MAC_GW, MAC_CLIENT, SERVER, CLIENT, 1, icmp_echo(0, 0x77, 1), 0.02)

# SYN scan from an outside address against the server: open ports answer SYN-ACK and get a RST,
# closed ports answer RST-ACK. No handshake is ever completed.
open_ports = {22, 80, 443}
for i, port in enumerate([21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389]):
    add(MAC_GW, MAC_SERVER, SCANNER, SERVER, 6, tcp(SCANNER, SERVER, 40000, port, 7000 + i, 0, SYN), 0.003)
    if port in open_ports:
        add(MAC_SERVER, MAC_GW, SERVER, SCANNER, 6, tcp(SERVER, SCANNER, port, 40000, 9000 + i, 7001 + i, SYN | ACK))
        add(MAC_GW, MAC_SERVER, SCANNER, SERVER, 6, tcp(SCANNER, SERVER, 40000, port, 7001 + i, 0, RST))
    else:
        add(MAC_SERVER, MAC_GW, SERVER, SCANNER, 6, tcp(SERVER, SCANNER, port, 40000, 0, 7001 + i, RST | ACK))

out = sys.argv[1] if len(sys.argv) > 1 else "sample.pcap"
with open(out, "wb") as f:
    f.write(struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, LINKTYPE_ETHERNET))
    for ts, frame in frames:
        f.write(struct.pack("<IIII", int(ts), int((ts % 1) * 1_000_000), len(frame), len(frame)) + frame)
print(f"wrote {len(frames)} frames to {out}")
