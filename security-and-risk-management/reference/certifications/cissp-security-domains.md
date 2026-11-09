# CISSP security domains

## Summary

The CISSP common body of knowledge is split into eight domains. ISC2 publishes the split in the *CISSP Certification Exam Outline*, together with 62 numbered sections that name what a candidate must understand and the average weight of each domain on the exam. This repository uses the same eight domains as its top level directories, so the outline is also the map of this knowledge base. This note explains what each domain covers, how the weights work, where the boundaries between domains are blurry and where each topic lives in the repository.

## Prerequisites

- [The CISSP certification](cissp.md) for the exam format, experience rules and what the credential claims to prove.
- [Security overview](../../foundations/security-overview.md) and the [CIA triad](../../foundations/cia-triad/README.md), because Domain 1 starts from them.

## Core concepts

### Definition

A *CISSP domain* is one of eight named areas of the CISSP body of knowledge. Each domain has a number, a fixed list of numbered sections (1.1, 1.2 and so on) and an average exam weight. The sections are statements of the form "Understand ...", "Apply ...", "Implement ..." or "Design ...", which signal the cognitive level the exam targets. A domain is a scope statement, not a curriculum: the outline lists topics, and says nothing about depth or order of study.

A domain is not an ISO taxonomy and not a standard. It is the content outline of one certification, maintained by ISC2 through a periodic Job Task Analysis, a survey of what working practitioners do.

### Analogy

Think of the outline as the table of contents of a reference library that has eight rooms. Every book belongs to one room because of its main question, but a book about locks can be useful in the room about buildings and in the room about people. The catalog tells you where to shelve a book. It does not claim that the rooms are independent.

The analogy breaks at the exam: a real exam question often crosses rooms. A scenario about a cloud outage can touch Domain 3 (architecture), Domain 7 (recovery) and Domain 1 (business continuity requirements) at once.

### The eight domains and their weights

Checked against the *CISSP Certification Exam Outline*, effective April 15, 2024 (ISC2, document version v9/2024), 2026-10. The weights are averages for the computerized adaptive test (CAT), not fixed counts.

| Domain | Name | Average weight | Sections |
| --- | --- | --- | --- |
| 1 | Security and Risk Management | 16% | 1.1 to 1.12 (12) |
| 2 | Asset Security | 10% | 2.1 to 2.6 (6) |
| 3 | Security Architecture and Engineering | 13% | 3.1 to 3.10 (10) |
| 4 | Communication and Network Security | 13% | 4.1 to 4.3 (3) |
| 5 | Identity and Access Management (IAM) | 13% | 5.1 to 5.6 (6) |
| 6 | Security Assessment and Testing | 12% | 6.1 to 6.5 (5) |
| 7 | Security Operations | 13% | 7.1 to 7.15 (15) |
| 8 | Software Development Security | 10% | 8.1 to 8.5 (5) |

The weights add up to 100%. The outline has 62 sections in total (I counted them from the text of the outline, see the worked example).

Two observations help when reading the table. First, the weight does not follow the section count: Domain 4 has only three sections but carries 13%, because each of its sections is long and broad (section 4.1 alone lists 18 topics). Second, Domain 7 has 15 sections but the same 13% as Domain 4, so one section in Domain 7 is on average much narrower than one in Domain 4.

### Domain 1: Security and Risk Management (16%)

The largest domain is the one that frames all the others. Its 12 sections are:

1. 1.1 Professional ethics, including the ISC2 Code of Professional Ethics and the organization's own code.
2. 1.2 Security concepts. The 2024 outline names five pillars: confidentiality, integrity, availability, authenticity and nonrepudiation.
3. 1.3 Security governance: alignment to business strategy, organizational roles, control frameworks (ISO, NIST, COBIT, SABSA, PCI, FedRAMP), due care and due diligence.
4. 1.4 Legal, regulatory and compliance issues: cybercrime, intellectual property, import and export controls, transborder data flow, privacy law.
5. 1.5 Investigation types: administrative, criminal, civil, regulatory and industry standards.
6. 1.6 Policy, standards, procedures and guidelines.
7. 1.7 Business continuity requirements, including the business impact analysis (BIA) and external dependencies.
8. 1.8 Personnel security.
9. 1.9 Risk management concepts: identification, analysis, treatment, control types, assessments, monitoring and reporting.
10. 1.10 Threat modeling.
11. 1.11 Supply chain risk management.
12. 1.12 Security awareness, education and training.

