# ICMP security

## Summary

The Internet Control Message Protocol (ICMP) carries control and error messages for IP: "destination unreachable", "time exceeded", "fragmentation needed", and the echo request/reply behind `ping`. It is essential for a healthy network, yet it is abused for reconnaissance, redirection, covert channels and floods. The security task is selective, not binary: keep the ICMP messages the network needs to function, rate-limit the abusable ones, and drop the dangerous legacy types. Blanket-blocking all ICMP is a common mistake that breaks path MTU discovery and diagnostics while providing little real security.

## Prerequisites

- [Attack surface by layer](../foundations/attack-surface-by-layer.md): ICMP sits at the internet layer.
- [ICMP flood](../network-attacks/denial-of-service/icmp-flood.md): the denial-of-service side.
- [IP spoofing and source address validation](ip-spoofing-and-source-validation.md): redirects and spoofing.

## Core concepts

### Definition

*ICMP* (RFC 792 for IPv4, RFC 4443 for ICMPv6) is a companion protocol to IP that reports errors and provides diagnostics. Messages have a type and code. ICMPv6 is more deeply integrated: it also carries Neighbor Discovery, which replaces ARP, so ICMPv6 cannot be blocked the way some sites block ICMPv4. See [IPv6 security](ipv6-security.md).

### Analogy

ICMP is the road-sign and traffic-report system of IP. "Road closed ahead" (destination unreachable) and "this bridge only takes small trucks" (fragmentation needed) keep traffic flowing correctly. An attacker can post a fake "detour this way" sign (ICMP redirect) to route you past their position, or simply flood the roads with cars (echo flood). Tearing down all road signs to stop the fake ones leaves everyone lost at the first closed road.

The analogy holds well; ICMP really is infrastructure signalling, and removing it causes the quiet, hard-to-diagnose failures that missing road signs would.

### Security-relevant ICMP messages

| Message | Type | Legitimate use | Abuse | Recommended handling |
| --- | --- | --- | --- | --- |
| Echo request/reply | 8/0 (v4) | `ping`, liveness checks | Host discovery, floods, covert channel in payload | Permit, rate-limit |
| Destination unreachable | 3 | Fast failure notification | Reconnaissance (which ports/hosts respond) | Permit, especially code 4 |
| Fragmentation needed (PTB) | 3/4 (v4), type 2 (v6) | Path MTU discovery | - | Permit; blocking it causes black-hole connections |
| Time exceeded | 11 | `traceroute`, TTL expiry | Topology mapping | Permit (diagnostics) or limit outbound |
| Redirect | 5 | Gateway suggests a better route | Reroute a host's traffic through the attacker | Drop; disable acceptance on hosts |
| Timestamp / address mask | 13/17 | Obsolete diagnostics | Information disclosure | Drop |

### The three main abuses

- **Reconnaissance.** Echo and the pattern of unreachable replies reveal which hosts and services exist. This is mapping, not compromise, and is covered in [network scanning](../network-attacks/network-scanning.md); the response is to limit what you reveal, not to break diagnostics.
- **Redirection.** An ICMP redirect tells a host "use this other gateway for that destination". Accepting it from an attacker reroutes traffic through them. Modern hosts disable acceptance by default; on this reference host `net.ipv4.conf.all.accept_redirects = 0`.
- **Covert channels and tunneling.** The echo payload is arbitrary data, so tools can carry a shell or exfiltrate files inside ping packets (ICMP tunneling). Detection looks for echo packets with unusual sizes, high volume, or non-standard payloads, similar in spirit to [DNS tunneling](../dns-security/dns-tunneling/README.md).

### Why you must not block all ICMP

Several messages are load-bearing:

- *Fragmentation needed* (PTB) drives path MTU discovery. Block it and connections that send large packets stall mysteriously (the "works for small requests, hangs on large ones" symptom), a widespread misconfiguration.
- *Destination unreachable* lets senders fail fast instead of waiting for timeouts.
- For IPv6, Neighbor Discovery and PTB are ICMPv6; blocking ICMPv6 breaks basic connectivity. RFC 4890 specifies exactly which ICMPv6 messages to permit.

## Worked example

Reading and reasoning about ICMP posture on the reference host (2026-10):

