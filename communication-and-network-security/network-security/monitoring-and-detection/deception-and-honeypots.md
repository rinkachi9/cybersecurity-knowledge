# Deception and honeypots

## Summary

Deception is a defensive technique that plants fake but attractive assets (honeypots, decoy services, bogus credentials, honeytokens) so that any interaction with them is, by definition, suspicious, since no legitimate user has any reason to touch them. This gives extremely high-fidelity detection with almost no false positives, which is the opposite problem to most network detection. Deception is especially good at catching the quiet activity, reconnaissance, [lateral movement](../network-attacks/lateral-movement.md), credential reuse, that blends into normal traffic and evades behavioral detection. It does not replace other controls; it is a low-noise tripwire layer that tells you an attacker is present and inside.

## Prerequisites

- [Network security monitoring](network-security-monitoring.md): deception complements it.
- [Lateral movement](../network-attacks/lateral-movement.md) and [network scanning](../network-attacks/network-scanning.md): what decoys catch.
- [Network segmentation](../architecture/network-segmentation.md): where decoys are placed.

## Core concepts

### Definition

*Deception technology* places decoy assets and data designed to attract and detect attackers. A *honeypot* is a decoy system with no production purpose, so any connection to it is suspect. A *honeytoken* is a piece of fake data (a credential, a file, an API key, a database record) that is monitored, so any use of it reveals an intruder. The defining property is a near-zero false-positive rate: legitimate users have no reason to interact with decoys.

### Analogy

Deception is marking a few banknotes and leaving a decoy wallet in the office. No honest employee touches the decoy wallet or spends the marked notes, so if either moves, you know a thief is present and you learn where they went. It does not stop theft by itself, but it is an almost false-alarm-free way to discover a thief who otherwise blends in with the staff.

The analogy holds closely; it carries the essential point that the signal is clean precisely because the bait has no legitimate use.

### Why the signal is so clean

Most network detection fights false positives: distinguishing malicious from legitimate traffic is hard because they look alike. Deception inverts this. A honeypot has no users and no purpose, so a single connection to it is a high-confidence indicator with essentially no benign explanation. A honeytoken credential that is never used by any real process, if it authenticates somewhere, was stolen and tried by an attacker. This makes deception alerts worth acting on immediately, unlike the tuning-heavy alerts of behavioral systems.

### Types

| Deception | What it is | Catches |
| --- | --- | --- |
| Low-interaction honeypot | Emulated service (fake open port/banner) | [Scanning](../network-attacks/network-scanning.md), automated attacks |
| High-interaction honeypot | Real (sandboxed) system | Hands-on attacker behavior, tooling, intent |
| Honeytoken credential | Fake account/credential, monitored | Credential theft and reuse, [lateral movement](../network-attacks/lateral-movement.md) |
| Honeytoken file/record | Bait document, database row, API key | [Exfiltration](../network-attacks/data-exfiltration.md), insider access |
| Decoy network assets | Fake shares, hosts, DNS entries | Discovery and lateral movement in the network |

*Interaction level* trades realism for risk: low-interaction is safe and simple but limited; high-interaction reveals more but is a real system that must be carefully isolated so it cannot be used as a foothold.

### Placement and purpose

Deception is most valuable inside the network, placed where an attacker would look during [lateral movement](../network-attacks/lateral-movement.md): decoy hosts and shares in [segments](../architecture/network-segmentation.md) alongside real assets, honeytoken credentials seeded on workstations, bait records in databases. An attacker performing internal reconnaissance or credential harvesting is very likely to encounter a decoy, and the moment they do, the defender gets a clean, early signal that an intruder is inside, often before the real objective is reached.

A classic caution: a honeypot must not become a stepping stone. High-interaction honeypots are real systems; if not strictly isolated and monitored, an attacker can use one to pivot into the real network.

## Worked example

Deception catching a lateral-movement attempt (conceptual; the principle, not a lab run):

