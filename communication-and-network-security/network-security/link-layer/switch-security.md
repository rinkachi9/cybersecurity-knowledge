# Switch security

## Summary

A switch forwards Ethernet frames inside a local network based on MAC addresses it learns from traffic. That learning is automatic and unauthenticated, which is the root of most link-layer attacks: a host can lie about its MAC address, flood the switch with fake ones, claim to be the DHCP server, or inject spanning-tree messages. Switch security is the set of features on managed switches that constrain this behavior: port security, DHCP snooping, Dynamic ARP Inspection, IP Source Guard, BPDU Guard and storm control. Together they turn a trusting layer-2 fabric into one that resists an attacker who has plugged into a port or joined the Wi-Fi.

## Prerequisites

- [Attack surface by layer](../foundations/attack-surface-by-layer.md): why layer-2 attacks are invisible to layer-3 controls.
- [Network threat model](../foundations/network-threat-model.md): the adjacent attacker.
- Basic Ethernet: MAC addresses, broadcast domains, VLANs.

## Core concepts

### Definition

*Switch security* comprises the controls on a layer-2 switch that enforce who may send what on each port. A switch's default job is to learn source MAC addresses and forward frames toward them; switch security adds verification to that learning and to the control protocols (DHCP, ARP, STP) that run alongside it.

### Analogy

An unmanaged switch is like a mailroom that delivers to whatever name is written on a desk, updating its map whenever a new nameplate appears, no questions asked. Switch security adds a receptionist: each desk may use only an assigned nameplate (port security), the mailroom checks that address claims match a signed register (DHCP snooping and DAI), and nobody at a desk may suddenly declare themselves the building's mail router (BPDU Guard).

The analogy breaks because a switch makes these decisions millions of times per second in hardware, so the controls must be expressible as simple per-frame checks, which is why they key off bindings and counters rather than judgment.

### The MAC address table and its abuse

A switch keeps a *MAC address table* (CAM table) mapping learned source MAC addresses to ports. Two abuses follow directly:

- A host can send frames with a *spoofed source MAC*, so the switch forwards that MAC's traffic to the attacker.
- A host can flood thousands of fake source MACs to overflow the finite table ([MAC flooding](mac-flooding.md)); when it is full, some switches fail open and broadcast unknown-destination traffic to every port, letting the attacker sniff.

### The control features

| Feature | Protects against | Mechanism |
| --- | --- | --- |
| Port security | MAC flooding, unauthorized devices | Limits the number of MAC addresses per port and can pin specific ones; violations disable the port or drop frames |
| DHCP snooping | [Rogue DHCP](dhcp-attacks.md) | Marks uplink ports "trusted"; DHCP server replies from untrusted (access) ports are dropped; builds the IP-MAC-port binding table |
| Dynamic ARP Inspection | [ARP spoofing](arp-spoofing/README.md) | Drops ARP packets that do not match the snooping bindings |
| IP Source Guard | IP spoofing from a port | Drops IP packets whose source address does not match the port's binding |
| BPDU Guard / Root Guard | Spanning-tree manipulation | Disables a port that sends spanning-tree BPDUs, or rejects a superior root claim |
| Storm control | Broadcast/multicast floods | Caps broadcast, multicast or unknown-unicast traffic per port |
| 802.1X | Unauthorized access | Requires authentication before a port forwards traffic; see [network access control](network-access-control-8021x.md) |

DHCP snooping is foundational: DAI and IP Source Guard both rely on the binding table it builds, so it is enabled first.

### Spanning Tree Protocol and its risks

The Spanning Tree Protocol (STP) prevents loops in a switched network by electing a root switch and blocking redundant links. It trusts the *Bridge Protocol Data Units* (BPDUs) that switches exchange. An attacker on an access port can send a BPDU claiming to be the root, forcing the network to reconverge around them (traffic redirection) or flap repeatedly (denial of service). *BPDU Guard* on access ports (which should never see BPDUs) shuts the port if one appears; *Root Guard* prevents a port from becoming a path to a new root. These are standard access-port hardening.

## Worked example

The namespace lab uses a software bridge without these management features, so this example is a hardening baseline for a real access port rather than a lab run. A minimally hardened Cisco access port:

