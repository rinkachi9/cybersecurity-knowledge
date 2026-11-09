# Cloud network security

## Summary

Cloud networking keeps the same fundamentals, addresses, routing, segmentation, filtering, but changes how they are expressed and who is responsible for what. Networks are virtual (VPCs/VNets defined by software), controls are API-driven objects (security groups, network ACLs) rather than physical appliances, and the provider owns the underlying fabric so you cannot TAP it. The security model rests on the shared responsibility principle: the provider secures the cloud's infrastructure, you secure what you build on it, including network configuration, which is a leading source of breaches through misconfiguration. This note maps the on-premises network concepts in this area onto their cloud equivalents and highlights where the differences bite.

## Prerequisites

- [Network segmentation](../architecture/network-segmentation.md) and [firewalls](../traffic-filtering/firewalls.md): the concepts being mapped.
- [Flow monitoring](../monitoring-and-detection/flow-monitoring.md): VPC flow logs are the cloud visibility.
- [Cloud and infrastructure security](../../../security-architecture-and-engineering/cloud-and-infrastructure-security/README.md): the broader cloud area, including [CSPM](../../../security-architecture-and-engineering/cloud-and-infrastructure-security/cloud-security-posture-management.md).

## Core concepts

### Definition

*Cloud network security* is the protection of the virtual networks and network controls provided by cloud platforms (AWS, Azure, Google Cloud): the software-defined networks (VPC/VNet), the filtering objects (security groups, network ACLs), connectivity (gateways, peering, private endpoints), and the visibility (flow logs), under the shared responsibility model.

### Analogy

On-premises networking is owning the building and its wiring: you run the cables, install the firewalls, and can tap any wire. Cloud networking is renting serviced offices in a managed tower: the landlord (provider) secures the building structure, power and lifts (the fabric), and you configure your own suite, which doors connect to which, who may enter, using the building's standard systems (the API). You cannot rewire the tower or tap its risers, but you get a standard access-log feed (flow logs). A suite left unlocked is your fault, not the landlord's.

The analogy holds closely; it carries the shared-responsibility split and the "misconfiguration is on you" point that dominates cloud network breaches.

### Mapping the concepts

| On-premises | Cloud equivalent | Difference that matters |
| --- | --- | --- |
| Physical/VLAN network | VPC / VNet, subnets | Software-defined, created and changed by API in seconds |
| Stateful firewall at a boundary | Security groups (instance-level, stateful) | Attached per resource, identity/tag-referencing, not a central box |
| Router ACL | Network ACLs (subnet-level, stateless) | Coarser, stateless, a second layer |
| DMZ | Public vs private subnets, managed edge (ALB, API gateway) | No physical DMZ; public subnets and managed services |
| Dedicated line between sites | VPC peering, transit gateway, VPN, Direct Connect | Software-defined interconnects |
| Internet exposure | Public IPs, internet/NAT gateways | A single misconfig can expose a resource globally |
| Private service access | Private endpoints / PrivateLink | Reach provider services without traversing the internet |
| Packet capture / TAP | VPC/VNet flow logs (mostly metadata) | You cannot TAP the fabric; flow logs are the visibility |

The concepts are familiar; the expression is API-driven objects, and the speed and scale of change is far higher, which is why [configuration posture management](../../../security-architecture-and-engineering/cloud-and-infrastructure-security/cloud-security-posture-management.md) is a cloud-specific discipline.

### Security groups vs network ACLs

Two filtering layers, often confused:

- *Security groups* are stateful and attach to resources (instances, interfaces). Return traffic is automatically allowed. They can reference other security groups by identity, so "web tier may reach app tier" is expressed by group, not IP, which survives autoscaling. This is the primary, [microsegmentation](../architecture/microsegmentation.md)-friendly control.
- *Network ACLs* are stateless and apply at the subnet boundary. Return traffic needs explicit rules. They are a coarser second layer, useful for broad subnet-level deny.

Using security groups as the main control (identity-referencing, stateful) and NACLs as a coarse backstop is the usual pattern.

### Shared responsibility and misconfiguration

The provider secures the fabric (hypervisors, physical network, the VPC isolation itself); the customer secures their configuration. The dominant cause of cloud network breaches is customer misconfiguration: a security group open to `0.0.0.0/0` on a sensitive port, a storage service made public, a private resource given a public IP. Because a single API change can expose a resource to the entire internet instantly, and because changes are frequent and decentralized, continuous configuration checking ([CSPM](../../../security-architecture-and-engineering/cloud-and-infrastructure-security/cloud-security-posture-management.md)) is essential, not optional.

### Visibility in the cloud

You cannot place a TAP in the provider's network, so [flow logs](../monitoring-and-detection/flow-monitoring.md) (VPC/VNet flow logs) are the primary network visibility, supplemented by provider services (DNS query logs, managed IDS, traffic mirroring where offered) and by endpoint telemetry. Planning this visibility is part of cloud network design, since the on-premises sensor model does not transfer.

