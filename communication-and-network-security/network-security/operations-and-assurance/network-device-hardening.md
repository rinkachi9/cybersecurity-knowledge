# Network device hardening

## Summary

Network devices, routers, switches, firewalls, wireless controllers, are themselves computers with operating systems, services and credentials, and compromising one gives an attacker control over the traffic it carries. Hardening them means reducing their attack surface and securing their administration: strong authentication and AAA, encrypted management only, disabling unused services, protecting the control and management planes, keeping firmware patched, and backing up and monitoring configurations for drift. Network infrastructure is a prime target precisely because it is often overlooked, left on default credentials and old firmware while the servers behind it are carefully maintained. Hardening follows published baselines (CIS Benchmarks, NSA and vendor guides).

## Prerequisites

- [Management plane security](../architecture/management-plane-security.md): the administrative-access controls this builds on.
- [Insecure legacy protocols](../core-protocols/insecure-legacy-protocols.md) and [SSH security](../secure-transport/ssh-security.md).
- [Network security controls](../foundations/network-security-controls.md).

## Core concepts

### Definition

*Network device hardening* is the process of configuring network infrastructure to minimize its attack surface and secure its operation: removing unnecessary functionality, securing administrative access, protecting the device's own planes, and maintaining it (patching, config backup, monitoring).

### Analogy

A network device is like the building's electrical and control panels. They are not where people work, so they get ignored, but whoever controls them controls the lights, locks and elevators for everyone. Hardening is locking the panel room, using named keys with a log, removing unused switches that could be flipped maliciously, keeping the wiring to code, and keeping a wiring diagram so you notice if someone rewires it.

The analogy holds well; it carries the key point that infrastructure is high-impact precisely because it is background and overlooked.

### The planes to protect

A device has three planes ([management plane security](../architecture/management-plane-security.md) covers them), each needing hardening:

- *Management plane*: how the device is administered. Harden with AAA, MFA, encrypted protocols, access restriction (see below and the management-plane note).
- *Control plane*: the routing and signaling protocols the device runs. Harden with routing authentication ([BGP security](../core-protocols/bgp-security.md)), [spanning-tree protections](../link-layer/switch-security.md), and *control-plane policing* (rate-limiting traffic destined to the device's CPU so it cannot be overwhelmed).
- *Data plane*: the traffic it forwards. Harden with the filtering and anti-spoofing covered throughout this area.

### The hardening checklist

| Area | Hardening action |
| --- | --- |
| Authentication | Centralized AAA (TACACS+/RADIUS), per-admin accounts, MFA, no shared or default credentials, role-based command authorization |
| Management access | Encrypted only (SSH, HTTPS, SNMPv3); disable Telnet, HTTP, SNMPv1/2c; restrict to management network/bastion; no internet exposure |
| Unused services | Disable unused services and ports (CDP/LLDP where not needed, HTTP server, finger, etc.); close unused physical ports |
| Control plane | Control-plane policing, routing protocol authentication, STP guards, ICMP rate limits |
| Firmware | Keep current; subscribe to vendor advisories; prioritize internet-facing devices (VPN gateways, firewalls are heavily targeted) |
| Configuration | Version-controlled backups, change management, drift detection against a known-good baseline |
| Logging | Send logs and AAA accounting to a [SIEM](../../../security-operations/defensive-operations/operations/siem.md); synchronized time (NTP, authenticated) |
| Physical | Secure console ports, disable password recovery where policy requires, physical access control |

### Why it is a prime target

Network devices are attractive because: a compromised router or switch sees and can redirect traffic; they often run old firmware (patching network gear causes outages, so it is deferred); they frequently keep default or weak credentials; and their management is sometimes exposed to the internet. Nation-state and criminal actors specifically target edge devices (VPN gateways, firewalls, routers) as initial access, and several of the most-exploited vulnerabilities each year are in network appliances. Hardening and patching infrastructure is therefore not optional background work; it is front-line defense.

### Configuration backup and drift

A device's security lives in its configuration. Hardening includes keeping version-controlled backups (so a change can be reviewed and rolled back) and *drift detection*, comparing the running configuration against the approved baseline to catch unauthorized or accidental changes. An attacker who gains access often changes configuration (adds an account, opens a path, disables logging); drift detection surfaces exactly that.

## Worked example

Hardening a switch found with default settings (reference configuration, consistent with CIS and NSA guidance; not run in the namespace lab, which has no managed device):

1. **Authentication.** Replace the shared enable password and local `admin` with per-admin accounts via TACACS+, MFA at the [bastion](../architecture/management-plane-security.md), role-based authorization, and command accounting to the SIEM.
2. **Management.** Disable Telnet and the HTTP server; allow SSH and HTTPS only, reachable only from the management network. Move SNMP to v3; remove default community strings.
3. **Services.** Disable unused services and protocols; shut unused ports or place them in an unused VLAN; apply the [switch-security](../link-layer/switch-security.md) features (port security, DHCP snooping, DAI, BPDU guard).
4. **Control plane.** Enable control-plane policing to protect the CPU, authenticate routing protocols, and enable STP guards on access ports.
5. **Maintenance.** Put the configuration under version control with drift detection, update firmware and subscribe to advisories, and ensure authenticated NTP and log forwarding.

Result: the device now has no default credentials, no cleartext management, a minimal service surface, protected planes, and change visibility, turning a soft target into a hardened one. The single most common real-world failure this fixes is the device left on defaults with internet-reachable management.

## Trade offs and when to use it

- **Patching vs uptime.** Updating network firmware can cause outages, which is why it is deferred, but deferral leaves known-exploited vulnerabilities open. Fix: maintenance windows, redundancy for hitless upgrades, prioritize internet-facing devices.
- **Feature-rich vs minimal.** Devices ship with many services on for convenience; each is attack surface. Disable what is unused, accepting the small effort to confirm nothing depends on it.
- **Central AAA dependency.** Centralized authentication is strong but becomes critical; provide redundancy and a secured local fallback.
- **Baselines.** Follow CIS/NSA/vendor baselines rather than inventing hardening ad hoc; they encode broad experience, but tailor to the environment.

## Common mistakes

- **Default or shared credentials.** The classic infrastructure compromise. Fix: per-admin accounts via AAA, no defaults.
- **Internet-exposed management.** A direct path to control. Fix: management only via the management network/bastion, never the internet.
- **Cleartext management (Telnet/HTTP/SNMPv1-2c).** Sniffable credentials. Fix: SSH/HTTPS/SNMPv3 only.
- **Deferred firmware patching on edge devices.** Prime initial-access targets. Fix: prioritize and schedule; subscribe to advisories.
- **No config backup or drift detection.** Malicious changes go unnoticed and are unrecoverable. Fix: version-controlled backups and drift alerts.
- **Unused services and ports left on.** Needless attack surface. Fix: disable them.

## Practice

1. Why is a network device a higher-impact target than an ordinary server?
2. What are the three planes of a network device, and give one hardening action for each.
3. Why is firmware patching on network gear often deferred, and why is that dangerous?
4. What does configuration drift detection catch that other controls might miss?
5. Why follow published baselines (CIS/NSA) rather than hardening ad hoc?

### Answers

1. It carries and can redirect the traffic of many systems, so compromising it gives control over communications for everything behind it, not just one host.
2. Management plane (AAA/MFA/encrypted management), control plane (control-plane policing, routing authentication, STP guards), data plane (filtering and anti-spoofing).
3. Updating firmware can cause outages, so it is deferred for stability; this leaves known-exploited vulnerabilities (especially on heavily targeted edge devices) open to attackers who specifically hunt unpatched infrastructure.
4. Unauthorized or accidental configuration changes, such as an attacker adding an account, opening a path or disabling logging, by comparing the running config against the approved baseline.
5. Baselines encode broad, tested experience and cover items easy to overlook, giving consistent and comprehensive hardening; ad hoc hardening tends to miss things and vary by administrator.

## Further reading

- NSA, Network Infrastructure Security Guide (2022): https://media.defense.gov/2022/Jun/15/2003018261/-1/-1/0/CTR_NSA_NETWORK_INFRASTRUCTURE_SECURITY_GUIDE_20220615.PDF
- CIS Benchmarks for network devices (Cisco, Juniper, etc.): https://www.cisecurity.org/cis-benchmarks
- CISA, guidance on securing network infrastructure and the Known Exploited Vulnerabilities catalog (heavy on edge devices): https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- [Management plane security](../architecture/management-plane-security.md) for administrative-access hardening.