1. **Seeding.** The defender places a decoy "file server" (`fileserver-backup`, a low-interaction honeypot) in the server segment, and seeds honeytoken credentials for a fake admin account on several workstations, plus a bait "passwords.xlsx" on a decoy share. None are used by any legitimate process, and all are monitored.
2. **Attacker reconnaissance.** A compromised workstation's attacker scans the segment and sees `fileserver-backup`. Because no real user ever connects to it, the first connection attempt raises a high-confidence alert, early in the intrusion, before the real file server is touched.
3. **Credential bait.** The attacker dumps credentials from the workstation and finds the honeytoken admin account. When they try to use it, the authentication of a credential that no real process ever uses fires an unambiguous alert and shows exactly where they tried it.
4. **Response.** The clean, early signals let the team confirm an active intrusion and respond (isolate the host, scope via [NSM](network-security-monitoring.md) data) while the attacker is still in the reconnaissance/lateral-movement stage.

Contrast with behavioral detection alone, which might have flagged the scanning as a low-confidence anomaly among normal traffic; the decoy turned it into a certainty.

## Trade offs and when to use it

- **High fidelity vs no prevention.** Deception gives near-false-positive-free detection but prevents nothing by itself; it is a tripwire layer on top of real controls. Use it to detect, not to defend.
- **Interaction level: realism vs risk.** High-interaction honeypots reveal attacker behavior but are real systems needing strict isolation; low-interaction is safe but limited. Choose by capacity to isolate and monitor.
- **Coverage vs maintenance.** Deception must be realistic and maintained to stay convincing and to avoid confusing operations; stale or obvious decoys lose value. It is an addition for maturing programs, not a first control.
- **Catches the quiet stages.** Its best value is detecting reconnaissance, lateral movement and credential reuse that blend in, so place it where those occur (internally), not only at the perimeter.

## Common mistakes

- **Treating deception as prevention.** It detects, it does not stop. Fix: use as a detection layer over real controls.
- **Unisolated high-interaction honeypots.** They become a real foothold. Fix: strict isolation and monitoring, or prefer low-interaction.
- **Obvious or stale decoys.** Attackers ignore them and they confuse staff. Fix: make decoys realistic and maintained; document them for operations.
- **Decoys only at the perimeter.** Misses the internal stages where deception shines. Fix: seed decoys and honeytokens inside, where lateral movement happens.
- **No response plan for a deception alert.** A high-fidelity alert wasted. Fix: deception alerts are high priority; have a response ready.

## Practice

1. Why do deception technologies have such a low false-positive rate?
2. What is the difference between a honeypot and a honeytoken?
3. Why is deception especially good at catching lateral movement and reconnaissance?
4. What is the risk of a high-interaction honeypot, and how is it managed?
5. Why is deception a detection layer rather than a preventive control?

### Answers

1. Decoys have no legitimate purpose or users, so any interaction with them has essentially no benign explanation and is therefore a high-confidence indicator of an attacker.
2. A honeypot is a decoy system with no production use; a honeytoken is a piece of fake monitored data (a credential, file, key or record) whose use reveals an intruder.
3. Those stages involve attackers exploring internal assets and reusing credentials, activities that are very likely to touch a seeded decoy or token, turning quiet, blend-in activity into a clean early alert.
4. It is a real system that an attacker could use as a stepping stone into the real network; it is managed by strict isolation and close monitoring, or avoided in favor of low-interaction decoys.
5. It plants bait that reveals an attacker's presence but does nothing to block their actions, so it detects intrusions (very reliably) but must sit on top of real preventive controls.

## Further reading

- MITRE Engage (formerly MITRE Shield), the adversary-engagement and deception knowledge base: https://engage.mitre.org/
- The Honeynet Project, research and tools for honeypots: https://www.honeynet.org/
- Spitzner, L., Honeypots: Tracking Hackers (the foundational text) and SANS honeytoken guidance.
- [Lateral movement](../network-attacks/lateral-movement.md) and [network security monitoring](network-security-monitoring.md) for what deception complements.
