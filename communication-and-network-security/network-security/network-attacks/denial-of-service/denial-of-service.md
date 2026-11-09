# Denial of service

## Summary

A denial of service (DoS) attack makes a system or network unavailable to its legitimate users. It does this by exhausting a resource the service depends on, such as link bandwidth, a state table, CPU or memory, or by sending input that crashes it. When the traffic comes from many sources at once, it is a distributed denial of service (DDoS). DoS attacks the availability part of the CIA triad. Unlike most attacks, it needs no foothold, no stolen credential and often no vulnerability, only more traffic or more expensive requests than the target can absorb. That is why the defense is mostly about capacity, filtering close to the source and making each request cheap to handle.

## Prerequisites

- [CIA triad](../../../../security-and-risk-management/foundations/cia-triad/README.md): DoS is the attack on availability.
- [Network threat model](../../foundations/network-threat-model.md): which attacker positions can spoof, reflect or flood.
- [Protocol design weaknesses](../../foundations/protocol-design-weaknesses.md): why IP lets a sender lie about its source address.
- Basic knowledge of the TCP three-way handshake and of ICMP.

Authorized use only. Load testing or DoS simulation is done only against systems you own or have written permission to test, preferably in an isolated lab. Most DDoS protection providers require advance notice before a customer tests their service, because a test looks the same as an attack.

## Core concepts

### Definition

A *denial of service* is any action that prevents authorized access to a resource or delays time-critical operations beyond an acceptable limit. In network security the term usually means a deliberate attack that does this by overloading or crashing a target. Three things separate it from other availability problems:

- **Intent.** A flash crowd after a product launch exhausts the same resources, but nobody planned it. The mitigations overlap, which is why DoS defense and capacity planning are often the same team's work.
- **Asymmetry.** The attacker spends less than the defender. One request costs the attacker a few bytes, while the defender spends memory, CPU or bandwidth to handle it. Every DoS technique is a way to increase that ratio.
- **No goal beyond unavailability.** Sometimes DoS is the end goal (extortion, protest, sabotage). Sometimes it is a smokescreen that keeps the security team busy during an intrusion elsewhere.

### Analogy

Think of a restaurant with 20 tables, two waiters and one phone line. You can stop it serving customers without breaking anything:

- Send 200 people to stand in the doorway (volumetric, the entrance is full).
- Book all 20 tables by phone and never show up (state exhaustion, the reservation book is full).
- Order the most complicated dish on the menu again and again (application layer, the kitchen is the bottleneck).
- Hand the waiter an order form written so that the kitchen staff faint when they read it (crash, a malformed input).

The analogy breaks in two places. A restaurant can see who is at the door, but on the internet a packet's source address can be forged. And a restaurant cannot ask thousands of unrelated businesses to send their deliveries to the victim, which is what reflection attacks do.

### The resource that runs out

Every DoS attack targets a specific bottleneck. Naming the bottleneck is the first step of both analysis and defense.

| Bottleneck | Example attack | Unit of measure | Where it is mitigated |
| --- | --- | --- | --- |
| Link bandwidth | UDP flood, reflection and amplification | bits per second (bps) | Upstream: ISP, scrubbing center, CDN |
| Packet processing | Small-packet floods against routers and firewalls | packets per second (pps) | Hardware capacity, upstream filtering |
| Connection state | [SYN flood](syn-flood.md), connection table exhaustion on firewalls | half-open or open connections | SYN cookies, stateless filtering in front of stateful devices |
| Application resources | HTTP floods, expensive search queries, TLS handshakes | requests per second (rps) | WAF, rate limiting, caching, CDN |
| Software correctness | [Ping of death](ping-of-death.md), malformed packets | one packet is enough | Patching, input validation |

The table is a guide, not a strict classification. An [ICMP flood](icmp-flood.md) can saturate bandwidth or packet processing depending on packet size.

### Three classes of attack