## Worked example

Designing network security for a three-tier app in a VPC (concepts mapped from the on-premises [segmentation](../architecture/network-segmentation.md) and [DMZ](../architecture/security-zones-and-dmz.md) notes):

1. **Subnets.** Public subnets hold only the load balancer and NAT gateway; private subnets hold the app tier; isolated subnets hold the database (no internet route at all).
2. **Security groups (identity-based).** The load balancer's group allows 443 from the internet; the app group allows its port only from the load balancer's group; the database group allows its port only from the app group. Expressed by group reference, so autoscaling new instances inherit the policy with no IP changes, the cloud form of [microsegmentation](../architecture/microsegmentation.md).
3. **Network ACLs.** A coarse subnet backstop denies the database subnet any internet-bound traffic.
4. **Private endpoints.** The app reaches provider services (storage, secrets) over private endpoints, not the internet, so no public path is needed for them.
5. **Visibility.** VPC [flow logs](../monitoring-and-detection/flow-monitoring.md) are enabled and centralized; the beaconing/exfiltration analytics from the monitoring subarea run on them.
6. **Posture.** [CSPM](../../../security-architecture-and-engineering/cloud-and-infrastructure-security/cloud-security-posture-management.md) continuously checks for the classic misconfigurations (a security group opened to `0.0.0.0/0`, a public IP on a private resource) and alerts on drift.

The result mirrors a sound on-premises design (public/private/isolated tiers, least-privilege flows, visibility) expressed in cloud-native objects, with continuous posture checking to catch the misconfigurations that are the main cloud risk.

## Trade offs and when to use it

- **Security groups vs NACLs.** Stateful, identity-referencing security groups are the primary control and survive dynamic addressing; stateless subnet NACLs are a coarse backstop. Use both, security groups as the main layer.
- **Speed vs safety.** API-driven networks change in seconds, enabling agility but also instant exposure; continuous posture checking is the counterbalance.
- **Native vs third-party controls.** Cloud-native controls are integrated and API-managed; third-party virtual appliances add familiar features (NGFW, IDS) at cost and complexity. Use native first, add appliances where they close a real gap.
- **Multi-cloud.** Each provider's model differs; abstractions and [multicloud CSPM](../../../security-architecture-and-engineering/cloud-and-infrastructure-security/multicloud-cspm.md) help manage the divergence.

## Common mistakes

- **Security groups open to `0.0.0.0/0` on sensitive ports.** Instant global exposure; the classic cloud breach. Fix: least-privilege groups, continuous checks.
- **Public IPs on resources that should be private.** Fix: private subnets with no internet route; private endpoints for provider services.
- **IP-based rules in an autoscaling environment.** Break as instances churn. Fix: identity/group-referencing security groups.
- **No flow logs.** Zero network visibility in the cloud. Fix: enable and centralize VPC/VNet flow logs.
- **Treating the provider as responsible for your configuration.** Misreads the shared responsibility model. Fix: own your network config; use CSPM to verify it.

## Practice

1. How does the shared responsibility model divide network security between provider and customer?
2. What is the difference between a security group and a network ACL, and which is the primary control?
3. Why do identity/group-referencing rules suit cloud environments better than IP-based rules?
4. Why is continuous configuration checking essential in the cloud specifically?
5. Why are flow logs the primary network visibility in the cloud?

### Answers

1. The provider secures the underlying fabric (physical network, hypervisors, VPC isolation); the customer secures what they configure on it, including subnets, security groups, exposure and routing.
2. Security groups are stateful and attach per resource (return traffic auto-allowed, can reference other groups by identity); network ACLs are stateless and apply at the subnet boundary (return traffic needs explicit rules). Security groups are the primary control.
3. Cloud resources autoscale and change IPs constantly, so rules that reference security groups or tags (identity) stay correct as instances churn, whereas IP-based rules break.
4. A single API change can expose a resource to the entire internet instantly, and changes are frequent and decentralized, so misconfigurations arise and must be caught continuously rather than at periodic review.
5. The customer cannot TAP the provider's network fabric, so VPC/VNet flow logs (metadata) are the available network record, supplemented by provider logging and endpoint telemetry.

## Further reading

- [Cloud and infrastructure security](../../../security-architecture-and-engineering/cloud-and-infrastructure-security/README.md) and [CSPM](../../../security-architecture-and-engineering/cloud-and-infrastructure-security/cloud-security-posture-management.md) for the posture-management discipline.
- Cloud provider network security documentation (AWS VPC, Azure VNet, Google VPC security best practices).
- NIST SP 800-207, Zero Trust Architecture, applied to cloud: https://doi.org/10.6028/NIST.SP.800-207
- [Kubernetes network security](kubernetes-network-security.md) for container networking on top of cloud networks.
