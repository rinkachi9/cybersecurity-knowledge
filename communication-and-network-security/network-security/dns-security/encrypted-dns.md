# Encrypted DNS

## Summary

Plain DNS queries travel in cleartext, so anyone on the path (an ISP, a Wi-Fi operator, an on-path attacker) can see every name a device looks up and can tamper with the answers. Encrypted DNS hides the query between the client and the resolver using TLS: DNS over TLS (DoT), DNS over HTTPS (DoH) and DNS over QUIC (DoQ). It protects user privacy and blocks on-path tampering of the first hop. For enterprises it creates a real tension: the same encryption that protects users also hides DNS from the security monitoring and [protective DNS](protective-dns.md) controls that rely on seeing lookups, and DoH in particular can be used by malware and users to bypass corporate resolvers. The resolution is to run your own encrypted resolver and steer clients to it, rather than blocking encryption outright.

## Prerequisites

- [DNS threat landscape](dns-threat-landscape.md): what the cleartext first hop exposes.
- [TLS in network security](../secure-transport/tls-in-network-security.md): the transport underneath.
- [DNSSEC](dnssec.md): the complementary authentication layer.

## Core concepts

### Definition

*Encrypted DNS* wraps the client-to-resolver query in an encrypted, authenticated channel. The main variants:

- *DNS over TLS (DoT)*, RFC 7858: DNS inside a TLS session on a dedicated port, 853.
- *DNS over HTTPS (DoH)*, RFC 8484: DNS inside HTTPS on port 443, indistinguishable from ordinary web traffic.
- *DNS over QUIC (DoQ)*, RFC 9250: DNS over QUIC (which is itself TLS over UDP), on port 853.

All encrypt the *transport* between stub and resolver. They are orthogonal to DNSSEC, which authenticates the *records* end to end.

### Analogy

Plain DNS is asking a librarian for a book title out loud in a crowded room: everyone hears what you are researching, and a prankster could shout a wrong shelf number before the librarian answers. Encrypted DNS is a private, sealed tube to one trusted librarian: nobody in the room hears your request or can slip you a false answer. The catch for an organization is that the library's own security desk also relied on overhearing requests to notice someone asking for dangerous material, and the private tube silences that too.

The analogy breaks in that DoH's tube is deliberately shaped to look like every other tube in the building (port 443), so the organization cannot even tell a DNS tube from a web tube, which is the core of the enterprise problem.

### DoT vs DoH vs DoQ

| | Port | Visibility to network | Blockable | Typical use |
| --- | --- | --- | --- | --- |
| DoT | 853 (dedicated) | Identifiable by port | Yes, block/allow port 853 | Enterprise-friendly: can be steered and monitored by policy |
| DoH | 443 (shared with HTTPS) | Hidden among web traffic | Hard without breaking HTTPS | Browser default to public resolvers; hard for networks to see |
| DoQ | 853 (over UDP/QUIC) | Identifiable by port, newer | Yes | Lower latency; growing support |

The practical difference is visibility. DoT uses a dedicated port, so an organization can see it, allow it to the corporate resolver and block it elsewhere. DoH rides on 443 alongside all web traffic, so it cannot be distinguished or blocked without inspecting or breaking HTTPS, which is why DoH is the one that undermines network DNS controls.

### The enterprise tension

Encrypted DNS is clearly good for user privacy on untrusted networks. Inside an enterprise it collides with legitimate controls:

- [Protective DNS](protective-dns.md), DNS logging and threat detection all rely on seeing and controlling lookups at the corporate resolver. If a client uses DoH to a public resolver, those controls are bypassed.
- Malware uses DoH deliberately to evade DNS-based blocking and to resolve C2 domains invisibly (MITRE ATT&CK, DNS over HTTPS can hide Application Layer Protocol and Dynamic Resolution).
- Split-horizon DNS (internal names) breaks if the client asks a public resolver.

### Resolving it: run your own encrypted resolver

The sound approach is not to ban encryption but to provide it:

- Stand up a corporate resolver that speaks DoT/DoH, so client-to-resolver traffic is encrypted *and* still passes through the control and logging point.
- Steer clients to it: configure the OS/browser encrypted-DNS settings to the corporate resolver, or use Discovery of Designated Resolvers (DDR) and network-provisioned resolver settings.
- Detect and block DoH to *unauthorized* public resolvers (known endpoint lists, canary domains like `use-application-dns.net` that signal browsers to disable auto-DoH), while allowing it to the corporate resolver.
- Keep DNSSEC validation on the resolver so answers are authenticated as well as private.

