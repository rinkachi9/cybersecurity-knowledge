# Lateral movement

## Summary

Lateral movement is how an attacker, having compromised one host, spreads to others to reach their real objective (data, domain control, critical systems). It is the stage where a single foothold becomes a serious breach, and it happens east-west, inside the network, where traditional perimeter defenses do not look. On the network, lateral movement uses the administrative and file-sharing protocols that are allowed to flow between hosts (SMB, RDP, WinRM, SSH) together with stolen or reused credentials, and often pivoting and tunneling through compromised hosts. The network defenses are segmentation and microsegmentation (remove the paths), east-west monitoring (see the movement), and controlling the protocols that enable it.

## Prerequisites

- [Network segmentation](../architecture/network-segmentation.md) and [microsegmentation](../architecture/microsegmentation.md): the main defenses.
- [Network security monitoring](../monitoring-and-detection/network-security-monitoring.md): seeing east-west traffic.
- [Privilege escalation](../../../security-operations/threats-and-attacks/attack-lifecycle/privilege-escalation.md) and [credential attacks](../../../identity-and-access-management/credential-attacks/README.md).

Authorized use only. Framed for detection and defense.

## Core concepts

### Definition

*Lateral movement* (MITRE ATT&CK tactic TA0008) is the set of techniques an attacker uses to move from an initial compromised host to other systems within the environment, typically reusing credentials and using legitimate administrative protocols, to progress toward their objective.

### Analogy

An intruder who gets through one window of a building rarely wants that room; they want the safe. Lateral movement is moving room to room using the building's own internal doors and the keys found on desks, rather than breaking in from outside each time. Because they use internal doors with found keys, the outer walls and the front-door guard (the perimeter) never see them. Locking internal doors and giving each key access to only one room (segmentation and least privilege) is what traps them in the first room.

The analogy holds closely; it breaks in that network "internal doors" are protocols that often appear legitimate, so the movement blends with normal administration unless you are watching east-west.

### Why it is a network problem

Most security investment historically watched the perimeter (north-south). Lateral movement is east-west: host to host inside the network. On a flat network where every host can reach every other on administrative ports, one foothold can reach everything, and the traffic looks like ordinary administration. This is why [segmentation](../architecture/network-segmentation.md) and east-west monitoring are the core network defenses, not the perimeter firewall.

### How it moves, on the network

| Protocol / method | Use in lateral movement | Note |
| --- | --- | --- |
| SMB (445) | File shares, remote execution (PsExec-style), admin shares | The classic Windows path; wormable (see [legacy protocols](../core-protocols/insecure-legacy-protocols.md) on SMBv1) |
| RDP (3389) | Interactive remote desktop | Credential reuse; often exposed too widely |
| WinRM / WMI (5985/5986) | Remote PowerShell and management | Blends with legitimate admin |
| SSH (22) | Remote shell, key reuse, agent/key hopping | Key sprawl aids it ([SSH security](../secure-transport/ssh-security.md)) |
| Remote services (T1021) | Generic: use valid credentials over remote-access protocols | MITRE ATT&CK T1021 |

Credential techniques feed these: pass-the-hash, pass-the-ticket, and reuse of local admin passwords shared across machines. The network sees the resulting connections; the credential theft is an endpoint and identity concern, so defense is layered across both.

### Pivoting and tunneling

When an attacker cannot reach a target directly, they *pivot*: route traffic through a compromised host that can. This often uses *tunneling* (SOCKS proxies, SSH port forwarding, protocol tunneling, MITRE T1572) to carry their tools' traffic through an allowed channel, reaching segments the attacker's own position cannot. Egress and internal filtering plus monitoring for unexpected tunnels counter this.

## Worked example

An attacker phishes a workstation and moves toward the domain controllers:

1. **Foothold.** Malware runs on workstation A. Nothing valuable is there; the attacker needs to move.
2. **Discovery.** From A, they scan the local segment for other hosts and open admin ports (SMB, RDP). On a flat network, they see hundreds of reachable hosts.
3. **Credential reuse.** They dump cached credentials from A and find a local admin password reused across many machines (or a cached domain credential). Using pass-the-hash over SMB, they execute code on workstation B and file server C, all over allowed protocols, looking like administration.
4. **Toward the objective.** Reusing harvested credentials, they reach a server with a path to the domain controllers and escalate.
5. **With network defenses.** On a [segmented and microsegmented](../architecture/microsegmentation.md) network, workstation A cannot reach other workstations on SMB/RDP at all (east-west blocked), so step 2 finds almost nothing; admin protocols are allowed only from [management jump hosts](../architecture/management-plane-security.md); and east-west [monitoring](../monitoring-and-detection/network-security-monitoring.md) alerts on A suddenly making SMB connections to many hosts. The foothold is trapped in the first room.