```bash
sysctl net.ipv4.conf.all.accept_redirects net.ipv4.conf.all.send_redirects net.ipv4.icmp_echo_ignore_broadcasts
```

```text
net.ipv4.conf.all.accept_redirects = 0        # ignores ICMP redirects (good)
net.ipv4.conf.all.send_redirects = 1          # still sends redirects (disable on non-routers)
net.ipv4.icmp_echo_ignore_broadcasts = 1      # ignores broadcast echo (anti-smurf, good)
```

Interpretation: the host will not be redirected by a forged ICMP redirect and will not answer broadcast echo (so it cannot be a smurf amplifier), which are both correct. It still *sends* redirects, which only makes sense on a router; on an end host or a hardened server this should be `0`.

At the firewall, the correct policy permits the essential types and rate-limits echo, as in the lab [baseline ruleset](../traffic-filtering/firewall-rule-design/scripts/fw-baseline.nft):

```
ip protocol icmp icmp type { destination-unreachable, time-exceeded, parameter-problem } accept
icmp type echo-request limit rate over 5/second burst 10 packets drop
icmp type echo-request accept
```

This keeps diagnostics and path MTU discovery working while capping echo abuse.

## Trade offs and when to use it

- **Permit vs limit echo.** Permitting echo helps monitoring and troubleshooting; the reconnaissance it enables is minor compared with the operational cost of blocking it. Rate-limit rather than block.
- **Permit essential errors.** The small information disclosure from unreachable and time-exceeded is outweighed by the breakage from dropping them. Permit PTB always.
- **Drop redirects and obsolete types.** Near-zero legitimate use, real risk; drop and disable acceptance.
- **ICMPv6 is not optional.** Follow RFC 4890 rather than reflexively filtering; over-filtering ICMPv6 breaks IPv6 outright.

## Common mistakes

- **Blocking all ICMP.** Breaks path MTU discovery (hung large transfers) and fast failure. Fix: selective filtering per RFC 4890 and the table above.
- **Leaving redirect acceptance enabled.** Allows traffic redirection. Fix: `accept_redirects = 0` (already set here); `send_redirects = 0` on non-routers.
- **Ignoring ICMP tunneling.** Echo payloads can carry data. Fix: monitor echo size, volume and payload; block unusual echo at egress if policy allows.
- **Allowing broadcast echo.** Makes the host a smurf amplifier. Fix: `icmp_echo_ignore_broadcasts = 1` (set here), disable directed broadcasts on routers.
- **Over-filtering ICMPv6.** Breaks Neighbor Discovery and connectivity. Fix: RFC 4890 allow list.

## Practice

1. Why is "block all ICMP" harmful, and which single message's loss causes hung large transfers?
2. What does an ICMP redirect do, and why is accepting one from an untrusted source dangerous?
3. How can ICMP be used as a covert channel, and how is that detected?
4. Why can ICMPv6 not be treated the way some sites treat ICMPv4?
5. On the reference host, which ICMP setting is still wrong for an end host, and what should it be?

### Answers

1. Several ICMP messages are essential; blocking the "fragmentation needed" (packet-too-big) message breaks path MTU discovery, so connections that send large packets hang.
2. It tells a host to use a different gateway for some destination; accepting a forged redirect reroutes the host's traffic through the attacker.
3. The echo request/reply payload is arbitrary, so data or a shell can be carried inside ping packets; detection looks for echo packets with unusual sizes, high volume, or non-standard payloads.
4. ICMPv6 carries Neighbor Discovery and path-MTU signalling that IPv6 depends on, so blocking it breaks basic connectivity; RFC 4890 specifies which types to permit.
5. `send_redirects = 1`; on an end host (non-router) it should be `0`.

## Further reading

- RFC 792, Internet Control Message Protocol (IPv4), and RFC 4443, ICMPv6: https://www.rfc-editor.org/rfc/rfc4443
- RFC 4890, Recommendations for Filtering ICMPv6 Messages in Firewalls (2007): https://www.rfc-editor.org/rfc/rfc4890
- RFC 1191, Path MTU Discovery, on why PTB messages must pass: https://www.rfc-editor.org/rfc/rfc1191
- Linux kernel `Documentation/networking/ip-sysctl.rst` for the ICMP sysctls.
