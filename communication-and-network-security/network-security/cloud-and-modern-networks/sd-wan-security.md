# SD-WAN security

## Summary

Software-defined wide area networking (SD-WAN) replaces traditional, rigid WAN links (such as MPLS) with software that intelligently steers traffic across multiple connections, often cheap internet links, between sites, data centers and cloud. It improves cost, performance and agility, and it is a building block of [SASE](../architecture/sase-and-sse.md). Its security relevance is twofold: SD-WAN itself must be secured (its central controller and management plane are high-value targets, and its tunnels must be properly encrypted), and SD-WAN enables security by routing site traffic through cloud-delivered security services instead of backhauling it. This note covers both: securing the SD-WAN fabric and using it to deliver security.

## Prerequisites

- [VPNs](../secure-transport/vpns.md) and [IPsec](../secure-transport/ipsec.md): SD-WAN tunnels are usually IPsec.
- [Management plane security](../architecture/management-plane-security.md): the SD-WAN controller is a management plane.
- [SASE and SSE](../architecture/sase-and-sse.md): SD-WAN is the networking half.

## Core concepts

### Definition

*SD-WAN* is an architecture that abstracts the WAN into software: edge devices at each site connect over multiple transport links (internet, LTE, MPLS), and a central controller pushes policy that steers each application's traffic over the best available link, with encryption between sites. It separates the control plane (centralized policy) from the data plane (the edge devices forwarding traffic).

### Analogy

Traditional WAN is a single dedicated private road between two offices: reliable but expensive and inflexible. SD-WAN is a smart satnav that uses all available roads (including public ones), picking the fastest for each trip and re-routing around jams, while putting valuables in a locked box for the public-road legs. The satnav's routing brain (the controller) is central and powerful, so protecting it is paramount; if someone hijacks the satnav, they can redirect every vehicle.

The analogy holds well; it carries the two security points, encrypt the public-road legs, and guard the central routing brain.

### Securing the SD-WAN fabric

SD-WAN introduces its own attack surface:

- *The controller / orchestrator* is a central management plane that configures every edge device. Compromising it means controlling the whole WAN's routing and policy, the highest-value target. It must be hardened and isolated like any [management plane](../architecture/management-plane-security.md): strong authentication and MFA, encrypted and restricted management access, patching, and not exposed to the internet beyond what is necessary.
- *The tunnels* between sites run over untrusted internet links, so they must be strongly encrypted and authenticated, typically [IPsec](../secure-transport/ipsec.md) with modern crypto and certificate-based edge authentication, not weak pre-shared keys.
- *The edge devices* are internet-facing appliances and, like [VPN gateways](../secure-transport/vpns.md), are targeted; keep them patched and minimize exposure.
- *Zero-touch provisioning* (edges auto-configuring on first boot) is convenient but a risk if the enrollment is not strongly authenticated, since an attacker who can impersonate the enrollment could insert a rogue edge.

### Using SD-WAN to deliver security

SD-WAN's steering is also a security enabler:

- *Avoiding backhaul.* Instead of hauling all internet-bound traffic from a branch to a central firewall and back (slow, costly), SD-WAN can send it directly out, but through cloud-delivered security ([SASE/SSE](../architecture/sase-and-sse.md)), so policy still applies without the detour.
- *Application-aware policy.* It can route sensitive application traffic over more trusted links and enforce different policy per application.
- *Segmentation across the WAN.* SD-WAN can carry [segmentation](../architecture/network-segmentation.md) between sites, keeping, for example, OT traffic separate from corporate traffic end to end.

This is why SD-WAN and SASE are discussed together: SD-WAN is the intelligent transport, and the security services are delivered at the cloud edge it steers traffic through.

## Worked example

A retailer connects 50 branches, previously on expensive MPLS backhauled to a central firewall. Moving to secured SD-WAN:

