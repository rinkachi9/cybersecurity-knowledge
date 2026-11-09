# BGP security

## Summary

The Border Gateway Protocol (BGP) is how the independent networks that make up the internet tell each other which blocks of addresses they can reach. It runs on trust: a network announces "I can reach these prefixes", and others believe it. That trust is abused by *prefix hijacking* (announcing address space you do not own, to attract and intercept or black-hole its traffic) and *route leaks* (propagating routes in a direction that policy forbids, causing traffic to detour through the wrong network). The defenses are Resource Public Key Infrastructure (RPKI) with Route Origin Validation, which checks that the originating network is authorized, and emerging path validation (ASPA) plus prefix filtering and the MANRS norms. BGP security matters to everyone because a hijack far away can redirect your traffic, and because misconfiguration causes as many incidents as attacks.

## Prerequisites

- [Protocol design weaknesses](../foundations/protocol-design-weaknesses.md): transitive trust in announcements.
- [Network threat model](../foundations/network-threat-model.md): off-path to on-path via routing.
- Basic routing and the idea of an Autonomous System (AS).

## Core concepts

### Definition

*BGP* (RFC 4271) is the routing protocol between *Autonomous Systems* (ASes), the independently operated networks (ISPs, large organizations) each identified by an AS number. BGP announcements say which IP prefixes an AS originates and the AS path a route has traversed. There is no built-in check that an announcement is truthful, so a false announcement propagates and can redirect traffic globally.

### Analogy

Imagine a world postal system where each country announces to its neighbors "mail for these postal codes, hand it to me". Normally France handles French codes. A *prefix hijack* is a country announcing "I handle Swiss codes too", so neighbors start handing it Swiss mail, which it can read, drop, or forward on. A *route leak* is a small courier that was only supposed to carry mail between two neighbors suddenly telling everyone "I can reach the whole world", so global mail floods through a courier that cannot handle it and should never have offered.

The analogy holds well; it breaks only in that BGP reconverges in seconds and a hijack can be global before humans notice, and that much of the harm is accidental misconfiguration, not malice.

### Prefix hijacking

An AS originates a prefix it does not own. Variants:

