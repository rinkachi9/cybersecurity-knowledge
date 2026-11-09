# Network scanning

## Summary

Network scanning is the active probing of a network to discover which hosts are alive, which ports are open, and which services and versions are running. It is the reconnaissance step that precedes most attacks, and it is equally a core tool of defenders doing asset discovery and [vulnerability management](../../../security-operations/vulnerability-management/README.md). The main techniques are host discovery (who is there), port scanning (what is open), and service and version detection (what is running). Understanding scanning from both sides matters: a defender must know what a scan reveals, how to detect one, and how to reduce what scanning exposes. This note connects to the attacker's [reconnaissance](../../../security-operations/threats-and-attacks/attack-lifecycle/reconnaissance.md) phase and reuses the scan-detection work from [packet capture analysis](../monitoring-and-detection/packet-capture-analysis/README.md).

## Prerequisites

- [Reconnaissance](../../../security-operations/threats-and-attacks/attack-lifecycle/reconnaissance.md): scanning is the active half.
- [TCP attacks](../core-protocols/tcp-attacks.md) and [packet capture analysis](../monitoring-and-detection/packet-capture-analysis/README.md): TCP flags and detecting scans.
- Authorized use only: scan only networks you own or are authorized in writing to test.

## Core concepts

### Definition

*Network scanning* is the systematic sending of probes to a range of addresses and ports to map the reachable attack surface: live hosts, open ports, and the services and versions behind them. The dominant tool is nmap.

### Analogy

Scanning is a burglar walking down a street at night, noting which houses have lights on (live hosts), trying each door and window to see which are unlocked (open ports), and peering in to guess what is inside and how old the locks are (service and version detection). A security patrol does exactly the same walk to find the unlocked doors first and get them fixed. The same activity serves attacker and defender; intent and authorization are the difference.

The analogy holds well; it breaks in that network scanning can cover millions of "houses" in minutes and can be done from anywhere on the internet, so exposure is far larger than a physical street.

### Host discovery

Before scanning ports, a scanner finds which hosts respond: ICMP echo (ping), TCP probes to common ports, ARP (on the local segment, the most reliable), and others. Defenders who block ICMP do not hide, scanners fall back to TCP probes, and blocking all discovery also breaks legitimate monitoring.

### Port scan types

| Scan | How it works | What it tells the attacker | Visibility |
| --- | --- | --- | --- |
| TCP connect | Completes the full handshake | Port open/closed | Noisy, logged by the service |
| SYN (half-open) | Sends SYN, sees SYN-ACK (open) or RST (closed), never completes | Port open/closed, stealthier | Less likely to be logged by the app |
| UDP | Sends UDP, infers from ICMP unreachable or reply | Open UDP services (slow, unreliable) | Slow; often rate-limited |
| FIN/NULL/Xmas | Unusual flag combinations | Exploits RFC behavior to infer state, evade some filters | Detectable by anomaly |

The SYN scan is the classic default: it learns the port state without completing connections, as shown in the [packet capture note](../monitoring-and-detection/packet-capture-analysis/README.md), where a scanner's SYNs draw SYN-ACK from open ports (22, 80, 443) and RST from closed ones.

### Service and version detection

Beyond "open", scanners probe the service to identify it and its version (banner grabbing, protocol-specific probes), and may run scripts to check for known issues. Version information is what connects a scan to [vulnerability management](../../../security-operations/vulnerability-management/cve.md): knowing "OpenSSH 8.9 on port 22" lets an attacker (or defender) look up relevant [CVEs](../../../security-operations/vulnerability-management/cve.md).

## Worked example

Detecting a scan from captured traffic, reusing the [packet capture analysis](../monitoring-and-detection/packet-capture-analysis/README.md) sample and its tested summarizer (Python 3.10, cross-checked with tcpdump 4.99.1, 2026-10):

```text
possible scanners (SYNs to 10 or more distinct host:port pairs):
  203.0.113.66 sent SYNs to 12 targets, ports [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389]

TCP conversations:
  203.0.113.66:40000 -> 198.51.100.20:22   half-open, reset by client (port open)
  203.0.113.66:40000 -> 198.51.100.20:21   rejected with RST (port closed)
  ...
```

