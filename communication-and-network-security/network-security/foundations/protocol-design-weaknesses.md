# Protocol design weaknesses

## Summary

The core internet protocols (IP, ARP, DHCP, DNS, BGP, ICMP) were designed in the 1970s and 1980s for a small network of cooperating institutions. They assume that every participant tells the truth about who it is and what it knows. None of them authenticates the sender by default. Most classic network attacks are not bugs in implementations but consequences of this design: forging a source address, answering a question that was not addressed to you, or announcing a route you do not own. Security was added later as optional layers (IPsec, DNSSEC, RPKI, TLS), so the defender's job is to know which trust assumption a protocol makes and which add-on or control closes it.

## Prerequisites

- [Network threat model](network-threat-model.md): attacker positions referred to throughout.
- Basic knowledge of the TCP/IP layers.

## Core concepts

### Definition

A *protocol design weakness* is a property of the specification itself that lets a participant cause harm while following the protocol's message formats. It differs from an implementation vulnerability (for example a buffer overflow in one vendor's DNS server), which can be fixed with a patch. A design weakness can only be mitigated with extensions, configuration or controls around the protocol.

### Analogy

Think of a village notice board where anyone can pin a note signed with any name. It works while everyone in the village is honest. When strangers arrive, nothing on the board tells you which notes are genuine. Adding signatures later (a seal from the town hall) helps only if readers check them, and old readers who ignore seals still believe the forged notes.

The analogy breaks because on the network the "readers" are software that runs automatically, so a forged note can be acted on in microseconds and at scale.

### Recurring design patterns that attackers use

| Pattern | Meaning | Protocols affected | Typical attack |
| --- | --- | --- | --- |
| Unauthenticated source | The sender writes its own "from" field | IP, UDP, Ethernet | Source address spoofing, reflection |
| Unsolicited answers accepted | A host caches an answer it never asked for, or the first answer wins | ARP, NDP, LLMNR, NBT-NS, old DNS resolvers | ARP spoofing, name resolution poisoning |
| Broadcast discovery | A client asks "who can help?" and trusts whoever replies | DHCP, LLMNR, mDNS, WPAD, SSDP | Rogue DHCP, WPAD hijacking |
| Transitive trust in announcements | A router believes what neighbors say about third parties | BGP, RIP, OSPF without authentication | Prefix hijacking, route leaks |
| Cleartext by default | Content and credentials travel unencrypted | Telnet, FTP, HTTP, SNMPv1/v2c, POP3, IMAP, LDAP | Sniffing credentials |
| Predictable fields as authentication | A guessable number is the only proof that a reply belongs to a request | TCP sequence numbers (historically), DNS transaction ID | Blind TCP injection, DNS cache poisoning |
| Amplification | A small request triggers a large response to an unverified address | DNS, NTP, memcached, SSDP, CLDAP | Reflection floods |
| Negotiation without integrity | Peers agree on the strongest common option, but an attacker can alter the offer | Old TLS, SSH version exchange, STARTTLS | Downgrade and stripping attacks |

### Why the internet was built this way

The ARPANET and early internet connected a handful of universities and research labs whose operators knew each other. In that setting, authenticating every packet would have added cost for a threat that did not exist: there were no anonymous strangers on the network. The design optimized for what mattered then, which was getting heterogeneous machines to interoperate and survive link failures. Robustness and the "end-to-end principle" (keep the network simple, put intelligence in the endpoints) were the goals, not defense against a hostile participant.

The weaknesses are therefore not oversights by careless engineers; they are the correct trade-offs for a cooperative network, carried unchanged into a hostile one. This framing matters because it explains why the fixes are layered on top (IPsec, DNSSEC, RPKI, TLS, 802.1X) rather than built in, and why deployment is slow: the insecure version still works and interoperates, so there is little forcing function to adopt the secure one.

### How the fixes map to the weaknesses

| Weakness | Add-on defense | What it adds | Deployment reality (checked 2026-10) |
| --- | --- | --- | --- |
| Unauthenticated IP source | BCP 38 ingress filtering, uRPF | Drops spoofed source addresses near the source | Partial; spoofing is still possible from many networks |
| ARP / NDP spoofing | Dynamic ARP Inspection, RA Guard, DHCP snooping | Switch verifies bindings | Common in managed enterprise switches, absent on flat networks |
| DNS forgery | DNSSEC | Signs DNS records so forgeries are detected | Signing and especially validation remain a minority of traffic |
| DNS confidentiality | DoT, DoH, DoQ | Encrypts the client-to-resolver query | Widely available, creates enterprise visibility tension |
| BGP hijack / route leak | RPKI with ROA and ROV, ASPA | Validates the origin and path of routes | ROV adoption rising; path validation (ASPA) still emerging |
| Cleartext protocols | TLS, SSH, replacing Telnet/FTP/SNMPv1 | Confidentiality, integrity, authentication | Mature; legacy protocols persist in old and OT networks |
| Predictable fields | Randomized TCP ISN, DNS source-port and 0x20 randomization | Makes blind injection impractical | Standard in modern stacks |
| Amplification | Closing open reflectors, response rate limiting | Removes the amplifier | Ongoing; open reflectors still exist |
| Downgrade | TLS 1.3, downgrade-protection signaling, HSTS, MTA-STS | Binds the negotiation to its integrity | Growing; depends on removing old fallbacks |