The example shows the division of defense: identity controls (unique local admin passwords, no credential reuse) and network controls (segmentation, east-west monitoring, restricting admin protocols) together break the chain; neither alone is enough.

## Detection and mitigation

- **Segmentation and microsegmentation.** Remove the east-west paths: workstations should not reach each other on admin ports; servers accept admin protocols only from jump hosts. This is the single most effective network control. See [microsegmentation](../architecture/microsegmentation.md).
- **East-west monitoring.** Deploy sensors and [flow monitoring](../monitoring-and-detection/flow-monitoring.md) internally, not just at the edge; alert on a host making many SMB/RDP/WinRM connections, new admin-protocol paths, and internal scanning.
- **Restrict admin protocols.** Allow SMB/RDP/WinRM/SSH only where needed and only from controlled sources; disable SMBv1; require SMB signing (also stops [NTLM relay](../core-protocols/local-name-resolution-poisoning.md)).
- **Identity hygiene (complementary).** Unique local admin passwords (LAPS), no credential reuse, tiered admin accounts, so a credential found on one host does not open others.
- **Detect tunneling and pivoting.** Watch for unexpected internal tunnels and proxies ([egress filtering](../traffic-filtering/egress-filtering.md), protocol anomaly detection).

## Trade offs and when to use it

- **Segmentation effort vs containment.** Tightly restricting east-west admin traffic is the strongest control but requires knowing legitimate admin paths; use observe-then-enforce. The payoff, turning a foothold into a contained incident, is large.
- **Monitoring coverage vs cost.** East-west monitoring needs internal sensors and generates data; prioritize sensors at segment boundaries and high-value zones.
- **Network vs identity defense.** Network controls remove paths; identity controls remove reusable credentials. Both are needed; neither substitutes for the other.

## Common mistakes

- **Flat internal network.** One foothold reaches everything over admin protocols. Fix: segment and microsegment, especially blocking workstation-to-workstation admin traffic.
- **Only perimeter monitoring.** Lateral movement is east-west and invisible to edge sensors. Fix: internal flow and traffic monitoring.
- **Admin protocols allowed broadly.** SMB/RDP/WinRM reachable everywhere. Fix: restrict to jump hosts and needed paths; disable SMBv1; require SMB signing.
- **Reused local admin passwords.** One stolen hash opens many machines. Fix: unique per-host admin passwords (LAPS), tiered accounts.
- **Ignoring tunneling.** Attackers pivot through allowed channels. Fix: egress control and tunnel/anomaly detection.

## Practice

1. Why is lateral movement an east-west problem that perimeter defenses miss?
2. Which protocols are commonly used for lateral movement, and why do they blend in?
3. How does credential reuse amplify lateral movement, and what network control limits it even so?
4. What is pivoting, and how does tunneling assist it?
5. What is the single most effective network control against lateral movement, and why?

### Answers

1. It occurs between internal hosts (east-west), using internal admin protocols and found credentials, so it never crosses the perimeter where traditional defenses watch (north-south).
2. SMB, RDP, WinRM/WMI and SSH; they are legitimate administrative protocols normally allowed between hosts, so attacker use of them looks like ordinary administration.
3. A credential (or hash) found on one host that is valid on others lets the attacker authenticate across machines without new exploits; segmentation limits this by removing the network paths so the reusable credential has nowhere to reach even if valid.
4. Pivoting routes the attacker's traffic through a compromised host to reach systems they cannot contact directly; tunneling (SOCKS, SSH forwarding, protocol tunneling) carries their tools' traffic through an allowed channel to those systems.
5. Segmentation/microsegmentation that removes east-west admin paths (especially workstation-to-workstation), because it prevents the attacker from reaching other hosts in the first place, turning a foothold into a contained incident.

## Further reading

- MITRE ATT&CK, Lateral Movement tactic (TA0008) and Remote Services (T1021): https://attack.mitre.org/tactics/TA0008/
- Microsoft, Local Administrator Password Solution (LAPS) and the tiered administration model.
- [Microsegmentation](../architecture/microsegmentation.md) and [network security monitoring](../monitoring-and-detection/network-security-monitoring.md) for the core defenses.
- NSA/CISA guidance on preventing lateral movement and on SMB hardening.