Reading it: one source sent SYNs to twelve common ports and completed no handshakes. Open ports answered SYN-ACK and the scanner replied RST (classic half-open scan); closed ports answered RST-ACK. The detection signal is the fan-out, many destination ports (or many hosts) from one source in a short time with few or no completed connections. That heuristic (SYNs to 10+ distinct targets) is exactly what the summarizer flags.

From the defender's side, the same capture tells you what the attacker learned: ports 22, 80 and 443 are open on `198.51.100.20`. The response is to confirm those services are meant to be exposed, patched, and monitored, and to reduce the exposed surface.

## Detection and mitigation

- **Detect the pattern, not the packet.** A scan is many probes from one source to many ports/hosts with low completion; IDS/IPS ([Suricata/Snort](../monitoring-and-detection/suricata-and-snort.md)), flow analysis, and the fan-out heuristic above all catch it. Individual probes look normal; the aggregate does not.
- **Reduce the attack surface.** The best response to scanning is to have little to find: close unused ports, remove unnecessary services, and segment so a scanner reaches little ([segmentation](../architecture/network-segmentation.md), [egress filtering](../traffic-filtering/egress-filtering.md)).
- **Rate-limit and tarpit.** Rate-limiting probes and connection attempts slows scans; tarpits waste the scanner's time.
- **Do not rely on hiding.** Blocking ICMP or changing ports (security by obscurity) barely slows a determined scanner and breaks legitimate tooling. Fix the exposure, do not hide it.
- **Scan yourself first.** Regular authorized scanning (asset discovery, [vulnerability management](../../../security-operations/vulnerability-management/README.md)) finds the exposed surface before an attacker does.

## Trade offs and when to use it

- **Defensive scanning cadence.** Frequent scanning finds new exposure quickly but generates load and noise; schedule and scope it. Authenticated scans (with credentials) find more but need careful handling.
- **Detect vs block scanning.** Blocking a scanning source stops that scan but attackers use many sources and slow scans; detection and surface reduction matter more than chasing sources.
- **Stealth vs speed (attacker side, for understanding).** Slow, distributed scans evade threshold-based detection but take longer; this is why detection combines rate thresholds with behavioral and flow analysis.

## Common mistakes

- **Trying to hide instead of reducing exposure.** Blocking ping or moving ports barely helps and breaks monitoring. Fix: close and patch what is exposed; segment.
- **Alerting on single probes.** Too noisy; real scans are patterns. Fix: threshold and behavioral detection on fan-out and low completion.
- **Never scanning your own network.** You do not know your exposed surface. Fix: regular authorized asset and vulnerability scanning.
- **Ignoring UDP services.** UDP scans are slow so UDP exposure is often overlooked by both sides. Fix: include UDP in your own assessments.
- **Scanning without authorization.** Even internally, uncoordinated scans cause incidents and can be illegal externally. Fix: written authorization and scope.

## Practice

1. What three things does a full network scan try to discover?
2. How does a SYN (half-open) scan determine whether a port is open without completing a connection?
3. Why is a scan detected by its pattern rather than by individual packets?
4. Why is reducing attack surface a better response to scanning than hiding hosts?
5. How does service/version detection connect scanning to vulnerability management?

### Answers

1. Which hosts are alive (host discovery), which ports are open (port scanning), and which services and versions are running (service/version detection).
2. It sends a SYN; an open port replies SYN-ACK (the scanner then sends RST instead of the final ACK) and a closed port replies RST-ACK, so the port state is learned from the response without finishing the handshake.
3. Individual probes look like ordinary connection attempts; the attack signature is the aggregate, one source probing many ports or hosts in a short time with few or no completed connections.
4. Hiding (blocking ping, changing ports) barely slows a determined scanner and breaks legitimate tooling, whereas closing, removing and segmenting services means a scan finds little to attack regardless of stealth.
5. Identifying the exact service and version lets you (or an attacker) look up known CVEs for that version, turning an open port into a specific, actionable vulnerability.

## Further reading

- Nmap reference guide and the book Nmap Network Scanning (Lyon): https://nmap.org/book/
- [Reconnaissance](../../../security-operations/threats-and-attacks/attack-lifecycle/reconnaissance.md) for the attacker-lifecycle context.
- [Packet capture analysis](../monitoring-and-detection/packet-capture-analysis/README.md) for the tested scan-detection example.
- MITRE ATT&CK, Network Service Discovery (T1046) and Active Scanning (T1595): https://attack.mitre.org/techniques/T1046/
