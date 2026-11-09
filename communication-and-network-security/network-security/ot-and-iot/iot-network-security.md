# IoT network security

## Summary

The Internet of Things (IoT) is the mass of network-connected devices that are not traditional computers: cameras, sensors, smart building systems, printers, medical devices, consumer gadgets. They share a hard security profile: weak or default credentials, rare or no patching, insecure-by-design services, long lifecycles, and no ability to run an endpoint agent, all deployed in large numbers. Because you usually cannot secure the device, IoT network security means securing the network around it: putting IoT on isolated segments, controlling what it can reach (especially outbound), monitoring it, and keeping it away from the rest of the network. The Mirai botnet, built from default-credential IoT devices, is the standing illustration of what happens when this is neglected.

## Prerequisites

- [Network segmentation](../architecture/network-segmentation.md) and [network access control (802.1X)](../link-layer/network-access-control-8021x.md).
- [Egress filtering](../traffic-filtering/egress-filtering.md) and [OT network security](ot-network-security.md) (the related, overlapping domain).
- [Insecure legacy protocols](../core-protocols/insecure-legacy-protocols.md).

## Core concepts

### Definition

*IoT* devices are purpose-built network-connected devices that are not general-purpose computers, typically embedded, with limited interfaces and resources. *IoT network security* protects the network in the presence of such devices, which usually cannot be secured individually.

### Analogy

IoT devices are like cheap locks fitted throughout a building by many different contractors: each is weak, you do not have the key schedule for most of them, and you cannot upgrade them. You do not try to make each cheap lock strong; you put the rooms they guard behind one good door, watch who goes through it, and make sure a thief who picks a cheap lock finds only that one room, not a corridor to the vault. The building's layout, not the individual locks, provides the security.

The analogy holds closely; it carries the "cannot fix the device, contain it with the network" principle shared with [OT](ot-network-security.md).

### Why IoT is hard to secure

- *Weak/default credentials*: many ship with hard-coded or default passwords, often unchangeable; Mirai simply logged in with a list of defaults.
- *Rare or no patching*: no update mechanism, abandoned by the vendor, or updates that require manual effort nobody does.
- *Insecure services*: [Telnet, old web interfaces, UPnP](../core-protocols/insecure-legacy-protocols.md), and other services on by default.
- *No agent possible*: you cannot install endpoint protection, so EDR does not cover them, the network is the only vantage point.
- *Scale and invisibility*: they are numerous, often deployed without IT's knowledge (shadow IoT), and easily forgotten in inventory.
- *Long lifecycles*: a camera or sensor may run for a decade with its original firmware.

### The network is the only lever

Since the device cannot be secured, IoT security is network security:

- *Isolate on dedicated segments.* IoT devices go on their own VLANs/segments ([segmentation](../architecture/network-segmentation.md)), separated from user and server networks, so a compromised device reaches little. [802.1X and NAC](../link-layer/network-access-control-8021x.md) with profiling can place devices into the right segment automatically and keep unknown devices out.
- *Control egress strictly.* Most IoT devices need to talk only to a few specific destinations (a vendor cloud, an NTP server). [Default-deny egress](../traffic-filtering/egress-filtering.md) prevents a compromised device from being recruited into a botnet (outbound to attacker infrastructure) or used for [exfiltration](../network-attacks/data-exfiltration.md), and it turns unexpected outbound attempts into alerts.
- *Restrict inbound and east-west.* Devices should not be reachable from the internet (Mirai exploited internet-exposed devices) and should not reach other internal systems beyond what they need.
- *Monitor.* Passive network monitoring detects compromised devices by their behavior (a camera suddenly scanning, beaconing, or generating DDoS traffic), since you cannot get telemetry from the device itself.
- *Inventory and discover.* You cannot protect what you do not know is there; device discovery and profiling find shadow IoT.

### IoT vs OT

IoT and [OT](ot-network-security.md) overlap heavily and share the "secure the network around unsecurable devices" principle. The distinction is loose: OT specifically controls physical industrial processes (safety-critical, availability-first), while IoT is the broader category of embedded connected devices, including consumer and building systems. Industrial IoT sits between them. The defenses are largely the same (segmentation, egress control, monitoring), with OT adding stronger safety and availability constraints.

## Worked example

Securing a building's IoT (cameras, sensors, smart HVAC) that have default credentials and no patches (conceptual):