- *Exact-prefix hijack*: announcing the same prefix as the owner; the shorter AS path or closer location wins for part of the internet.
- *More-specific hijack*: announcing a longer (more specific) prefix (for example a `/24` inside the owner's `/16`); longest-prefix-match routing means the hijacker wins everywhere, which is why more-specific hijacks are so effective.

The purpose can be interception (become on-path, often combined with forwarding so the victim notices nothing but latency), black-holing (traffic disappears, a denial of service), or spam and fraud from address space that is not traceable to the attacker. Famous incidents include the 2008 YouTube outage (Pakistan Telecom announced a more-specific YouTube prefix) and repeated cryptocurrency thefts via BGP interception of specific services.

### Route leaks

A route learned from one peer is announced to another in violation of the intended commercial relationship (the "valley-free" rule: a network should not provide transit between two of its providers or peers). The result is traffic detouring through a network that should not carry it, causing congestion, latency, or exposure. Most leaks are accidental misconfiguration, but the effect, traffic through an unexpected path, is the same as an attack. RFC 7908 classifies the leak types.

### Defense: RPKI and Route Origin Validation

*Resource Public Key Infrastructure* (RPKI, RFC 6480) lets address holders publish cryptographically signed *Route Origin Authorizations* (ROAs) stating "AS X is authorized to originate prefix P, up to length L". Routers performing *Route Origin Validation* (ROV, RFC 6811) check each announcement against the ROAs and mark it Valid, Invalid or NotFound, dropping Invalids. ROV stops hijacks where the origin AS is wrong, including most more-specific hijacks, because the more-specific announcement from an unauthorized AS is Invalid.

ROV's limit: it validates only the *origin*, not the whole *path*. An attacker who forges a path that keeps the real origin AS at the end can still deceive ROV. This gap is being closed by:

- *ASPA* (Autonomous System Provider Authorization): signed statements of an AS's legitimate providers, enabling path validation and route-leak detection. As of 2026-10 the ASPA specifications are late-stage IETF drafts moving toward publication, with early deployment; they are not yet a finalized RFC.
- *BGPsec* (RFC 8205): cryptographic path signing, specified but almost undeployed due to cost.

### Defense: prefix filtering and MANRS

Independently of RPKI, networks filter what they accept from customers and peers:

- Accept from a customer only the prefixes the customer is registered (in an IRR, Internet Routing Registry) to originate.
- Apply maximum-prefix limits and reject bogons (unallocated or private prefixes).

*MANRS* (Mutually Agreed Norms for Routing Security) bundles these into four actions: filtering, anti-spoofing (BCP 38), coordination, and global validation (publish ROAs, do ROV). It is the practical checklist most operators follow.

## Worked example

This is a conceptual walkthrough; running BGP needs a router emulation lab (such as Containerlab or GNS3), not the namespace lab, so it is marked not tested here.

A bank owns `203.0.113.0/24` and its ISP (AS 64500) originates it, with a ROA authorizing AS 64500 for that prefix up to `/24`.

1. **Hijack attempt.** A malicious AS 64666 announces `203.0.113.128/25`, a more-specific prefix. Without RPKI, longest-prefix match sends all traffic for those addresses through AS 64666, which intercepts the bank's customers.
2. **With ROV.** The ROA says only AS 64500 may originate within `203.0.113.0/24` up to `/24`. The `/25` from AS 64666 is longer than the ROA's maximum length and from the wrong origin, so ROV marks it Invalid and validating networks drop it. The hijack fails across the part of the internet that does ROV.
3. **Residual risk.** A network not doing ROV still accepts the hijack, which is why coverage must be widespread; and a path-forgery attack keeping AS 64500 as the apparent origin would pass ROV, needing ASPA/BGPsec to catch. This is why BGP security is described as a work in progress with partial but rising coverage (ROV adoption has grown substantially by 2026, path validation less so).

The lesson: publishing ROAs protects your prefixes from origin hijacks *to the extent others validate*, so BGP security is inherently collective.

## Trade offs and when to use it

- **Publishing ROAs** is low-effort, high-value, and protects your address space from origin hijacks wherever ROV is done. Do it.
- **Doing ROV** protects your own traffic and users from accepting hijacked routes; the cost is RPKI validator infrastructure and the small risk of dropping legitimately misconfigured routes.
- **Prefix filtering from IRR data** is effective but depends on registry accuracy, which varies by region.
- **BGPsec** offers full path security but is not practically deployable at scale today; ASPA is the pragmatic near-term path-validation step.

Most organizations are not ISPs and influence BGP security in two ways: ensure their provider does MANRS and ROV, and publish ROAs for any address space they own.

## Common mistakes

- **Not publishing ROAs for owned prefixes.** Leaves them hijackable with no validation possible. Fix: create ROAs via your RIR.
- **Assuming ROV protects the path.** It validates only the origin. Fix: understand the gap; adopt ASPA as it matures.
- **No maximum-prefix limits or bogon filtering.** A leak or fat-finger floods your table. Fix: apply limits and bogon filters on all sessions.
- **Treating leaks as purely malicious.** Most are misconfiguration; the fix (filtering, ASPA) is the same. Fix: filter regardless of intent.
- **Exposing BGP sessions to injection.** Long-lived router sessions on predictable ports. Fix: TCP-AO and ACLs limiting peers (see [TCP attacks](tcp-attacks.md)).

## Practice

1. What is the difference between a prefix hijack and a route leak?
2. Why is a more-specific prefix hijack more effective than an exact-prefix one?
3. What does a ROA assert, and what does Route Origin Validation do with it?
4. What is the main limitation of ROV, and what is being developed to address it?
5. Why is BGP security inherently a collective effort?

### Answers

1. A hijack announces address space the AS does not own, to attract its traffic; a route leak propagates a legitimate route in a direction policy forbids, detouring traffic through a network that should not carry it.
2. Longest-prefix-match routing always prefers the more specific prefix, so a more-specific hijack wins across the whole internet, whereas an exact-prefix hijack competes with the real announcement and wins only part of it.
3. A ROA asserts that a specific AS is authorized to originate a prefix up to a maximum length; ROV checks each announcement against ROAs and marks it Valid, Invalid or NotFound, dropping Invalids.
4. ROV validates only the origin AS, not the AS path, so a forged path keeping the real origin can still deceive it; ASPA (and BGPsec) add path validation.
5. Publishing ROAs only protects your prefixes where others perform ROV, and your traffic is only protected if you perform ROV, so the benefit depends on widespread mutual adoption.

## Further reading

- RFC 4271, A Border Gateway Protocol 4 (BGP-4): https://www.rfc-editor.org/rfc/rfc4271
- NIST SP 800-189, Resilient Interdomain Traffic Exchange / BGP Security and Resilience (Rev. 1 initial public draft, 2025): https://csrc.nist.gov/pubs/sp/800/189/r1/ipd
- RFC 6811, BGP Prefix Origin Validation, and RFC 6480, RPKI: https://www.rfc-editor.org/rfc/rfc6811
- RFC 7908, Problem Definition and Classification of BGP Route Leaks: https://www.rfc-editor.org/rfc/rfc7908
- MANRS, Mutually Agreed Norms for Routing Security: https://www.manrs.org/