The 2024 outline lists authenticity and nonrepudiation next to the classic triad. That is a change from the three-property model that older study guides teach. The [CIA triad note](../../foundations/cia-triad/README.md) covers how those two extra properties relate to the triad.

Where it lives here: [foundations](../../foundations/README.md), [governance and compliance](../../governance-and-compliance/README.md), [risk management](../../governance-and-compliance/risk-management/README.md), [threat modeling](../../threat-modeling/README.md), [security awareness](../../security-awareness/README.md), [privacy regulations](../../privacy-regulations/README.md).

### Domain 2: Asset Security (10%)

Domain 2 asks what you protect and how its handling changes over time. Sections: classification (2.1), handling requirements (2.2), secure provisioning, ownership and inventory (2.3), the data lifecycle with roles, retention, remanence and destruction (2.4), asset retention including end of life and end of support (2.5), and data security controls such as scoping, tailoring, standards selection, DRM, DLP and CASB (2.6).

The data roles in 2.4 (owner, controller, custodian, processor, user or subject) are a frequent source of confusion, because *controller* and *processor* come from privacy law (see [GDPR](../../privacy-regulations/gdpr.md)) while *owner* and *custodian* come from information classification practice. A person can be a custodian in one sentence and a processor in the next.

Where it lives here: [Asset security](../../../asset-security/README.md), which today holds the [NIST Privacy Framework](../../../asset-security/privacy-and-data-protection/nist-privacy-framework.md). Classification and lifecycle notes are planned.

### Domain 3: Security Architecture and Engineering (13%)

Domain 3 is about building systems that are secure by design. Its ten sections cover secure design principles (3.1: threat modeling, least privilege, defense in depth, secure defaults, fail securely, segregation of duties, keep it simple, zero trust, privacy by design, shared responsibility, SASE), security models such as Bell-LaPadula and Biba (3.2), control selection (3.3), hardware and system capabilities like memory protection and the TPM (3.4), vulnerabilities of architectures from client systems to serverless and high-performance computing (3.5), cryptographic solutions (3.6), cryptanalytic attacks (3.7), site and facility design (3.8 and 3.9) and the system lifecycle (3.10).

The domain mixes abstract models with physical security. Evidence storage, fire suppression and HVAC appear here, not in operations.

Where it lives here: [defense in depth](../../../security-architecture-and-engineering/design-principles/defense-in-depth.md), [cryptography](../../../security-architecture-and-engineering/cryptography/README.md), [PKI](../../../security-architecture-and-engineering/cryptography/public-key-infrastructure.md), [cloud and infrastructure](../../../security-architecture-and-engineering/cloud-and-infrastructure-security/README.md) (including [CSPM](../../../security-architecture-and-engineering/cloud-and-infrastructure-security/cloud-security-posture-management.md) and [KSPM](../../../security-architecture-and-engineering/cloud-and-infrastructure-security/kubernetes-security-posture-management/README.md)), [operating system security](../../../security-architecture-and-engineering/operating-system-security/README.md) and [secure AI architecture](../../../security-architecture-and-engineering/ai-security/README.md).

### Domain 4: Communication and Network Security (13%)

Only three sections, but very wide. 4.1 is secure design of network architectures: the OSI and TCP/IP models, IPv4 and IPv6, secure protocols (IPsec, SSH, TLS), converged protocols, transport architecture and planes, traffic flows (north-south and east-west), physical and logical segmentation, micro-segmentation, edge, wireless, cellular, CDN, software-defined networking, virtual private cloud and monitoring. 4.2 is network components (infrastructure operation, transmission media, network access control, endpoint security). 4.3 is secure communication channels (voice and collaboration, remote access, data communications, third-party connectivity).

