#!/usr/bin/env python3
"""Write a small synthetic pcap with three HTTP sessions for IDS testing.

Python 3.10, standard library only. Addresses are from the documentation ranges
(RFC 5737). Usage: python3 make-ids-lab-pcap.py lab.pcap
"""
import struct
import sys
import time


def csum(data: bytes) -> int:
    if len(data) % 2:
        data += b"\0"
    s = sum(struct.unpack(f"!{len(data)//2}H", data))
    s = (s >> 16) + (s & 0xFFFF)
    s += s >> 16
    return ~s & 0xFFFF


def ip4(a):
    return bytes(int(x) for x in a.split("."))


def packet(src, dst, sport, dport, seq, ack, flags, payload=b""):
    tcp_len = 20 + len(payload)
    tcp = struct.pack("!HHIIBBHHH", sport, dport, seq, ack, 5 << 4, flags, 64240, 0, 0) + payload
    pseudo = ip4(src) + ip4(dst) + struct.pack("!BBH", 0, 6, tcp_len)
    tcp = tcp[:16] + struct.pack("!H", csum(pseudo + tcp)) + tcp[18:]
    iph = struct.pack("!BBHHHBBH4s4s", 0x45, 0, 20 + tcp_len, 1, 0x4000, 64, 6, 0, ip4(src), ip4(dst))
    iph = iph[:10] + struct.pack("!H", csum(iph)) + iph[12:]
    eth = b"\x02\x00\x00\x00\x00\x02" + b"\x02\x00\x00\x00\x00\x01" + b"\x08\x00"
    return eth + iph + tcp


def session(client, server, sport, request, response):
    SYN, ACK, PSH, FIN = 0x02, 0x10, 0x08, 0x01
    c, s = 1000, 5000
    pk = [packet(client, server, sport, 80, c, 0, SYN),
          packet(server, client, 80, sport, s, c + 1, SYN | ACK),
          packet(client, server, sport, 80, c + 1, s + 1, ACK),
          packet(client, server, sport, 80, c + 1, s + 1, PSH | ACK, request),
          packet(server, client, 80, sport, s + 1, c + 1 + len(request), PSH | ACK, response),
          packet(client, server, sport, 80, c + 1 + len(request), s + 1 + len(response), FIN | ACK),
          packet(server, client, 80, sport, s + 1 + len(response), c + 2 + len(request), FIN | ACK),
          packet(client, server, sport, 80, c + 2 + len(request), s + 2 + len(response), ACK)]
    return pk


def http(method_path, host, ua):
    return f"{method_path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {ua}\r\nAccept: */*\r\n\r\n".encode()


OK = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 2\r\n\r\nok"
pkts = []
pkts += session("198.51.100.20", "203.0.113.5", 40001, http("GET /index.html", "shop.example.com", "Mozilla/5.0"), OK)
pkts += session("198.51.100.66", "203.0.113.5", 40002,
                http("GET /search?q=%3Cscript%3Ealert(1)%3C%2Fscript%3E", "shop.example.com", "Mozilla/5.0"), OK)
pkts += session("198.51.100.66", "203.0.113.5", 40003, http("GET /admin/config.php", "shop.example.com", "sqlmap/1.8"), OK)

with open(sys.argv[1], "wb") as f:
    f.write(struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1))  # pcap global header, Ethernet
    t = 1794355200  # 2026-11-11 00:00:00 UTC
    for i, p in enumerate(pkts):
        f.write(struct.pack("<IIII", t + i // 8, (i % 8) * 1000, len(p), len(p)) + p)
print(f"wrote {len(pkts)} packets")
