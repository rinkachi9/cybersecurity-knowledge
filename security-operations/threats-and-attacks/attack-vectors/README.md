# Attack vectors

## Summary

An attack vector is the path or method an attacker uses to reach a target and deliver an attack: an exposed service, a phishing email, a stolen password, a poisoned update, a USB stick, a Wi-Fi network, a trusted partner connection. Counting and shrinking vectors is the practical side of reducing the attack surface. The term has two common meanings that are easy to mix up. In threat analysis it means the route into an organization. In CVSS it is a metric (AV) that describes how a specific vulnerability can be reached, and that metric is not the same thing as the delivery route. This note separates the two, lists the vectors with MITRE ATT&CK Initial Access techniques, runs a small exposure analysis and ends with the controls that remove a vector instead of reacting to it.

## Prerequisites

- [Threats and attacks overview](../threats-and-attacks-overview.md) and [attack categorization](../attack-categorization.md), which group attacks by vector, technique, objective and actor.
- [CVSS](../../vulnerability-management/cvss.md) for the Attack Vector metric.
- [Attack lifecycle](../attack-lifecycle/README.md), because a vector is the entry step of the lifecycle.
- [Defense in depth](../../../security-architecture-and-engineering/design-principles/defense-in-depth.md).

## Core concepts

### Definition

*Attack vector* (threat view): the route by which an adversary gains the access or delivers the payload needed for an attack, such as network services, email, removable media or a supplier. NIST's glossary lists several definitions of the term from different publications; I did not retrieve them for this note, so the definition here is a working one. The NIST definition of an advanced persistent threat (see [APTs](../advanced-persistent-threats/README.md)) uses the term when it says the adversary combines "multiple attack vectors, such as cyber, physical, and deception".

*Attack vector* (CVSS view): the base metric AV of CVSS v3.1, which "reflects the context by which vulnerability exploitation is possible" (FIRST CVSS v3.1 specification, checked 2026-10). Its values and weights:

| Value | Weight | Meaning |
| --- | --- | --- |
| Network (N) | 0.85 | The attack can be launched remotely across a network, potentially from anywhere, including across multiple hops |
| Adjacent (A) | 0.62 | The attack uses the network stack but is limited to a logically adjacent topology, such as the same subnet or administrative domain |
| Local (L) | 0.55 | The attack does not use the network stack. It relies on local or remote read, write or execute access, or on a user being tricked into acting |
| Physical (P) | 0.2 | The attacker must physically touch or manipulate the vulnerable component |

*Attack surface* is the set of all vectors and exposed points; *attack path* is a specific sequence of steps through them. A vector is one entry, a path is the whole chain.

### Analogy

A building has doors, windows, a loading dock, a fire escape, a delivery entrance and staff with keys. Each is an entry route. Security means counting the routes, closing the ones that need not exist and guarding the rest. CVSS "attack vector" is different: it is the question "from where can someone operate this specific lock", not "which door do burglars use". The analogy breaks because digital doors are created by software changes, so the count changes daily.

### Why the distinction matters

A phishing email is a delivery vector. The vulnerability exploited by the attachment can be rated AV:L in CVSS, because the user opens the file on the local machine, even though the attacker came in over the network. So a vulnerability with a Local vector can be reached from the internet if the delivery vector is email. If you filter your remediation queue by AV:N only, you miss it. Likewise a vulnerability rated AV:N on an internal-only server is not exposed to an outsider until a path exists. The CVSS metric measures the exploit mechanism, and the exposure of the asset comes from the threat view.

### Catalog of vectors

MITRE ATT&CK lists 11 techniques in the Initial Access tactic (TA0001, checked 2026-10). They form a practical catalog of entry vectors:

