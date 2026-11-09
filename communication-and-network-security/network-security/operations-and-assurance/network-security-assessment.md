# Network security assessment

## Summary

A network security assessment is the structured evaluation of a network's security: finding what is exposed, what is misconfigured, and what an attacker could do. It spans several activities with different depth and authorization: architecture and firewall-rule review (on paper and in configs), vulnerability scanning (automated discovery of known weaknesses), and penetration testing (authorized simulation of an attack). The output is a prioritized set of findings that feeds remediation. The non-negotiable foundation of any active assessment is authorization: scope, rules of engagement and written permission, because the same actions, without them, are an attack. Assessment is how an organization learns its real exposure before an attacker does.

## Prerequisites

- [Network scanning](../network-attacks/network-scanning.md) and [firewall rule design](../traffic-filtering/firewall-rule-design/README.md): techniques used in assessment.
- [Vulnerability management](../../../security-operations/vulnerability-management/README.md): where findings go.
- [Network segmentation](../architecture/network-segmentation.md): a common review target.

Authorized use only. Every active technique here requires written authorization and a defined scope.

## Core concepts

### Definition

A *network security assessment* is an evaluation of a network's security posture to identify vulnerabilities, misconfigurations and exposure, and to measure the effectiveness of controls. It ranges from passive review (reading configurations and architecture) to active testing (scanning, penetration testing).

### Analogy

Assessment is a building safety inspection plus a hired, authorized burglar. The inspector reviews the blueprints and checks that doors and locks match code (architecture and config review). A scanner walks the building noting every unlocked door (vulnerability scan). The authorized burglar actually tries to break in within agreed rules to show what a real intruder could reach (penetration test). All three are done with the owner's written permission and a clear scope; the same burglar without permission is a criminal.

The analogy holds closely; it carries the central point that authorization and scope are what separate assessment from attack.

### The spectrum of assessment

| Activity | What it does | Depth | Authorization |
| --- | --- | --- | --- |
| Architecture review | Evaluate design: zones, flows, trust boundaries | Design-level, no touching | Internal, low risk |
| Configuration / firewall-rule review | Read device and firewall configs for weaknesses | Detailed, passive | Access to configs |
| Vulnerability scanning | Automated discovery of known vulnerabilities and exposure | Broad, shallow | Scope and schedule; can disrupt |
| Penetration testing | Authorized simulation of an attack, including exploitation | Deep, narrow | Strict scope, rules of engagement, written permission |
| Red teaming | Goal-based, stealthy, full-scope adversary emulation | Deepest, holistic | Tightly controlled, executive sponsor |

They are complementary: architecture review finds design flaws a scan cannot see; scanning finds known vulnerabilities at breadth; penetration testing shows what is actually exploitable and chainable; red teaming tests detection and response as well.

### Firewall and architecture review

Much high-value assessment is passive. Reviewing [firewall rules](../traffic-filtering/firewall-rule-design/README.md) finds overly broad allows, [shadowed and redundant rules](../traffic-filtering/firewall-rule-design/README.md), and exposed management, often without sending a packet. Reviewing architecture checks that [segmentation](../architecture/network-segmentation.md) matches intent, that the [management plane](../architecture/management-plane-security.md) is isolated, and that trust boundaries are enforced. These reviews find systemic issues that point-in-time scans miss.

### Authorization and rules of engagement

Active assessment is distinguished from attack only by authorization. Before any active testing:

- *Scope*: exactly which systems, addresses and times are in and out of bounds.
- *Rules of engagement*: what techniques are allowed (e.g. no denial-of-service, no social engineering unless agreed), how to handle sensitive data found, and emergency contacts.
- *Written permission* from someone authorized to grant it.
- *Deconfliction*: the operations team knows a test is happening (or, for red teams, a small trusted group does), so a real incident during the test is not missed.

Skipping these is both dangerous (unexpected outages, legal exposure) and, externally, illegal.

### From findings to remediation

An assessment's value is in acting on it. Findings are prioritized by risk (severity and exposure), assigned owners, and tracked to closure, feeding [vulnerability management](../../../security-operations/vulnerability-management/README.md). An assessment whose report is filed and forgotten changed nothing. Re-testing confirms fixes worked.

## Worked example

