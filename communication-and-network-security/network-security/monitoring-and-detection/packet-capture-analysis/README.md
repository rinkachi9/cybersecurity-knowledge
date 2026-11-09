# Packet capture analysis

## Summary

Packet capture (PCAP) analysis is the examination of recorded network traffic at the packet level to understand what happened on a network: who talked to whom, over what protocol, and with what content. It is the ground truth of network security monitoring, because unlike logs it shows the actual bytes on the wire. This note explains the capture format, the Berkeley Packet Filter (BPF) language used to select traffic, and a triage workflow, using `tcpdump` and a small reader script on a synthetic capture that contains a web session, DNS lookups, a ping and a port scan.

## Prerequisites

- [Network security monitoring](../network-security-monitoring.md): where capture fits among data sources.
- TCP/IP basics: the handshake, flags, ports, DNS.
- The [network security lab](../../foundations/network-security-lab/README.md) if you want to capture live traffic yourself.

## Core concepts

### Definition

A *packet capture* is a file of recorded frames, each with a timestamp and the raw bytes as seen on an interface. The classic format is *pcap* (libpcap); the newer *pcapng* format adds multiple interfaces and metadata. A *capture filter* (BPF) decides which packets are recorded or read; a *display filter* (in Wireshark) decides which are shown.

### Analogy

A packet capture is a security camera recording of a hallway, frame by frame with timestamps. A capture filter is choosing which cameras to record; a display filter is fast-forwarding to the clips with a person in a red coat. The recording shows exactly what happened, but a full recording of a busy hallway is enormous, so you film selectively and review with filters.

The analogy breaks because packets can be forged and encrypted: the camera might show an actor in a costume (spoofed source) or a person carrying a locked box whose contents you cannot see (TLS).

### The capture file format

A classic pcap file is a 24-byte global header (a magic number that also encodes byte order and timestamp resolution, plus the link type, for example Ethernet) followed by records, each a 16-byte record header (timestamp seconds, microseconds, captured length, original length) and the packet bytes. The reader script in this note parses exactly this structure, so every field is visible rather than hidden behind a library.

### Berkeley Packet Filter (BPF)

BPF is the filter language used by `tcpdump`, libpcap and many sensors. It compiles a small program that the kernel runs on each packet, so filtering happens before the packet is copied to user space, which is efficient. Useful primitives:

| Filter | Matches |
| --- | --- |
| `host 198.51.100.20` | traffic to or from that address |
| `net 192.0.2.0/24` | traffic to or from that network |
| `port 53` | TCP or UDP port 53 either direction |
| `tcp port 443` | TCP 443 only |
| `tcp[tcpflags] & tcp-syn != 0` | packets with the SYN flag set |
| `tcp[tcpflags] & (tcp-syn\|tcp-ack) == tcp-syn` | SYN without ACK (connection attempts) |
| `icmp[icmptype] == icmp-echo` | ICMP echo requests |
| `udp port 53 and greater 100` | DNS packets over 100 bytes (unusually large queries) |

Filters combine with `and`, `or`, `not`. A capture filter should be as narrow as possible to keep files small and avoid dropping packets under load.

### A triage workflow

Given an unknown capture:

1. **Scope.** How many packets, over what time span, which protocols dominate.
2. **Talkers.** Which addresses send and receive the most. Outliers are interesting.
3. **Conversations.** Which connections exist and in what state. Many half-open connections suggest scanning; one long connection moving a lot of data suggests transfer or exfiltration.
4. **Names.** DNS queries reveal intent. Long, high-entropy query names suggest [tunneling](../../dns-security/dns-tunneling/README.md).
5. **Anomalies.** Scans, unexpected protocols, cleartext credentials, odd ports.
6. **Content.** For cleartext protocols, read the payload. For encrypted ones, use metadata ([encrypted traffic analysis](../encrypted-traffic-analysis.md)).

## Worked example

The script [scripts/generate-sample-pcap.py](scripts/generate-sample-pcap.py) writes a synthetic capture (documentation addresses only), and [scripts/summarize-pcap.py](scripts/summarize-pcap.py) performs the triage above. Both are pure Python, tested with Python 3.10 and cross-checked against tcpdump 4.99.1, 2026-10.

```bash
python3 scripts/generate-sample-pcap.py sample.pcap
python3 scripts/summarize-pcap.py sample.pcap
```

Output (abridged):

```text
frames: 40, duration: 1.335 s
protocols: TCP 35, UDP 3, ICMP 2

TCP conversations:
  192.0.2.10:51515 -> 198.51.100.20:80      550 B  established, closed with FIN  [GET /index.html HTTP/1.1]
  203.0.113.66:40000 -> 198.51.100.20:21      108 B  rejected with RST (port closed)
  203.0.113.66:40000 -> 198.51.100.20:22      162 B  half-open, reset by client (port open)
  203.0.113.66:40000 -> 198.51.100.20:80      162 B  half-open, reset by client (port open)
  203.0.113.66:40000 -> 198.51.100.20:443     162 B  half-open, reset by client (port open)
  ...

DNS queries:
  192.0.2.10       www.example.com
  192.0.2.10       mzxw6ytboi2dsnrqgezdgnbvgy3tqojq.t.example.org  <- long, high-entropy label

possible scanners (SYNs to 10 or more distinct host:port pairs):
  203.0.113.66 sent SYNs to 12 targets, ports [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389]
```

