# Network segmentation

## Summary

Network segmentation divides a network into parts and controls which traffic may pass between them. Its purpose is containment: when one system is compromised, segmentation limits what the attacker can reach next, and it makes the traffic that crosses boundaries visible and enforceable. A flat network, where every host can reach every other host on every port, turns one infected laptop into access to the whole company. Segmentation is not a product but a design: you decide on zones from the value and exposure of systems, define the allowed flows between zones, and enforce them with firewalls, ACLs or host policies.

## Prerequisites

- [Network threat model](../foundations/network-threat-model.md): segmentation mostly defends against the insider and lateral movement.
- [Defense in depth](../../../security-architecture-and-engineering/design-principles/defense-in-depth.md): segmentation is one layer, not the whole defense.
- [Security zones and DMZ](security-zones-and-dmz.md): the vocabulary of zones and boundaries.

## Core concepts

### Definition

*Segmentation* is the partitioning of a network into *segments* (groups of systems with a similar trust level and function) together with an *enforcement point* at every boundary that allows only explicitly approved flows. Two kinds of traffic are distinguished:

- *North-south* traffic crosses the edge of the environment, for example between the internet and a data center.
- *East-west* traffic stays inside, for example between two servers or two workstations.

Classic perimeter designs controlled only north-south traffic. Most of an intrusion, after the first foothold, happens east-west.

*Macro-segmentation* separates large zones (user networks, servers, management, OT, guests) usually with VLANs, VRFs and firewalls. *Microsegmentation* applies policy per workload or per application, usually on the host or hypervisor; see [microsegmentation](microsegmentation.md).

### Analogy

A ship is built with watertight compartments. A hole in the hull floods one compartment, and the doors between compartments keep the rest dry. The doors exist because people and goods must move, but they are few, known and can be closed.

The analogy holds for the main point: the design assumes a breach and limits its spread. It breaks because water has no intent. An attacker actively looks for an open door, so every allowed flow is a possible path, and doors that "nobody uses" are exactly the ones an attacker will find.

### Mechanism: from zones to enforced flows

1. **Inventory and classify.** List systems and data, and group them by function and by the impact of their compromise (for example with [FIPS 199 categories](../../../security-and-risk-management/foundations/cia-triad/README.md)).
2. **Define zones.** Typical zones: internet edge and DMZ, user workstations, guest, servers by tier (web, application, database), identity infrastructure (domain controllers), management, backup, OT, payment card environment.
3. **Write a flow matrix.** For each pair of zones, list the allowed protocols and ports, the direction and the reason. Everything not in the matrix is denied.
4. **Choose enforcement points.** Firewalls between zones, ACLs on layer 3 switches, cloud security groups, host firewalls.
5. **Enforce and log.** Default deny at every boundary, logging of denied and allowed flows.
6. **Verify and maintain.** Test that forbidden paths are really closed, review rules regularly, and treat every new flow request as a change with an owner and an expiry.

### Example flow matrix

| From \ To | Web DMZ | App servers | Database | Domain controllers | Management |
| --- | --- | --- | --- | --- | --- |
| Internet | TCP 443 | deny | deny | deny | deny |
| Workstations | TCP 443 | deny | deny | Kerberos, LDAP, DNS, SMB to DCs | deny |
| Web DMZ | - | TCP 8443 to app tier | deny | deny | deny |
| App servers | deny | - | TCP 5432 | Kerberos, LDAP, DNS | deny |
| Management (jump hosts) | SSH | SSH | SSH | RDP, WinRM | - |

Every cell is a decision with a reason. The empty diagonal means intra-zone traffic is a separate decision, usually handled by microsegmentation.

### Enforcement technologies

| Technology | Layer | Strength | Limitation |
| --- | --- | --- | --- |
| VLANs alone | 2 | Separates broadcast domains | No policy: if the router between VLANs allows everything, there is no segmentation |
| VRFs | 3 | Separate routing tables, no route means no path | Coarse, policy still needed where VRFs meet |
| ACLs on switches and routers | 3 and 4 | Fast, in the path | Usually stateless, hard to manage at scale |
| Stateful firewalls | 3 to 7 | Connection state, logging, application awareness | Throughput cost, hairpinning traffic to a central device |
| Cloud security groups | 3 and 4 | Per-interface, stateful, API-managed | Sprawl, rules referencing broad CIDRs |
| Host firewalls and agents | 3 to 7 | Identity of the process and workload | Depends on the host not being compromised |
| 802.1X with dynamic VLANs | 2 | Places a device in a segment based on identity | Needs certificate or credential infrastructure |

### Regulatory and framework anchors