Denial of service techniques are usually grouped into three classes by the layer they target. This note treats each one from the defender's side: what the traffic looks like, how to detect it, and how to absorb or filter it. The individual techniques the user asked about have their own notes: [SYN flood](syn-flood.md), [ICMP flood](icmp-flood.md), [ping of death](ping-of-death.md), and [distributed denial of service](distributed-denial-of-service.md).

**Volumetric attacks** try to fill the link. The defender cannot filter a full pipe from inside, because the traffic has already consumed the link by the time it arrives, so mitigation happens upstream: at the ISP, in a scrubbing center, or behind a content delivery network. The main amplifier is *reflection*: the attacker sends small requests with the victim's address as the forged source to many public servers (DNS, NTP, memcached, CLDAP), and those servers send much larger replies to the victim. The *bandwidth amplification factor* (BAF) measures the gain. From the US-CERT advisory TA14-017A (last revised 2019), DNS gives a BAF of 28 to 54, NTP 556, and memcached 10,000 to 51,000, which is why memcached reflection produced some of the largest recorded attacks. The defense against being an unwitting reflector is to not run these services open to the internet; the defense against being a victim is upstream capacity and scrubbing.

**Protocol and state-exhaustion attacks** target a finite table rather than bandwidth. A [SYN flood](syn-flood.md) fills the connection backlog with half-open connections. These are cheaper for the attacker than volumetric attacks because each small packet ties up a relatively expensive resource on the target. Defenses work by not allocating state until a handshake is proven genuine (SYN cookies) or by placing a stateless device in front that validates connections.

**Application-layer attacks** send requests that are individually legal but expensive to serve: repeated searches, large report generation, login attempts that trigger password hashing, or many TLS handshakes. They are hard to distinguish from real users and low in volume, so they often pass network defenses and must be handled at the application: caching, rate limiting per client, work factors (proof-of-work or CAPTCHAs) on expensive endpoints, and a web application firewall.

### Why distribution changes everything

A single-source attack can be blocked by filtering one address. A [distributed denial of service](distributed-denial-of-service.md) uses thousands of sources (a botnet of compromised devices, or reflectors), so there is no single address to block and the combined bandwidth can exceed any single victim's capacity. Distribution also makes the traffic resemble a flash crowd, which is why volumetric DDoS defense is a specialist, capacity-heavy service rather than something a single firewall can do.

## Worked example

This uses the [network security lab](../../foundations/network-security-lab/README.md) to show the two halves of DoS defense that a host operator controls: input validation against malformed packets, and rate limiting against floods. It deliberately does not generate attack traffic at scale; it demonstrates the defensive mechanisms.

**Malformed-packet resistance.** The IPv4 header limits a packet, including headers, to 65,535 bytes. The historic [ping of death](ping-of-death.md) worked by fragmenting an oversized packet so the victim reassembled something larger than this limit and overflowed a buffer. Modern stacks reject it. In the lab, the largest legal echo request succeeds and one byte more is refused by the sender's own stack (tested on kernel 6.8, 2026-10):

```text
# ping -s 65507 (65,535-byte IP packet): succeeds
65515 bytes from 192.0.2.1: icmp_seq=1 ttl=64 time=0.383 ms
# ping -s 65508 (one byte over the limit): refused before it is even sent
ping: local error: message too long, mtu=1500
```

The defense here is a correct, patched network stack: the oversize condition is handled, not crashed on.

**Rate limiting a flood.** A firewall can cap how fast a given kind of packet is accepted, so a flood degrades to a trickle instead of overwhelming the host. The lab firewall limits echo requests to 5 per second with a burst of 10 (see [firewall rule design](../../traffic-filtering/firewall-rule-design/README.md) for why the rule must sit before the connection-state rule). Sending 50 requests at 20 per second, 22 arrive and 28 are dropped:

```text
50 packets transmitted, 22 received, 56% packet loss
```