Reading the result: one host completed a normal web request. A second address (`203.0.113.66`) sent SYNs to twelve ports and never completed a handshake. The pattern of "SYN, SYN-ACK from open ports, then RST from the scanner" is a *SYN scan* (half-open scan): the scanner learns which ports are open without finishing the connection. Ports that answered with SYN-ACK (22, 80, 443) are open; the rest answered RST-ACK and are closed. One DNS name is far longer and more random than the others, the signature of encoded data in a name.

The same facts can be confirmed with tcpdump. Counting connection attempts:

```bash
tcpdump -nn -r sample.pcap 'tcp[tcpflags] & (tcp-syn|tcp-ack) == tcp-syn'
```

shows 13 SYN packets (one web client plus twelve scan probes). Listing which ports answered open:

```bash
tcpdump -nn -r sample.pcap 'tcp[tcpflags] == (tcp-syn|tcp-ack)'
# -> 198.51.100.20.80, .22, .80, .443
```

and reading the cleartext HTTP request:

```bash
tcpdump -nn -A -r sample.pcap 'tcp port 80 and tcp[tcpflags] & tcp-push != 0'
# -> GET /index.html HTTP/1.1  Host: www.example.com  User-Agent: lab-client
```

The scan detection and the port-scan topic connect to [network scanning](../../network-attacks/network-scanning.md).

## Trade offs and when to use it

- **Full capture vs flow records.** Full packets give content and certainty but are huge and raise privacy concerns. [Flow records](../flow-monitoring.md) are compact and keepable for a long time but have no payload. Most programs keep flows long-term and full packets briefly at key points.
- **Capture everywhere vs at choke points.** Capturing at every link is impractical. Place sensors where segmentation forces traffic through, which is another reason segmentation and monitoring are designed together.
- **tcpdump vs Wireshark vs Zeek.** `tcpdump` is for quick capture and BPF filtering. Wireshark is for deep manual inspection with dissectors. [Zeek](../zeek.md) turns packets into structured logs for scale.

## Common mistakes

- **Dropped packets under load.** A filter that is too broad or a disk too slow causes the capture to miss packets, and the analysis is then wrong. Fix: narrow capture filters, fast storage, watch the drop counter.
- **Capturing on the wrong interface or missing a VLAN tag.** Fix: confirm the tap or mirror actually carries the traffic, including both directions.
- **Trusting the source address.** A spoofed source looks real in the capture. Fix: corroborate with direction, interface and state.
- **Ignoring privacy and legal limits.** Full capture records user content. Fix: capture under policy, with authorization, minimized retention, and access control.
- **Reading pcapng with a pcap-only tool.** Fix: convert first (`editcap -F pcap in.pcapng out.pcap`); the script in this note states this limitation.

## Practice

1. What does a BPF filter of `tcp[tcpflags] & (tcp-syn|tcp-ack) == tcp-syn` select, and why is it useful?
2. In the example, how do you tell an open port from a closed one in a SYN scan?
3. Why is a very long, random-looking DNS query name suspicious?
4. Give one reason to keep flow records long-term but full packets only briefly.
5. Why can you not rely on the source IP in a capture to identify the sender?

### Answers

1. Packets with SYN set and ACK clear, that is, new connection attempts. It isolates the first packet of each connection, which makes scans and connection rates visible.
2. An open port replies SYN-ACK (and the scanner then sends RST); a closed port replies RST-ACK. The script labels these "half-open, reset by client (port open)" and "rejected with RST (port closed)".
3. The labels of a domain name carry at most 63 characters and normally encode human-meaningful words; a long high-entropy label usually means data has been encoded into the name, as in DNS tunneling.
4. Full packets are large, contain user content with privacy implications, and fill storage quickly; flow records are small and keepable for months of history.
5. The source address is written by the sender and can be spoofed; only corroborating evidence (direction, interface, connection state, replies) tells you whether it is genuine.

## Further reading

- `tcpdump` manual page and https://www.tcpdump.org/ , including the pcap-filter(7) page for the full BPF syntax.
- Wireshark User's Guide, https://www.wireshark.org/docs/ , for interactive analysis and dissectors.
- Sanders, C., Practical Packet Analysis (No Starch Press). A practical, example-driven introduction.
- The pcap file format: https://datatracker.ietf.org/doc/html/draft-gharris-opsawg-pcap and pcapng: https://datatracker.ietf.org/doc/html/draft-ietf-opsawg-pcapng