1. **Discover and inventory.** Network discovery and profiling find all the devices, including some shadow IoT (a smart TV, a personal assistant) nobody had recorded.
2. **Isolate.** All IoT devices are placed on dedicated VLANs via [NAC profiling](../link-layer/network-access-control-8021x.md), separated from the corporate and server networks. Unknown devices are denied or quarantined.
3. **Egress control.** [Default-deny egress](../traffic-filtering/egress-filtering.md): the cameras may reach only their management server and an NTP source; the HVAC only its vendor cloud endpoint. Everything else outbound is blocked and alerted, so a device recruited into a botnet cannot reach attacker infrastructure.
4. **No internet exposure.** None of the devices is reachable from the internet; remote access to the camera system is via a controlled path, not by exposing the cameras.
5. **East-west restriction.** The IoT VLAN cannot initiate connections to the corporate or server networks; management flows are one-way from controlled sources.
6. **Monitor.** Passive monitoring baselines the devices' simple, repetitive traffic and alerts on anomalies (a camera scanning the network or beaconing out).
7. **Result.** The devices remain insecure (default credentials, no patches), but a compromised one is isolated, cannot be reached from the internet, cannot reach attacker infrastructure or internal systems, and its misbehavior is detected, exactly what would have prevented Mirai-style recruitment.

The example applies the IoT principle: accept the device cannot be secured, and let the network contain and watch it.

## Trade offs and when to use it

- **Containment vs device function.** Strict isolation and egress control are the main defenses, but each device's few legitimate flows must be identified so function is not broken; use observe-then-enforce.
- **NAC/profiling effort vs coverage.** Automatic profiling and segment assignment scale to many devices and catch shadow IoT, at the cost of a NAC deployment; manual assignment does not scale.
- **Replace vs contain.** Insecure IoT with long lifecycles usually cannot be replaced soon; contain with the network and plan replacement, as with OT.
- **Consumer/shadow IoT.** Devices brought in without IT's knowledge are a particular risk; discovery and a default-deny posture for unknown devices are the counter.

## Common mistakes

- **IoT on the main network.** A compromised device reaches everything. Fix: dedicated isolated segments via NAC.
- **Default credentials left in place where changeable, and no egress control where not.** Mirai's exact opening. Fix: change defaults where possible; always apply default-deny egress.
- **Internet-exposed devices.** Directly attacked and recruited into botnets. Fix: never expose IoT to the internet; controlled remote access instead.
- **No inventory / shadow IoT.** Unknown devices unprotected. Fix: discovery and profiling; deny unknown devices by default.
- **Expecting endpoint agents or patches to save you.** Usually impossible on IoT. Fix: rely on network containment and monitoring.

## Practice

1. Why can IoT devices usually not be secured individually?
2. Why is strict egress control especially important for IoT, with reference to botnets?
3. How does NAC with profiling help manage large numbers of IoT devices?
4. What was the key network failure that enabled the Mirai botnet?
5. How do IoT and OT network security relate?

### Answers

1. They commonly have weak or unchangeable default credentials, no or rare patching, insecure-by-design services, no ability to run an endpoint agent, and long lifecycles, so the device itself cannot be hardened.
2. Most IoT devices need only a few outbound destinations; default-deny egress stops a compromised device from reaching attacker infrastructure (preventing botnet recruitment, as in Mirai) and from exfiltrating, and makes unexpected outbound attempts into alerts.
3. It automatically identifies (profiles) device types and places them into the correct isolated segment, keeps unknown devices out, and scales to large numbers, also surfacing shadow IoT.
4. Large numbers of IoT devices with default credentials were exposed directly to the internet, letting Mirai log in and recruit them; isolation and no internet exposure would have prevented it.
5. They overlap and share the principle of securing the network around unsecurable devices (segmentation, egress control, monitoring); OT specifically controls safety-critical physical processes with availability-first priorities, while IoT is the broader embedded-device category.

## Further reading

- NIST SP 800-213 and NISTIR 8259 series, IoT device cybersecurity guidance: https://doi.org/10.6028/NIST.SP.800-213
- Antonakakis, M. et al., "Understanding the Mirai Botnet", USENIX Security 2017: https://www.usenix.org/conference/usenixsecurity17/technical-sessions/presentation/antonakakis
- [OT network security](ot-network-security.md) for the closely related industrial domain.
- ENISA and CISA IoT security guidance.