| Vector | ATT&CK technique | What it means |
| --- | --- | --- |
| Public-facing applications and services | T1190 Exploit Public-Facing Application | A bug or misconfiguration in an internet-facing host |
| Remote access services | T1133 External Remote Services | VPNs, Citrix and similar services used to gain or keep access |
| Email and messaging | T1566 Phishing (sub-techniques .001 to .004) | Deceptive messages with social engineering |
| Web | T1189 Drive-by Compromise | A user visiting a site receives exploit code |
| Web traffic injection | T1659 Content Injection | Malicious content inserted into network traffic |
| Credentials | T1078 Valid Accounts (.001 to .004) | Existing credentials abused |
| Third parties | T1199 Trusted Relationship | A supplier or partner with access is breached or abused |
| Supply chain | T1195 Supply Chain Compromise (.001 to .003) | Products or delivery tampered with, see [supply-chain attacks](../../../software-development-security/application-security/supply-chain/supply-chain-attacks/README.md) |
| Removable media | T1091 Replication Through Removable Media | Malware spread by USB and similar, including to air-gapped systems |
| Hardware | T1200 Hardware Additions | A device introduced to give access |
| Wireless | T1669 Wi-Fi Networks | Open or credentialed target networks, requiring physical proximity |

Beyond Initial Access, the threat view also includes insiders (an actor who already has legitimate access), physical intrusion and social engineering by phone or in person. For the human vectors see [social engineering](../../../security-and-risk-management/security-awareness/social-engineering/README.md), [tailgating](../../../security-and-risk-management/security-awareness/social-engineering/tailgating.md) and [business email compromise](../business-email-compromise/README.md).

### Grouping vectors

Three groupings are common and useful together.

| Grouping | Categories | Use |
| --- | --- | --- |
| By access needed | Remote with no foothold, remote with credentials, adjacent, local, physical | Prioritization of exposure |
| By target | Technology, people, process, third parties | Control ownership |
| By direction | Inbound (to us), outbound (user pulls content), lateral (inside) | Where to put detection |

### Reducing a vector

There are three moves, in order of effectiveness.

1. **Remove it.** Close unused ports and services, retire unused applications, disable macros and autorun, remove stale accounts and VPN profiles. A vector that does not exist cannot be attacked.
2. **Narrow it.** Put the service behind a gateway or zero trust access ([zero trust](../../../communication-and-network-security/network-security/nist-zero-trust-architecture.md)), restrict by identity and device, segment the network and add MFA.
3. **Watch it.** Log and alert on the remaining vectors, patch them first and test them through [red, blue and purple team](../../../security-assessment-and-testing/red-blue-purple-teams.md) exercises.

Use [asset management](../../../asset-security/asset-management/README.md) to find the vectors, because an unknown asset is an unmanaged vector, and attack surface management ([CASM](../../attack-surface-management/cloud-attack-surface-management/README.md)) to see them from the outside.

## Worked example

The script `scripts/vector-exposure.py` groups seven synthetic findings by CVSS Attack Vector and by entry path, and extracts the findings that an outsider can use without a foothold. The CVSS weights come from the specification. Python 3.10, standard library only. The output is real.

```bash
python3 scripts/vector-exposure.py
```

Output:

```text
by CVSS Attack Vector metric:
  Network   weight 0.85 -> ['F-1', 'F-2', 'F-3']
  Adjacent  weight 0.62 -> ['F-5']
  Local     weight 0.55 -> ['F-4', 'F-7']
  Physical  weight 0.20 -> ['F-6']
usable without any foothold (AV:N and PR:N): ['F-1', 'F-2']
findings per entry path: {'external remote service': 1, 'public-facing application': 2, 'phishing attachment': 1, 'internal network': 1, 'physical access': 1, 'supply chain / CI': 1}
assets reachable by an outsider: ['vpn-gw-1', 'web-shop']
```

What the output shows:

1. Three findings have the Network vector, but only two (`F-1` on a VPN gateway and `F-2` on a web shop) also need no privileges (`PR:N`). `F-3` is network reachable but needs low privileges, so it becomes an outsider risk only after an account is obtained. The first filter that matters for exposure is AV:N together with PR:N.
2. `F-4`, the phishing attachment, is rated Local by CVSS. A queue filtered only by Network would not show it. The entry path column catches it. This is the CVSS-versus-delivery difference in practice.
3. `F-7` is on a build runner, a Local vulnerability on the supply chain path. It is serious because a compromise of the pipeline reaches every artifact it builds, not because of its CVSS vector.
4. `F-6` has the lowest weight (Physical, 0.2), but on a kiosk in a public area the physical vector is cheap for an attacker. Context overrides the metric.

Remediation order from this output: `F-1` and `F-2` first (remote, no privileges), then the credential or privilege chain for `F-3`, then the phishing vector with email controls and patching of the client, then `F-7` and `F-6` by asset criticality and context.

## Trade offs and when to use it