Assessing a segmented network before a compliance audit (combining passive and active, all authorized and scoped):

1. **Architecture review.** The assessor reviews the [segmentation](../architecture/network-segmentation.md) design and flow matrix, confirming the DMZ, server and management zones and their intended boundaries.
2. **Firewall-rule review.** Reading the firewall configs with the [anomaly audit approach](../traffic-filtering/firewall-rule-design/README.md), they find a shadowed deny and an over-broad "any-any" rule left from a migration, exposing more than intended, found without a single packet.
3. **Vulnerability scan.** An authorized, scheduled scan of the in-scope ranges finds unpatched services and a device still running [SNMPv1 with a default community string](../core-protocols/insecure-legacy-protocols.md).
4. **Penetration test.** Within strict scope and rules of engagement, the tester confirms that the over-broad firewall rule plus the SNMP exposure would let an attacker reach the management network, demonstrating real, chained impact that the individual scan findings understated.
5. **Validate segmentation.** They test from each zone that forbidden destinations are truly unreachable, a core segmentation test (and a PCI DSS requirement).
6. **Report and remediate.** Findings are prioritized (the management-network path first), assigned, fixed, and re-tested to confirm closure.

The example shows the layers working together: passive review found the systemic rule flaws cheaply, scanning found the known weaknesses broadly, and the (authorized) penetration test showed what they meant in combination.

## Trade offs and when to use it

- **Passive vs active.** Architecture and config review are low-risk, cheap and find systemic issues; active testing (scanning, pen testing) shows real exploitability but can disrupt and needs strict authorization. Use passive broadly and often, active with care.
- **Breadth vs depth.** Vulnerability scanning is broad and automated (run regularly); penetration testing is deep and narrow (periodic, scoped). Each covers the other's gap.
- **Point-in-time vs continuous.** A single assessment is a snapshot; networks change. Fix: regular scanning and periodic testing, plus continuous monitoring.
- **Internal vs third-party.** Internal teams know the environment; third parties bring independence and attacker perspective. Alternate or combine.

## Common mistakes

- **Active testing without authorization and scope.** Causes outages and legal exposure; externally illegal. Fix: written permission, scope, rules of engagement, deconfliction, always.
- **Scanning as the whole assessment.** Misses design flaws and real exploitability. Fix: add architecture and config review and periodic penetration testing.
- **One-off assessments.** A snapshot that decays. Fix: regular scanning, periodic testing, continuous monitoring.
- **Not testing segmentation.** Assuming boundaries hold without verifying. Fix: test from each zone that forbidden paths are blocked.
- **Reports that are filed, not acted on.** No risk reduction. Fix: prioritize, assign, track to closure, re-test.

## Practice

1. What single factor distinguishes a network security assessment from an attack?
2. Why are architecture and firewall-rule review valuable even though they send no packets?
3. How do vulnerability scanning and penetration testing complement each other?
4. What must be defined before any active testing, and why does deconfliction matter?
5. Why is a one-off assessment insufficient?

### Answers

1. Authorization: written permission with a defined scope and rules of engagement; the same active techniques without them are an attack.
2. They find systemic design and configuration flaws (over-broad or shadowed rules, poor segmentation, exposed management) that point-in-time scans cannot see, cheaply and without risk of disruption.
3. Scanning is broad and automated, finding known vulnerabilities across many systems; penetration testing is deep and narrow, showing which findings are actually exploitable and chainable into real impact.
4. Scope, rules of engagement and written permission; deconfliction (the operations team knowing a test is happening) matters so that a real incident occurring during the test is not mistaken for the test and missed.
5. Networks change constantly (new systems, new rules, new vulnerabilities), so a single assessment is a decaying snapshot; regular scanning, periodic testing and continuous monitoring are needed.

## Further reading

- NIST SP 800-115, Technical Guide to Information Security Testing and Assessment: https://doi.org/10.6028/NIST.SP.800-115
- PTES (Penetration Testing Execution Standard) and the OSSTMM for methodology.
- [Vulnerability management](../../../security-operations/vulnerability-management/README.md) and [firewall rule design](../traffic-filtering/firewall-rule-design/README.md) for where findings come from and go.
- PCI DSS segmentation testing requirements for the segmentation-validation angle.