1. **Fabric security.** Edge devices authenticate to the controller with certificates (not shared keys); the controller is in a hardened management network, MFA-protected, patched, not internet-exposed beyond its necessary enrollment endpoint, which uses strong mutual authentication for zero-touch provisioning.
2. **Encrypted tunnels.** Site-to-site traffic runs over [IPsec](../secure-transport/ipsec.md) with modern ciphers across the branches' cheap internet links, so the public-link legs are confidential and authenticated.
3. **No backhaul, still inspected.** Branch internet traffic goes directly out through the [SASE/SSE](../architecture/sase-and-sse.md) edge rather than to the central firewall, so web filtering, CASB and firewall policy still apply, with far better performance.
4. **Segmentation.** In-store payment-terminal traffic is carried in its own SD-WAN segment, isolated from guest Wi-Fi and back-office traffic end to end, supporting PCI scope control.
5. **Result.** Lower cost, faster branches, consistent security policy, and sensitive traffic segmented, provided the controller (the crown jewel) is well protected.

The example shows both halves: the fabric is secured (controller, tunnels, edges), and the SD-WAN is used to deliver security (no-backhaul inspection, WAN segmentation).

## Trade offs and when to use it

- **Agility/cost vs new attack surface.** SD-WAN cuts cost and improves performance but adds a powerful central controller and internet-facing edges to protect. The benefit is real; so is the obligation to secure the fabric.
- **Zero-touch provisioning vs enrollment risk.** Convenient at scale but must have strongly authenticated enrollment, or it becomes a path to insert rogue edges.
- **Vendor-integrated security vs best-of-breed.** Many SD-WAN products bundle security features; these may be convenient but should be evaluated on merit, and SD-WAN pairs naturally with dedicated [SASE/SSE](../architecture/sase-and-sse.md).
- **Internet links vs private.** Using cheap internet links saves money but relies entirely on the tunnel encryption and link diversity for reliability and confidentiality.

## Common mistakes

- **Under-protecting the controller.** It configures the whole WAN; its compromise is total. Fix: harden and isolate it as a critical management plane.
- **Weak tunnel crypto or pre-shared keys.** Traffic over public links exposed. Fix: strong IPsec with certificate-based edge authentication.
- **Unauthenticated zero-touch provisioning.** Lets an attacker insert a rogue edge. Fix: strongly authenticated enrollment.
- **Unpatched, over-exposed edge appliances.** Like VPN gateways, prime targets. Fix: patch promptly, minimize exposure.
- **Direct branch internet with no cloud security.** Removes backhaul but also removes inspection. Fix: steer direct traffic through SASE/SSE so policy still applies.

## Practice

1. What two aspects of security does SD-WAN involve?
2. Why is the SD-WAN controller the highest-value target in the fabric?
3. How does SD-WAN improve both performance and security compared with backhauling branch traffic to a central firewall?
4. What is the risk in zero-touch provisioning, and how is it mitigated?
5. Why are SD-WAN and SASE discussed together?

### Answers

1. Securing the SD-WAN fabric itself (controller, encrypted tunnels, edge devices) and using SD-WAN to deliver security (steering traffic through cloud security services, WAN segmentation).
2. It centrally configures every edge device's routing and policy, so compromising it gives control over the entire WAN's traffic.
3. SD-WAN sends branch internet traffic directly out (avoiding the slow, costly backhaul detour) while steering it through cloud-delivered security (SASE/SSE), so performance improves and policy still applies.
4. If enrollment is not strongly authenticated, an attacker could impersonate it and insert a rogue edge device into the fabric; mitigation is strongly (mutually) authenticated enrollment.
5. SD-WAN is the intelligent networking/transport half and SASE/SSE is the cloud-delivered security half; together they let branches reach the internet directly while still being secured, which is the SASE model.

## Further reading

- [SASE and SSE](../architecture/sase-and-sse.md) for the security-delivery context.
- [IPsec](../secure-transport/ipsec.md) and [VPNs](../secure-transport/vpns.md) for the tunnel technology.
- Vendor SD-WAN security architecture documentation (evaluate critically).
- Gartner SD-WAN and SASE market guidance.