Where it lives here: [Communication and network security](../../../communication-and-network-security/README.md), with the [network security](../../../communication-and-network-security/network-security/README.md) section covering protocols, [segmentation](../../../communication-and-network-security/network-security/architecture/network-segmentation.md), [secure transport](../../../communication-and-network-security/network-security/secure-transport/README.md), [wireless](../../../communication-and-network-security/network-security/wireless/README.md), [network access control](../../../communication-and-network-security/network-security/link-layer/network-access-control-8021x.md) and the [NIST zero trust architecture](../../../communication-and-network-security/network-security/architecture/nist-zero-trust-architecture.md). Voice and collaboration channels and third-party connectivity are not written yet.

### Domain 5: Identity and Access Management (13%)

Six sections: control of physical and logical access (5.1), identification and authentication strategy for people, devices and services (5.2), federation (5.3), authorization mechanisms RBAC, ABAC, rule-based, risk-based, MAC, DAC and policy decision and enforcement points (5.4), the provisioning lifecycle (5.5) and authentication systems (5.6).

Note that 5.1 includes physical access to facilities. IAM in the CISSP sense is not only a directory and a login page.

Where it lives here: [Identity and access management](../../../identity-and-access-management/README.md), including [authentication vs authorization](../../../identity-and-access-management/identity-and-access/authentication-vs-authorization.md), [OAuth](../../../identity-and-access-management/identity-and-access/protocols/oauth.md), [OpenID Connect](../../../identity-and-access-management/identity-and-access/protocols/openid-connect.md) and [credential attacks](../../../identity-and-access-management/credential-attacks/README.md).

### Domain 6: Security Assessment and Testing (12%)

Five sections: designing assessment, test and audit strategies, internal, external and third party (6.1), security control testing (6.2: vulnerability assessment, penetration testing, log reviews, synthetic transactions, code review, misuse case testing, coverage analysis, interface testing, breach and attack simulation, compliance checks), collecting security process data such as KPIs, KRIs and backup verification (6.3), analyzing results and reporting including remediation, exception handling and ethical disclosure (6.4) and conducting audits (6.5).

SAST, DAST and SCA are listed in Domain 8 (section 8.2) in the outline, which is why their notes live in Domain 8 in this repository and are linked from here.

Where it lives here: [Security assessment and testing](../../../security-assessment-and-testing/README.md) and [red, blue and purple teams](../../../security-assessment-and-testing/red-blue-purple-teams.md).

### Domain 7: Security Operations (13%)

The most granular domain, with 15 sections: investigations including evidence collection and handling, forensics and reporting (7.1), logging and monitoring (7.2), configuration management (7.3), foundational concepts such as need to know, segregation of duties and privileged account management (7.4), resource protection and media management (7.5), incident management (7.6), detective and preventive measures such as firewalls, IDS and IPS, sandboxing and honeypots (7.7), patch and vulnerability management (7.8), change management (7.9), recovery strategies (7.10), disaster recovery processes and tests (7.11 and 7.12), business continuity planning and exercises (7.13), physical security (7.14) and personnel safety (7.15).

Where it lives here: [Security operations](../../../security-operations/README.md): [chain of custody](../../../security-operations/digital-forensics/chain-of-custody/README.md) for 7.1, [SIEM](../../../security-operations/defensive-operations/operations/siem.md) and [IDS](../../../security-operations/defensive-operations/detection/ids.md) for 7.2 and 7.7, the [NIST incident response lifecycle](../../../security-operations/defensive-operations/operations/nist-incident-response/README.md) for 7.6 and [vulnerability management](../../../security-operations/vulnerability-management/README.md) for 7.8.

### Domain 8: Software Development Security (10%)

Five sections: security in the software development lifecycle and methodologies such as Agile, DevOps and DevSecOps, plus maturity models such as CMM and SAMM (8.1), security controls in the development ecosystem including CI/CD, repositories and application security testing (SAST, DAST, SCA, IAST) (8.2), assessing the effectiveness of software security (8.3), the security impact of acquired software (COTS, open source, third party, managed and cloud services) (8.4) and secure coding guidelines (8.5).

