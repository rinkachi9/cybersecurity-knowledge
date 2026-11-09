# SASE and SSE

## Summary

Secure Access Service Edge (SASE) and Security Service Edge (SSE) are architectures that deliver network security from the cloud rather than from appliances in a data center. As users, applications and data moved out of the office (remote work, SaaS, cloud), backhauling all traffic to a central firewall stopped making sense. SASE combines networking (SD-WAN) and security (secure web gateway, cloud access security broker, firewall-as-a-service, and [zero-trust network access](zero-trust-networking.md)) into one cloud-delivered service close to the user. SSE is the security half of SASE without the networking. These are consolidation and delivery models, not new security mechanisms: they repackage controls this area already covers and move the enforcement point to the cloud edge.

## Prerequisites

- [Zero-trust networking](zero-trust-networking.md) and [VPNs](../secure-transport/vpns.md): ZTNA is a core SASE component.
- [Proxies and secure web gateways](../traffic-filtering/proxies-and-secure-web-gateways.md) and [network security controls](../foundations/network-security-controls.md).
- [SD-WAN security](../cloud-and-modern-networks/sd-wan-security.md): the networking half.

## Core concepts

### Definition

*SASE* (coined by Gartner in 2019) is a cloud-delivered architecture that converges wide-area networking (SD-WAN) and a set of network security services at points of presence near the user. *SSE* is the security-only subset: the same security services without the SD-WAN networking component. Both deliver enforcement from the cloud edge rather than from on-premises appliances.

### Analogy

The old model is a company where every letter, no matter where it is sent from, must first travel to the head-office mailroom to be screened, then back out again (backhauling to a central firewall). SASE is replacing that with screening stations in every city, so a letter is checked at the nearest station and sent straight on. The screening rules are the same; the stations are everywhere and close to the sender, so mail is faster and the head office is no longer a bottleneck.

The analogy holds well; it breaks in that the "screening stations" are run by a cloud provider, so the model trades on-premises control for a dependency on that provider seeing the traffic.

### The components

SASE/SSE bundles controls covered elsewhere in this area, delivered from the cloud:

| Component | What it does | Related note |
| --- | --- | --- |
| Secure Web Gateway (SWG) | Filters and inspects web traffic, enforces policy | [Proxies and secure web gateways](../traffic-filtering/proxies-and-secure-web-gateways.md) |
| Cloud Access Security Broker (CASB) | Visibility and control over SaaS use | Cloud security |
| Zero-Trust Network Access (ZTNA) | Per-application access, VPN replacement | [Zero-trust networking](zero-trust-networking.md) |
| Firewall-as-a-Service (FWaaS) | Cloud-delivered firewall | [Firewalls](../traffic-filtering/firewalls.md) |
| Data Loss Prevention (DLP) | Stops sensitive data leaving | - |
| SD-WAN (SASE only) | Intelligent WAN routing across sites | [SD-WAN security](../cloud-and-modern-networks/sd-wan-security.md) |

SSE is SWG + CASB + ZTNA (+ DLP, FWaaS); SASE is SSE + SD-WAN.

### Why it emerged

- **Users left the perimeter.** Remote and hybrid work means most users are not in the office, so a central firewall protects nobody on the road.
- **Applications left the data center.** SaaS and cloud mean most traffic goes to the internet, not the data center, so backhauling it to a central inspection point adds latency for no benefit.
- **Appliance sprawl.** Separate boxes for web filtering, CASB, VPN and firewall are costly to run and inconsistent; consolidation into one cloud service simplifies policy.

### What it is and is not

SASE/SSE is a *delivery and consolidation* model. It does not invent new protections; it takes the secure web gateway, CASB, ZTNA and firewall functions and runs them as one cloud service with unified policy and identity. The security value comes from consolidation (consistent policy, one place to manage, enforcement near every user) and from enabling zero-trust access, not from a novel mechanism. Evaluating a SASE offering means evaluating each component's quality plus the provider's coverage, performance and trustworthiness.

## Worked example

