# MAC flooding

## Summary

MAC flooding is a link-layer attack that overflows a switch's MAC address table by sending a large number of frames with different fake source MAC addresses. The table has a finite size, and when it fills, some switches stop learning and fail open: they flood frames for unknown destinations out of every port, as a hub would. The attacker on any port then receives traffic meant for other hosts and can sniff it. The defense is port security, which caps how many MAC addresses a port may use and so prevents one port from filling the table.

## Prerequisites

- [Switch security](switch-security.md): the MAC address table and port security.
- [Attack surface by layer](../foundations/attack-surface-by-layer.md): layer-2 attacks.

Authorized use only. Described for detection and mitigation; no attack tool is provided.

## Core concepts

### Definition

*MAC flooding* (also CAM table overflow) sends many frames with distinct, forged source MAC addresses so the switch learns them all until its *content-addressable memory* (CAM) table is exhausted. The goal is to force the switch into *fail-open* behavior, turning a switched segment back into a shared one the attacker can eavesdrop on. It relates to MITRE ATT&CK Network Sniffing (T1040).

### Analogy

A switch's MAC table is a receptionist's notepad mapping names to desks. An attacker scribbles thousands of fake names until the notepad is full. With no room to record the real desk for an incoming visitor, the flustered receptionist resorts to walking every visitor past every desk, so the attacker, sitting at one desk, sees everyone's visitors.

The analogy breaks because not every switch fails this way; many modern switches simply stop learning new addresses and keep forwarding known ones correctly, which limits the attack.

### Mechanism and its limits

The attack floods forged source MACs. What happens next depends on the switch:

- **Fail-open switches** flood all unknown-unicast traffic to every port once the table is full, exposing traffic to the attacker. This is the classic, sniff-enabling outcome.
- **Modern switches** often stop learning new MACs when the table is full but keep existing entries and forward their traffic normally, so the attacker gains little beyond noise, and the flooding itself may be detected.

Either way, the flood is noisy: a sudden appearance of thousands of MAC addresses on one port is a strong signal.

### Defense: port security

*Port security* limits the number of source MAC addresses accepted on a port (for example two, a PC and a phone). A flood of fake MACs trips the limit immediately, and the switch drops the excess, logs a violation, or disables the port, depending on the configured violation mode. Because the attacker is confined to one port, they cannot fill a table sized for the whole switch. Port security is the direct and sufficient control.

## Worked example

The namespace lab has no CAM-limited hardware switch, so this is a configuration and detection example. Port security on a Cisco access port:

```text
interface GigabitEthernet0/5
 switchport port-security
 switchport port-security maximum 2
 switchport port-security violation restrict
 switchport port-security aging time 2
```

With this in place, a MAC flood from the host on that port exceeds two addresses instantly; `restrict` drops the extra frames and increments a violation counter that a monitoring system reads. If set to `shutdown`, the port is disabled and an alert is raised.

Detection without port security, from switch counters or a sensor: a single port sourcing an abnormal number of distinct MAC addresses per second, or a sudden rise in flooded unknown-unicast traffic, both indicate CAM overflow in progress.

## Trade offs and when to use it

- **Port security maximum** must match the real number of devices behind a port (PC, phone, a few VMs); too low causes outages, too high leaves room to flood.
- **Violation mode.** `shutdown` stops the attack hard but risks disabling ports on legitimate quirks; `restrict` keeps the port up while dropping and logging. Many sites use `restrict` with alerting.
- **Sticky MAC learning** can pin the first-seen addresses to a port for convenience, but it inherits whatever was plugged in at that moment, so it is not an identity control.

MAC flooding is largely solved by enabling port security, which is standard on enterprise access ports. It remains relevant on unmanaged switches and where port security is not configured.

## Common mistakes

- **No port security on access ports.** Fix: enable it with a realistic maximum on every access port.
- **Treating a fail-safe modern switch as immune.** It may stop the sniff but the flood is still a denial-of-service and reconnaissance signal. Fix: detect and alert on it anyway.
- **Maximum set too high "to be safe".** Leaves room to flood. Fix: set to the real device count.
- **Confusing port security with authentication.** It counts MACs, it does not verify identity. Fix: add 802.1X where identity matters.

## Practice

1. What resource does MAC flooding exhaust, and what is the dangerous "fail-open" result?
2. Why do many modern switches limit the damage of MAC flooding?
3. How does port security prevent the attack?
4. Why is a MAC flood easy to detect even when it does not succeed in sniffing?
5. Why is port security not an identity control?

### Answers

1. The switch's MAC address (CAM) table; when full, a fail-open switch floods unknown-unicast traffic to all ports, letting an attacker on any port sniff it.
2. They stop learning new MACs when the table is full but keep existing entries and forward their traffic correctly, so the attacker does not gain a sniffing position.
3. It caps the number of source MAC addresses per port, so a flood from one port trips the limit and is dropped, logged or the port is disabled before the table can fill.
4. One port sourcing thousands of distinct MAC addresses, or a surge of flooded unknown-unicast traffic, is an obvious anomaly in switch counters or a sensor.
5. It only limits and optionally pins MAC addresses, which are forgeable; it does not cryptographically verify who or what is connected.

## Further reading

- Cisco, Configuring Port Security, the reference for the control and its violation modes.
- MITRE ATT&CK, Network Sniffing (T1040): https://attack.mitre.org/techniques/T1040/
- NSA, Network Infrastructure Security Guide (2022), access-layer hardening: https://media.defense.gov/2022/Jun/15/2003018261/-1/-1/0/CTR_NSA_NETWORK_INFRASTRUCTURE_SECURITY_GUIDE_20220615.PDF