The pattern is consistent: the secure layer exists, works, and is specified, but the insecure default remains for compatibility, so the defender's job is to turn the secure option on, verify it is actually used, and detect fallback to the old behavior.

## Worked example

Trace one request, `http://intranet.example.com`, and name the design weakness exploited at each step an attacker could take:

1. The client asks its resolver for `intranet.example.com`. Without DNSSEC, a forged answer (unsolicited-answer and predictable-field weaknesses) can point the name at an attacker's address. Fix: DNSSEC validation, or at least a trusted resolver path.
2. The client sends the request to the returned address. On the local network, an attacker can answer ARP for the gateway (unsolicited-answer weakness) and become on-path. Fix: Dynamic ARP Inspection, or TLS so the content is still protected.
3. The request is HTTP, so it is cleartext (cleartext-by-default weakness). The on-path attacker reads the session cookie. Fix: HTTPS with HSTS.
4. If the site offered HTTPS but the client first tried HTTP, the attacker can keep it on HTTP (downgrade weakness). Fix: HSTS preloading so the browser never tries HTTP.

Each mitigation closes exactly one weakness; none closes all of them, which is why defense in depth and "assume a hostile network" are the governing principles.

## Trade offs and when to use it

- The add-on defenses cost deployment effort and interoperability risk, and some (DNSSEC, RPKI) require coordination beyond one organization, which is why adoption lags.
- A defender rarely gets to replace a protocol; the practical work is enabling the secure variant, disabling the insecure fallback, and detecting when something speaks the old way.
- For legacy and OT environments where the secure variant does not exist, the answer is compensating network controls (segmentation, monitoring), because the protocol itself cannot be fixed. See [OT network security](../ot-and-iot/ot-network-security.md).

## Common mistakes

- **Assuming a protocol authenticates its peers because it "works".** Working and authenticating are unrelated. Fix: check what each protocol actually verifies.
- **Enabling the secure variant but leaving the insecure fallback.** Attackers force the fallback. Fix: disable old versions and detect downgrades.
- **Blaming implementations for design weaknesses.** Patching one vendor does not fix a design flaw shared by all. Fix: deploy the protocol-level add-on.
- **Treating encryption as a cure-all.** It closes confidentiality and (with integrity) tampering, but not spoofing, flooding or metadata exposure. Fix: match the control to the weakness.

## Practice

1. Why did the early internet protocols omit authentication, and why is that not simply a mistake?
2. Give the add-on defense for each: ARP spoofing, DNS forgery, BGP prefix hijack, cleartext credentials.
3. Why does enabling a secure protocol variant not help if the insecure version is still accepted?
4. Which weakness does encryption not address at all?
5. Why is deployment of DNSSEC and RPKI slower than deployment of TLS?

### Answers

1. They connected a small set of mutually trusting institutions where no anonymous attacker existed, so authentication would have added cost against a non-existent threat; it was the right trade-off for that network, carried into a hostile one.
2. ARP spoofing: Dynamic ARP Inspection with DHCP snooping. DNS forgery: DNSSEC. BGP hijack: RPKI with route origin validation (and ASPA for path). Cleartext credentials: TLS or SSH and replacing the legacy protocol.
3. An attacker can force the negotiation down to the insecure version (a downgrade attack), so the secure option is only effective once the insecure one is refused.
4. Spoofing of source addresses, flooding, and exposure of metadata (who talks to whom, when, how much); encryption protects content and, with integrity, tampering.
5. TLS is deployed by each server and client independently and benefits them directly; DNSSEC and RPKI require coordination across zone operators and networks, and the benefit is partly collective, so there is less individual forcing function.

## Further reading

- RFC 3552, Guidelines for Writing RFC Text on Security Considerations (2003): the IETF's own account of the threat model and common weaknesses: https://www.rfc-editor.org/rfc/rfc3552
- Saltzer, J., Reed, D., Clark, D., "End-to-End Arguments in System Design" (1984): the design philosophy behind the simple-network choice.
- Bellovin, S., "Security Problems in the TCP/IP Protocol Suite" (1989): the classic early catalogue of these weaknesses.
- NIST SP 800-189, Border Gateway Protocol Security and Resilience (Rev. 1 initial public draft, 2025), for the routing add-ons: https://csrc.nist.gov/pubs/sp/800/189/r1/ipd