Rate limiting protects the host's own resources. It does not protect the link, because the packets still arrived to be counted. That is the dividing line: a host can defend its state and CPU, but only upstream capacity defends bandwidth.

## Trade offs and when to use it

Defenses, and their costs:

- **Upstream scrubbing / CDN / anycast.** The only answer to large volumetric attacks. Cost: money, a dependency on a provider, and TLS or routing changes so the provider can see and absorb the traffic.
- **SYN cookies and stateless front-ends.** Cheap and effective against state exhaustion, with minor loss of some TCP options under attack.
- **Rate limiting.** Protects host resources, but a limit set too low harms legitimate bursts and a limit too high lets attack traffic through. It must be tuned per service.
- **Application controls (caching, work factors, WAF).** Necessary for application-layer attacks that network defenses never see. Cost: complexity and some user friction.

When network-level defense is the wrong focus: a low-and-slow application attack sends too little traffic to trip any volume threshold, so chasing it with bandwidth tools wastes effort. Match the defense to the bottleneck being attacked.

## Common mistakes

- **Trying to filter a volumetric attack on the target.** By the time traffic reaches the target, the link is already full. Fix: mitigate upstream.
- **Running open reflectors.** Internet-facing DNS resolvers, NTP, memcached or CLDAP that answer anyone turn you into a weapon against others. Fix: close them to the public, disable amplifying commands, apply BCP 38 source validation.
- **Stateful devices with no SYN protection in front.** A firewall's own state table becomes the target. Fix: SYN cookies, or a stateless validator in front.
- **Confusing a flash crowd with an attack.** The mitigations overlap, but blocking real users during a launch is its own outage. Fix: capacity planning and graceful degradation, not only blocking.
- **No runbook.** DoS is a time-pressured event; improvising wastes the first critical minutes. Fix: a prepared plan, provider contacts and practiced escalation. See [network incident response](../../operations-and-assurance/network-incident-response.md).

## Practice

1. Why can a host rate-limit a ping flood but not defend its own link bandwidth against a volumetric flood?
2. What is a bandwidth amplification factor, and why does memcached's make it so dangerous?
3. Which resource does a SYN flood exhaust, and what defense avoids allocating it?
4. Why is an application-layer DoS often invisible to network volume thresholds?
5. How does distribution defeat the simple defense of blocking the source address?

### Answers

1. Rate limiting drops packets after they arrive, protecting CPU and state, but the packets have already traversed and can fill the link; only upstream capacity defends bandwidth.
2. The ratio of response bytes to request bytes from a reflector. Memcached can return 10,000 to 51,000 times the request size, so a small amount of attacker bandwidth produces an enormous flood at the victim.
3. The connection backlog (half-open connection state). SYN cookies encode the needed state in the sequence number instead of allocating a table entry, so no state is held until the handshake completes.
4. It sends few, individually legal requests that are expensive to serve, so volume-based thresholds never trip; the cost is on the application, not the network.
5. With thousands of sources there is no single address to block, the combined bandwidth can exceed the victim's capacity, and the traffic resembles legitimate users from many places.

## Further reading

- US-CERT (CISA) Alert TA14-017A, UDP-Based Amplification Attacks, with the amplification-factor table (last revised 2019): https://www.cisa.gov/news-events/alerts/2014/01/17/udp-based-amplification-attacks
- RFC 4987, TCP SYN Flooding Attacks and Common Mitigations (2007): https://www.rfc-editor.org/rfc/rfc4987
- BCP 38 / RFC 2827, Network Ingress Filtering (2000), the source-validation defense against reflection: https://www.rfc-editor.org/rfc/rfc2827
- MITRE ATT&CK, Network Denial of Service (T1498) and Endpoint Denial of Service (T1499): https://attack.mitre.org/techniques/T1498/
- CISA, Understanding and Responding to Distributed Denial-of-Service Attacks (joint guidance): https://www.cisa.gov/