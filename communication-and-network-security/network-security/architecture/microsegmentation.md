# Microsegmentation

## Summary

Microsegmentation applies access control at the level of individual workloads rather than large network zones, so that each server, container or virtual machine accepts only the specific connections it needs, even from neighbors on the same subnet. It is the fine-grained form of [segmentation](network-segmentation.md) and a building block of [zero-trust networking](zero-trust-networking.md). Where traditional segmentation stops lateral movement between zones, microsegmentation stops it between workloads inside a zone, which is where most post-breach movement actually happens. It is enforced close to the workload (host firewalls, hypervisor policy, cloud security groups, service mesh) and is driven by identity and policy rather than by IP addresses and VLANs.

## Prerequisites

- [Network segmentation](network-segmentation.md): the coarse-grained parent concept.
- [Network security controls](../foundations/network-security-controls.md): placement at the host.
- [Lateral movement](../network-attacks/lateral-movement.md): what microsegmentation stops.

## Core concepts

### Definition

*Microsegmentation* enforces per-workload network policy: each workload has an allow list of the flows it may send and receive, defined by workload identity and function rather than by its location on the network. "Workload" means a server, VM, container or application instance.

### Analogy

Traditional segmentation is like dividing a building into floors with locked stairwells: people on a floor move freely among its rooms but need a key to change floors. Microsegmentation locks every individual office door and gives each person keys only to the specific rooms their job requires, so even two colleagues on the same floor cannot enter each other's offices without authorization. An intruder who gets into one office is trapped there.

The analogy holds well; it breaks in that "doors" here are policy rules tied to each workload's identity, which move with the workload when it is recreated elsewhere, unlike fixed physical doors.

### Why it matters: east-west inside a zone

A zone or VLAN typically lets its members talk to each other freely. After an attacker compromises one host, that intra-zone freedom is the highway for [lateral movement](../network-attacks/lateral-movement.md): scanning neighbors, reusing credentials, spreading ransomware. Microsegmentation removes the highway: workload A may talk to the database it uses and nothing else, so a compromised web server cannot reach a peer web server or an unrelated service even though they share a subnet.

### Enforcement technologies

| Where enforced | Technology | Notes |
| --- | --- | --- |
| Host | Host firewall driven by a central policy (agent) | Follows the workload; depends on host integrity |
| Hypervisor / virtual switch | Distributed firewall (e.g. NSX) | Enforced below the guest, hard for a compromised VM to evade |
| Cloud | Security groups / network policies per instance | Native, API-driven, identity-referencing |
| Container platform | Kubernetes NetworkPolicy, CNI | Per-pod, label-selected; see [Kubernetes network security](../cloud-and-modern-networks/kubernetes-network-security.md) |
| Service-to-service | Service mesh with mTLS | Identity by workload certificate, not IP |

The shift is from *where a workload is* (IP, VLAN) to *what a workload is* (its identity, labels, role). This is why microsegmentation survives dynamic environments where addresses change constantly.

### Policy from observed flows

Writing per-workload policy by hand is impractical, so the usual method is:

1. *Discover* actual flows by observing traffic for a period (flow logs, agents).
2. *Model* the application's real dependencies from the observed flows.
3. *Author* allow-list policy from the model, in monitor-only mode first.
4. *Enforce* once the policy is validated, then alert on anything outside it.

This observe-then-enforce cycle avoids breaking applications whose dependencies were undocumented, which is the main operational risk.

## Worked example

A three-tier application (web, app, database) runs as containers in one Kubernetes namespace that currently allows all pod-to-pod traffic.

1. **Discover.** Flow logs show the real paths: internet to web (443), web to app (8443), app to database (5432). No web-to-web, web-to-database, or app-to-app traffic exists.
2. **Author policy.** Microsegmentation rules (here, Kubernetes NetworkPolicies selecting pods by label):
   - web pods: accept from ingress on 443; may connect to app pods on 8443.
   - app pods: accept from web on 8443; may connect to database on 5432.
   - database pods: accept from app on 5432; initiate nothing.
   - default: deny all other pod-to-pod traffic.
3. **Result.** If a web pod is compromised, the attacker can reach the app tier on 8443 (an allowed flow) but cannot reach the database directly, cannot reach another web pod, and cannot scan the namespace. Lateral movement is cut to the single legitimate next hop, and any attempt outside the policy is denied and alerted.

Contrast with the flat namespace: a compromised web pod could scan and attack every pod, including the database directly. Microsegmentation changed a full-namespace exposure into a single contained path.

## Trade offs and when to use it

- **Containment vs operational cost.** Microsegmentation sharply limits lateral movement but requires accurate flow discovery, policy authoring and maintenance per workload; it is most justified for high-value or high-exposure environments first.
- **Identity-based vs address-based.** Identity/label-based policy survives dynamic addressing and autoscaling; address-based rules break constantly in cloud and container environments. Prefer identity.
- **Host/agent vs hypervisor/mesh enforcement.** Host agents follow the workload but trust the host; hypervisor and mesh enforcement sit outside the guest and are harder to evade. Combine based on environment.
- **Where it is overkill.** Low-value, static, already well-segmented environments may not need per-workload policy; apply effort where lateral movement risk is real.

## Common mistakes

- **Enforcing before discovery.** Breaks applications with undocumented dependencies. Fix: observe-then-enforce, monitor-only first.
- **Address-based rules in dynamic environments.** Constant breakage as IPs change. Fix: identity/label-based policy.
- **Microsegmenting only the perimeter workloads.** Leaves internal lateral paths open. Fix: cover the workloads that matter for lateral movement, especially shared and high-value services.
- **Trusting a host agent that the attacker can disable.** Fix: enforce below the guest (hypervisor, mesh) for high-value workloads; monitor agent health.
- **Static policy that decays.** Applications change; stale allow lists either break apps or leave gaps. Fix: periodic re-discovery and policy review.

## Practice

1. How does microsegmentation differ from traditional zone-based segmentation?
2. Why is intra-zone (east-west) traffic the main thing microsegmentation addresses?
3. Why is identity- or label-based policy preferred over IP-based policy for microsegmentation?
4. What is the observe-then-enforce cycle, and why is it necessary?
5. In the worked example, what can a compromised web pod reach, and what can it not?

### Answers

1. Traditional segmentation controls traffic between large zones; microsegmentation controls traffic per individual workload, including between workloads on the same subnet.
2. Members of a zone usually talk freely, so after one host is compromised the intra-zone freedom is the path for lateral movement; microsegmentation removes that freedom.
3. Workloads in dynamic environments change IP addresses and scale up and down constantly, so identity or labels (what the workload is) produce stable policy, whereas IP-based rules break continuously.
4. First discover the application's real flows by observation, model dependencies, author allow-list policy in monitor-only mode, then enforce; it is necessary because undocumented dependencies would otherwise be broken by immediate enforcement.
5. It can reach the app tier on the one allowed port (8443); it cannot reach the database directly, reach other web pods, or scan the namespace.

## Further reading

- NIST SP 800-207, Zero Trust Architecture (2020): https://doi.org/10.6028/NIST.SP.800-207
- NIST SP 800-215, Guide to a Secure Enterprise Network Landscape (2022): https://doi.org/10.6028/NIST.SP.800-215
- Kubernetes NetworkPolicy documentation: https://kubernetes.io/docs/concepts/services-networking/network-policies/
- Cloud Security Alliance and vendor guidance on microsegmentation and software-defined perimeters.