```text
interface GigabitEthernet0/5
 switchport mode access
 switchport access vlan 10
 switchport port-security                     ! limit MACs on this port
 switchport port-security maximum 2           ! e.g. a PC plus a phone
 switchport port-security violation restrict  ! drop and log on excess MACs
 spanning-tree portfast
 spanning-tree bpduguard enable               ! shut the port if it sends BPDUs
 ip verify source                             ! IP Source Guard
!
ip dhcp snooping
ip dhcp snooping vlan 10
ip arp inspection vlan 10                      ! DAI, using the snooping bindings
```

Reading it: the port accepts at most two MAC addresses, drops DHCP server replies and spoofed ARP, verifies source IP, and shuts itself if a device tries to participate in spanning tree. An attacker who plugs in gets a single authorized-looking connection and none of the layer-2 attacks work. The uplink toward the real DHCP server and switches is configured as trusted so legitimate control traffic passes.

## Trade offs and when to use it

- **Port security maximum.** Too low breaks a PC-plus-phone-plus-VM setup; too high permits MAC flooding. Set it to the realistic device count per port.
- **Violation mode.** `shutdown` is safest but creates a help-desk burden (ports disabled by accident); `restrict` drops and logs without disabling. Choose per environment.
- **DHCP snooping trust.** Misconfiguring the uplink as untrusted blocks real DHCP; as trusted on the wrong port it defeats the control. This is the most common operational error.
- **BPDU Guard on the wrong ports.** Enabled on a real switch-to-switch link, it disables legitimate connectivity. Enable it only on access (edge) ports.

These features are standard on managed switches and should be on by default in enterprise access layers. They are absent on unmanaged switches and simple home gear, which is one reason guest and untrusted devices belong on separate, managed infrastructure.

## Common mistakes

- **Enabling DAI or IP Source Guard without DHCP snooping.** They have no bindings to check. Fix: snooping first.
- **Leaving unused ports enabled in a live VLAN.** An attacker plugs in and is on the network. Fix: shut unused ports or put them in an unused VLAN.
- **BPDU Guard on uplinks.** Disables real links. Fix: access ports only; use Root Guard on designated boundaries.
- **Trusting MAC-based port security as strong authentication.** MACs are forgeable; port security limits count, not identity. Fix: 802.1X for identity.
- **Flat VLAN with no inter-VLAN filtering.** Switch features harden ports but do not segment. Fix: combine with [segmentation](../architecture/network-segmentation.md).

## Practice

1. Why is a switch's default MAC learning a security weakness?
2. Which feature must be enabled before DAI and IP Source Guard, and why?
3. What does BPDU Guard do, and on which ports should it be enabled?
4. Why is MAC-based port security not a substitute for 802.1X?
5. What happens on some switches when the MAC address table overflows, and which feature prevents the overflow?

### Answers

1. It learns and trusts any source MAC with no verification, so hosts can spoof MACs, flood fake ones, or impersonate services.
2. DHCP snooping, because it builds the IP-MAC-port binding table that DAI and IP Source Guard check against.
3. It disables an access port that sends spanning-tree BPDUs (which an access port never should), preventing STP manipulation; enable it on access/edge ports only.
4. MAC addresses are easily spoofed, so port security limits the number of addresses but does not prove identity; 802.1X authenticates the device or user cryptographically.
5. Some switches fail open and flood unknown-unicast traffic to all ports, letting an attacker sniff; port security (limiting MACs per port) prevents the table-filling flood.

## Further reading

- NSA, Network Infrastructure Security Guide (2022), the layer-2 hardening sections: https://media.defense.gov/2022/Jun/15/2003018261/-1/-1/0/CTR_NSA_NETWORK_INFRASTRUCTURE_SECURITY_GUIDE_20220615.PDF
- Cisco, Catalyst switch security configuration guides (port security, DHCP snooping, DAI, IP Source Guard, BPDU Guard).
- IEEE 802.1Q (VLANs) and 802.1D/802.1w (spanning tree), the standards behind the behavior.
- CIS Benchmarks for network devices, for a vendor-neutral hardening checklist.