- PCI DSS uses segmentation to reduce the scope of the cardholder data environment: systems that are properly isolated are out of scope, and the isolation itself must be tested.
- NIST SP 800-53 control SC-7 (Boundary Protection) and its enhancements require managed interfaces, deny by default and allow by exception.
- IEC 62443 builds OT security on zones and conduits; see [OT network security](../ot-and-iot/ot-network-security.md).
- CIS Controls v8 safeguard 12.2 asks for a secure network architecture with segmentation.

## Worked example

A company of 300 people has one `/16` network for everything. Ransomware entered through one phished laptop and encrypted file servers, backups and the domain controllers in four hours.

Redesign:

1. Zones: workstations (`10.10.0.0/16`), servers (`10.20.0.0/16`), identity (`10.30.0.0/24`), backup (`10.40.0.0/24`), management (`10.50.0.0/24`), guest (separate internet-only network).
2. Key flow decisions:
   - Workstations reach file servers only on SMB (TCP 445) and only the file servers, not every server.
   - Workstation to workstation traffic is blocked on the host firewall, because peers rarely need to talk directly and that path is the main route for worm-like spread.
   - Backup servers initiate connections to the systems they back up. Nothing initiates connections to the backup zone except the management zone. Backups are also kept offline or immutable, because segmentation alone does not stop an attacker who holds administrator credentials.
   - Administrative protocols (RDP, SSH, WinRM) are allowed only from jump hosts in the management zone.
3. Result in a repeat incident: the phished laptop can reach file shares it is entitled to and nothing else. Encryption is limited to those shares, the backups survive, and the denied connection attempts to RDP on servers produce alerts.

The example shows the typical value: segmentation did not prevent the first compromise, but it changed the outcome from total loss to a contained incident.

## Trade offs and when to use it

Benefits:

- Limits blast radius and lateral movement.
- Creates choke points where monitoring sees the important traffic.
- Reduces audit scope (PCI DSS) and supports regulatory requirements.

Costs:

- Requires an accurate inventory of applications and their dependencies. Undocumented dependencies cause outages when the rules are tightened.
- Rule sets grow and decay. Without ownership and review, segmentation slowly turns back into a flat network with extra steps.
- Central firewalls add latency and are a capacity bottleneck for east-west traffic.

When it is the wrong tool: segmentation does not help against an attacker who uses an allowed flow with valid credentials, for example a stolen administrator account used from a jump host. That needs identity controls and [zero trust networking](zero-trust-networking.md).

## Common mistakes

- **VLANs without filtering.** Different VLANs routed through a core switch that permits everything. Fix: enforce policy at the inter-VLAN routing point.
- **"Any" rules created during a migration and never removed.** Fix: every rule has an owner, a ticket and a review date. See [firewall rule design](../traffic-filtering/firewall-rule-design/README.md).
- **Forgetting outbound control.** Segments that may connect anywhere on the internet let attackers download tools and exfiltrate data. Fix: [egress filtering](../traffic-filtering/egress-filtering.md).
- **Shared services that bridge everything.** A monitoring server or backup server that can reach every zone with administrator credentials becomes the path between zones. Fix: put such systems in their own tightly controlled zone and limit their credentials.
- **Never testing.** Fix: test from each zone that forbidden destinations are really unreachable, as part of change management and periodic assessment.

## Practice

1. What is the difference between north-south and east-west traffic, and why does segmentation focus on the second?
2. Why are VLANs alone not segmentation?
3. In the worked example, why does the backup server initiate connections instead of accepting them?
4. Name two systems that commonly break segmentation because they need to reach every zone.
5. What should happen to a firewall rule that was created for a project that ended?

### Answers

1. North-south crosses the edge, east-west stays inside. After an initial foothold, most attacker movement is east-west, which a perimeter firewall never sees.
2. VLANs separate broadcast domains, but if traffic between them is routed without a policy, any host can still reach any other.
3. A compromised production host then has no allowed path into the backup zone, so it cannot reach and destroy the backups over the network.
4. For example monitoring and management servers, backup servers, vulnerability scanners, software deployment servers, domain controllers.
5. It should be removed, ideally automatically through an expiry date, after confirming that no traffic still uses it.

## Further reading

- NIST SP 800-215, Guide to a Secure Enterprise Network Landscape (2022). Covers the shift from perimeter to distributed security, including segmentation: https://doi.org/10.6028/NIST.SP.800-215
- NIST SP 800-53 Rev. 5, control SC-7 Boundary Protection: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- NSA, Network Infrastructure Security Guide (2022). Practical guidance on segmentation, filtering and management networks: https://media.defense.gov/2022/Jun/15/2003018261/-1/-1/0/CTR_NSA_NETWORK_INFRASTRUCTURE_SECURITY_GUIDE_20220615.PDF
- PCI Security Standards Council, Guidance for PCI DSS Scoping and Network Segmentation. How segmentation reduces compliance scope and how it is tested.
- CISA, Layering Network Security Through Segmentation (infographic, 2022), a short overview for non-specialists.