A company with 20 small offices and many remote staff currently backhauls all internet traffic over MPLS to a central firewall and uses a legacy VPN. Problems: slow internet for branches and remote users, inconsistent policy, an exposed VPN appliance. Moving to SASE:

1. **Edge enforcement.** Users and branches connect to the SASE provider's nearest point of presence. Web traffic is filtered and inspected there (SWG), SaaS use is governed (CASB), and firewall policy is applied (FWaaS), all with one policy set tied to user identity.
2. **ZTNA replaces the VPN.** Remote access to internal apps becomes per-application ZTNA, so a stolen credential no longer exposes a flat network and the VPN appliance is retired.
3. **SD-WAN.** Branches use SD-WAN to send internet-bound traffic directly out (through the SASE edge) instead of backhauling it, improving performance while keeping policy.
4. **Result.** Consistent security policy for every user wherever they are, faster access, no central backhaul bottleneck, and no internet-exposed VPN appliance. The trade is a dependency on the SASE provider, which now terminates and inspects the traffic.

The controls are the same ones this area describes; SASE changed where they run and unified their management.

## Trade offs and when to use it

- **Consolidation vs provider dependency.** One cloud service with unified policy simplifies operations and covers remote users, but concentrates trust in the provider, which sees (and often decrypts) the traffic. Evaluate the provider's security and jurisdiction.
- **Performance vs inspection.** Edge enforcement near users is faster than backhauling, but TLS inspection and DLP at the edge carry the same [inspection trade-offs](../secure-transport/tls-inspection.md) and privacy questions.
- **Fit.** SASE suits distributed organizations with many remote users and heavy SaaS use; a single-site organization with mostly on-premises applications gains less.
- **Lock-in.** A converged single-vendor service is harder to unpick than separate best-of-breed components; weigh integration benefit against flexibility.

## Common mistakes

- **Treating SASE as a new kind of security.** It is a delivery model for existing controls. Fix: evaluate each component (SWG, CASB, ZTNA, FWaaS) on its merits and the provider's trustworthiness.
- **Ignoring the provider trust and privacy implications.** The provider inspects your traffic. Fix: due diligence on the provider's security, data handling and jurisdiction.
- **Keeping the legacy VPN alongside without a plan.** Dual access models with inconsistent policy. Fix: migrate remote access to ZTNA with a defined timeline.
- **Assuming cloud delivery removes the TLS inspection dilemma.** It does not; the same decryption trade-offs apply at the edge. Fix: apply selective inspection and privacy policy as with on-premises inspection.
- **Adopting SASE where it does not fit.** A single-site, on-premises organization may gain little. Fix: match the model to the traffic pattern.

## Practice

1. What is the difference between SASE and SSE?
2. Why did backhauling all traffic to a central firewall stop making sense?
3. Name four security components typically bundled in SSE.
4. Why is SASE described as a delivery and consolidation model rather than a new security mechanism?
5. What is the main trust trade-off when adopting SASE?

### Answers

1. SASE is the convergence of SD-WAN networking with cloud-delivered security services; SSE is the security-only subset (the same security services without the SD-WAN networking).
2. Users and applications moved out of the office to remote locations, SaaS and cloud, so most traffic no longer goes to the data center; sending it to a central firewall first adds latency and protects nobody who is not on the internal network.
3. Secure Web Gateway, Cloud Access Security Broker, Zero-Trust Network Access, and Firewall-as-a-Service (and Data Loss Prevention).
4. It repackages existing controls (SWG, CASB, ZTNA, firewall) as one cloud-delivered service with unified policy near the user, rather than introducing a new protection mechanism; its value is consolidation and edge delivery.
5. The provider terminates and often decrypts the organization's traffic, so adopting SASE concentrates trust in that provider, requiring due diligence on its security, data handling and jurisdiction.

## Further reading

- Gartner, the original SASE and SSE definitions and market guides (coined 2019).
- NIST SP 800-207, Zero Trust Architecture, for the ZTNA component: https://doi.org/10.6028/NIST.SP.800-207
- Vendor SASE/SSE architecture documentation for component details (evaluate critically, these are marketing sources).
- CISA, Secure Cloud Business Applications (SCuBA) and cloud security guidance for the CASB angle.