**Benefits of a vector view.** It turns an unbounded list of vulnerabilities into a short list of routes, and it shows where one control closes many risks (for example blocking macros from the internet removes a whole class of phishing payloads).

**Limits.**

- A catalog is a checklist. Attackers combine vectors, so the path matters more than the single entry.
- CVSS AV is a technical metric and not an exposure measure. Use exposure (reachability), exploit availability and asset value too. See [vulnerability remediation](../../vulnerability-management/vulnerability-remediation/README.md).
- New vectors appear with new technology: SaaS integrations, OAuth consent, browser extensions, AI assistants with tool access (see [adversarial AI](../../../security-architecture-and-engineering/ai-security/adversarial-machine-learning/README.md)).
- Counting vectors can mislead when the attack is a small variation of an existing one.

**Alternatives.** Threat modeling (STRIDE, attack trees) starts from assets and finds the vectors, see [attack trees](../../../security-and-risk-management/threat-modeling/methods/attack-trees.md). The attack lifecycle view places the vector in time. Use the vector view for exposure reviews and the lifecycle view for detection coverage.

## Common mistakes

| Mistake | Effect | Fix |
| --- | --- | --- |
| Equating the CVSS Attack Vector with the delivery route | Phishing-delivered Local flaws are deprioritized | Track both, reachability and delivery |
| Counting only internet-facing assets | Misses insiders, partners, physical and supply chain | Use the full catalog |
| Treating the perimeter as the only vector | Credentials and SaaS bypass it | Add identity and third-party vectors |
| Ignoring unknown assets | They carry unmanaged vectors | Asset discovery, see [asset management](../../../asset-security/asset-management/README.md) |
| Closing a vector without watching it | Silent re-opening, such as a service re-enabled | Continuous attack surface monitoring |
| Assuming air gaps close the vector | Removable media (T1091) crosses them | Media control and scanning |
| Treating the vector list as complete | New integrations create new vectors | Review the catalog yearly |

Detection and mitigation: each vector has a detection data source (email gateway logs for phishing, web server and WAF logs for public applications, VPN and identity logs for remote services, endpoint logs for removable media, asset and certificate inventories for third-party and supply chain). The mitigation for the whole topic is the three moves above: remove, narrow, watch.

## Practice

1. Classify these by ATT&CK Initial Access technique: an exposed admin panel, a stolen VPN password, a USB drive dropped in a car park, a breached managed service provider.
2. A flaw in a PDF reader is rated AV:L. Under what delivery vector can it be attacked from the internet?
3. In the worked example, why is `F-3` not in the "no foothold" list, and what event would move it there?
4. List the three moves for reducing a vector, with one example each for a VPN.
5. Extend the script to sort findings by `AV weight` multiplied by a simple criticality score per asset. What does the ranking miss?
6. Which CISSP sections touch this topic?

**Answers and hints**

1. T1190, T1078 (or T1133 for the VPN service), T1091 and T1199.
2. Email (T1566) or a drive-by web page (T1189), both of which cause the user to open the file locally.
3. It needs low privileges (`PR:L`). An attacker obtaining any account, for example by phishing or credential stuffing, would turn it into a usable finding.
4. Remove: decommission VPN profiles that are not used. Narrow: require phishing-resistant MFA and device posture. Watch: alert on VPN logins from new countries and on new VPN accounts.
5. It ignores exploit availability and the lateral chain, which a path analysis would add.
6. Sections 1.9 (threat and vulnerability identification), 1.10 (threat modeling), 3.1 (secure design principles), 4.1 (network architecture and segmentation), 7.7 (detective and preventive measures) and 7.8 (vulnerability management). See [CISSP security domains](../../../security-and-risk-management/reference/certifications/cissp-security-domains.md).

## Further reading

- MITRE ATT&CK, [Initial Access (TA0001)](https://attack.mitre.org/tactics/TA0001/): the 11 techniques used as the catalog.
- FIRST, [CVSS v3.1 specification](https://www.first.org/cvss/v3.1/specification-document): the Attack Vector metric and its weights.
- NIST CSRC glossary, [attack vector](https://csrc.nist.gov/glossary/term/attack_vector): several definitions from NIST publications. The page could not be retrieved during this check.
- [CVSS](../../vulnerability-management/cvss.md) and [attack categorization](../attack-categorization.md) in this repository.