## Worked example

A laptop on café Wi-Fi versus the same laptop on the corporate network:

1. **On café Wi-Fi.** Plain DNS would let the café (or an on-path attacker) see every site the user visits and forge answers. With DoH to a trusted resolver, the café sees only an encrypted 443 flow; names and answers are private and tamper-proof on that hop. This is encrypted DNS working as intended.
2. **On the corporate network, misconfigured.** The same laptop keeps using DoH to a public resolver. The corporate protective-DNS block list and logging never see the lookups, so a request to a known-malicious domain is neither blocked nor recorded, and internal names fail to resolve. Encrypted DNS has bypassed the controls.
3. **On the corporate network, done right.** The laptop is steered to the corporate DoT/DoH resolver. The query is encrypted to that resolver (private from other hosts on the LAN), but the resolver still enforces the block list, logs the lookup for detection, validates DNSSEC, and serves internal names. Privacy and control coexist.

The difference between cases 2 and 3 is configuration and steering, not whether encryption is used.

## Trade offs and when to use it

- **Privacy vs visibility.** Encrypted DNS to an external resolver maximizes user privacy but removes enterprise visibility; to an internal resolver it keeps both. Choose based on whether the device is enterprise-managed.
- **DoT vs DoH for an organization.** DoT is easier to govern (dedicated port, steerable, monitorable); DoH is harder to see but is what browsers default to. Provide a corporate DoH/DoT resolver and manage the clients.
- **Blocking DoH is fragile.** You cannot cleanly block DoH without inspecting HTTPS; rely on steering and endpoint policy, plus blocking known public DoH endpoints, rather than a port block.
- **Trust in the resolver operator.** Encrypted DNS moves trust to whoever runs the resolver; a public resolver sees all your lookups. For sensitive environments, run your own.

## Common mistakes

- **Trying to block all encrypted DNS at the firewall.** DoH on 443 cannot be cleanly blocked. Fix: provide and steer to a corporate encrypted resolver; block known public DoH endpoints.
- **Ignoring browser auto-DoH.** Browsers may silently switch managed devices to public DoH. Fix: use the canary domain and enterprise policies to control it.
- **Confusing encrypted DNS with DNSSEC.** One gives privacy of the hop, the other authenticity of records; you want both. Fix: run DNSSEC validation on the encrypted resolver.
- **Losing protective DNS to DoH bypass.** Fix: ensure all managed clients resolve through the controlled resolver.
- **Blindly trusting a public resolver with all lookups.** Fix: for sensitive use, operate your own resolver.

## Practice

1. What does encrypted DNS protect, and how does that differ from what DNSSEC protects?
2. Why is DoH harder for an organization to see or block than DoT?
3. Describe the enterprise tension encrypted DNS creates.
4. What is the recommended way to get the benefits of encrypted DNS without losing enterprise DNS controls?
5. Why is blocking DoH at the firewall an unreliable strategy?

### Answers

1. Encrypted DNS protects the confidentiality (and tamper-resistance) of the query between client and resolver; DNSSEC authenticates the integrity and origin of the records end to end. They are complementary.
2. DoH runs on port 443 mixed with all other HTTPS traffic, so it is indistinguishable without breaking TLS, whereas DoT uses the dedicated port 853 that can be identified and steered.
3. The encryption that protects user privacy also hides DNS from the corporate resolver's logging and protective-DNS controls, and lets malware and users bypass DNS-based blocking.
4. Run a corporate resolver that speaks DoT/DoH and steer managed clients to it, so queries are encrypted to the resolver while still passing through logging, filtering and DNSSEC validation.
5. DoH cannot be distinguished from ordinary HTTPS without inspecting or breaking TLS, so a port block does not catch it; steering clients and blocking known public DoH endpoints is needed instead.

## Further reading

- RFC 7858 (DoT), RFC 8484 (DoH), RFC 9250 (DoQ): https://www.rfc-editor.org/rfc/rfc8484
- NIST SP 800-81r3, Secure DNS Deployment Guide (2026), on recursive-resolver confidentiality and query minimization: https://doi.org/10.6028/NIST.SP.800-81r3
- RFC 9462/9463, Discovery of Designated Resolvers (DDR) and network-provisioned resolvers: https://www.rfc-editor.org/rfc/rfc9462
- NSA/CISA, Selecting and Hardening Remote Access VPNs and Protective DNS guidance for the enterprise control angle.