Where it lives here: [Software development security](../../../software-development-security/README.md): [OWASP Top 10](../../../software-development-security/application-security/owasp/owasp-top-10.md), [SAST](../../../software-development-security/application-security/testing/static-application-security-testing.md), [SCA](../../../software-development-security/application-security/testing/software-composition-analysis.md), [SLSA](../../../software-development-security/application-security/supply-chain/slsa.md).

### Cross-domain topics and where they are filed

The outline repeats some topics in several domains. This repository keeps one home note per topic (see the [GUIDELINE](../../../GUIDELINE.md#311-cissp-domain-placement)).

| Topic | Appears in sections | Home in this repository | Reason |
| --- | --- | --- | --- |
| Threat modeling | 1.10, 3.1 | Domain 1 | The note teaches the methods, not a design review. |
| Zero trust | 3.1, 4.1 | Domain 4 | The central mechanism is access to networked resources. |
| Segregation of duties | 3.1, 7.4 | planned | Not yet written. |
| Supply chain | 1.11, 8.4 | Domain 8 for software, Domain 1 for the risk program | Software artifacts versus supplier risk. |
| Evidence handling | 3.9, 7.1 | Domain 7 | Evidence storage facilities (3.9) are physical, collection and handling (7.1) is procedural. |
| Business continuity | 1.7, 7.13 | planned | The requirements are Domain 1, the exercises Domain 7. |
| Cloud security | 3.5, 4.1, 8.4 | Domain 3 | Cloud posture is a design and configuration problem. |

## Worked example

This example derives two numbers from the outline itself: the section count per domain and the expected number of items per domain on a CAT exam. The outline text was converted with `pdftotext -layout` (poppler 22.02) and analyzed with Python 3.10. It reproduces the table above.

```python
import re
from collections import Counter

text = open("cissp.txt", encoding="utf-8").read()

# Section headings look like "    7.1 Understand and comply with investigations".
# Domain headers ("Domain 7:") do not match because they have no dot.
sections = Counter(
    m.group(1) for m in re.finditer(r"^\s+([1-8])\.\d+ [A-Z]", text, re.M)
)
weights = {1: 16, 2: 10, 3: 13, 4: 13, 5: 13, 6: 12, 7: 13, 8: 10}

print("sections per domain:", sorted(sections.items()), "total", sum(sections.values()))
print("weights add up to", sum(weights.values()))
for items in (100, 150):  # the CAT minimum and maximum number of items
    print(items, "items ->", [round(items * w / 100, 1) for w in weights.values()])
```

Output:

```text
sections per domain: [('1', 12), ('2', 6), ('3', 10), ('4', 3), ('5', 6), ('6', 5), ('7', 15), ('8', 5)] total 62
weights add up to 100
100 items -> [16.0, 10.0, 13.0, 13.0, 13.0, 12.0, 13.0, 10.0]
150 items -> [24.0, 15.0, 19.5, 19.5, 19.5, 18.0, 19.5, 15.0]
```

What to read from it. A candidate who is asked 100 items (the minimum) can expect about 16 on Domain 1 and about 10 on Domain 2. A candidate asked 150 items can expect about 24 on Domain 1. The numbers are expectations, not guarantees: a CAT selects the next item from an adaptive pool, and ISC2 calls the weights averages.

Reading the output critically: Domain 4 has 3 sections and about 13 items, which is about 4.3 items per section. Domain 7 has 15 sections and about 13 items, which is under 1 item per section. This is why short-looking domains are not easier. They are denser.

## Trade offs and when to use it

**What the domain model gives you.** A shared vocabulary with employers, auditors and other practitioners, and a checklist of topics that an experienced reviewer considers part of the profession. The 62 sections work well as a gap analysis: mark each section as strong, partial or missing.

**What it does not give you.**

- It does not tell you how deep to go. "Understand" in section 4.1 is applied to 18 topics, and a practitioner may need packet-level skill in two of them.
- It is a management level view. It is not a technical curriculum, and it does not replace hands-on training such as the one offered by SANS or by vendor labs.
- It changes. ISC2 states that the exam is based on a new outline effective April 15, 2027. I have not read the 2027 outline. Public summaries I found were individual posts, not an ISC2 document, so I do not record their claims. Review this note and the repository mapping when the new outline is available.

**Alternatives.** The NIST NICE Workforce Framework describes work roles and tasks, which fits job design better. The SANS curriculum and the CompTIA Security+ objectives are lower in level and narrower. The [ISO/IEC 27001](../../governance-and-compliance/standards/iso-iec-27001.md) Annex A controls are a control catalog, not a skills outline.

## Common mistakes

- **Treating weights as study time.** A domain with 10% of items can still decide a pass when it is the weakest. Study to the 62 sections, then weight the time.
- **Filing a topic by its tool name.** A SIEM is a Domain 7 topic because the exam asks about monitoring (7.2), but the design of its log pipeline touches Domain 3. File by the central question.
- **Assuming a domain equals a team.** Section 5.1 includes facility access, which is often a physical security team. Section 7.14 puts physical security in operations while 3.8 and 3.9 put its design in architecture.
- **Using the old three-property model for Domain 1.** The 2024 outline lists five pillars in 1.2. Answers that stop at confidentiality, integrity and availability may miss authenticity and nonrepudiation.
- **Quoting weights from memory.** The weights were different in earlier outlines. Always cite the outline edition. For example, ISC2 announced a change to the exam weighting in 2023 ([ISC2 Insights, November 2023](https://www.isc2.org/insights/2023/11/Changes-to-CISSP-Exam-Weighting)); I did not read that article, so I do not state its numbers.

## Practice

1. Which domain contains evidence storage facilities, and which contains evidence collection and handling? Why are they different?
2. Domain 4 has 3 sections and Domain 7 has 15. Both weigh 13%. What does that tell you about studying them?
3. A cloud misconfiguration scanner finds a public storage bucket. Name the domains that the finding touches, and say which one you would file a note about the scanner under.
4. Using the list of data roles in section 2.4, explain how GDPR vocabulary and classification vocabulary overlap, and where they differ.
5. Extend the worked example script to also print the number of bullet topics per domain (lines that start with the `»` character). What does the result say about which domains are lists of topics and which are lists of skills?

**Answers and hints**

1. Evidence storage facilities are in 3.9 (site and facility security controls). Collection and handling are in 7.1 (investigations). The first is about building a secure place, the second is about procedure and proof.
2. Each section in Domain 4 carries far more topics (4.1 alone has 18). The 3 sections in Domain 4 are wide survey areas, the 15 in Domain 7 are narrower.
3. Domain 3 (cloud architecture, 3.5), Domain 5 (access policy on the bucket), Domain 7 (detection and response) and Domain 2 (the data classification of what is in it). The scanner note belongs to Domain 3, because the central question is configuration of a cloud system.
4. Controller and processor are legal roles with duties set by law. Owner and custodian are internal governance roles. One organization can hold several roles for the same data set.
5. Hint: use `text.count("»")` per domain slice. The result is only an approximation because wrapped lines and multi-column layouts affect it.

## Further reading

- ISC2, *CISSP Certification Exam Outline*, effective April 15, 2024: the primary source for everything in this note ([PDF](https://edge.sitecorecloud.io/internationf173-xmc4e73-prodbc0f-9660/media/Project/ISC2/Main/Media/documents/exam-outlines/CISSP-Exam-Outline-April-2024-English.pdf)).
- ISC2, [CISSP certification page](https://www.isc2.org/certifications/cissp): current statements about the exam and the announcement of the April 15, 2027 outline.
- ISC2, [Code of Ethics](https://www.isc2.org/ethics): the text behind section 1.1.
- [CISSP certification](cissp.md): exam format, experience requirements and the credential.
- [ISC2](isc2.md): the organization behind the exam.
