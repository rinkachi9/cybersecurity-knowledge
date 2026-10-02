# NIST Privacy Framework

## Summary

The NIST Privacy Framework is a voluntary tool for managing privacy risk, which NIST defines around problems that individuals can experience as a result of how an organization processes data about them. It reuses the shape of the NIST Cybersecurity Framework (a Core of Functions, Categories and Subcategories, plus Profiles and Tiers) and adds five privacy Functions: Identify-P, Govern-P, Control-P, Communicate-P and Protect-P. It sits next to privacy law without replacing it: it helps an organization decide what outcomes to pursue and show how it manages privacy risk, while laws such as the GDPR define what is required.

Checked against NIST Privacy Framework Version 1.0 (2020-01-16). Version 1.1 is a draft or a recent release depending on the source, see the status section, and its contents are not covered here.

## Prerequisites

- [NIST CSF 2.0](../governance-and-compliance/frameworks/nist-cybersecurity-framework.md): the Core, Profiles and Tiers structure is shared.
- [Privacy regulations overview](regulations/privacy-regulations-overview.md) and [GDPR](regulations/gdpr.md): the legal obligations the framework helps to meet.
- [CIA triad](../foundations/cia-triad/README.md): the overlap between privacy and security.

## Core concepts

### Definition

The Privacy Framework (PF) 1.0 is titled *A Tool for Improving Privacy through Enterprise Risk Management*. It consists of three parts:

- **Core:** a set of privacy protection activities and outcomes, in Functions, Categories and Subcategories, that supports communication from the executive level to the operational level.
- **Profiles:** a selection of Functions, Categories and Subcategories that the organization has prioritized. A Current Profile shows what is achieved now, and a Target Profile shows the outcomes needed for the desired privacy risk management goals.
- **Implementation Tiers:** a point of reference on how an organization views privacy risk and whether it has the processes and resources to manage it. The four Tiers are Partial, Risk Informed, Repeatable and Adaptive.

NIST illustrates the three parts as connected gears in Fig. 1 of the framework: the Core as an increasingly granular set of activities and outcomes, Profiles as a selection of Functions, Categories and Subcategories (current and target), and Tiers as support for communication about whether the organization has enough processes and resources to reach its Target Profile.

### Privacy risk in NIST's terms

The PF explains the vocabulary:

- **Data processing** is the collective set of data actions, and a **data action** is a system, product or service operation on data across its life cycle: collection, retention, logging, generation, transformation, use, disclosure, sharing, transmission and disposal.
- A **problematic data action** is a data action that could cause a problem for individuals. The **likelihood** that a problematic data action occurs and the **impact** if it does are the basis for privacy risk.
- **Problems for individuals** range from dignity-type effects such as embarrassment or stigma to more tangible harms such as discrimination, economic loss or physical harm. NIST provides an illustrative catalog of problems in its Privacy Risk Assessment Methodology (PRAM).
- Problems can come from **data processing that works as designed**: the PF's example is smart meters that collect granular household electricity use, which can reveal behavior in the home even when the system operates as intended. They can also arise from interactions with systems when data is not directly linked to identifiable individuals.

![Relationship between privacy risk and organizational risk: a problem arises from data processing, the individual experiences a direct impact such as embarrassment, discrimination or economic loss, and the organization experiences a resulting impact such as customer abandonment, noncompliance costs or harm to reputation or internal culture. Source: NIST Privacy Framework 1.0, Fig. 3.](../_assets/privacy-and-data-protection/nist-privacy-framework-privacy-to-organizational-risk.png)

The figure shows how the PF connects the two views: a problem arises from data processing, the individual experiences a direct impact, and only then does the organization experience impacts such as customer abandonment, noncompliance costs and harm to reputation or internal culture. Organizations commonly manage these organizational impacts at the enterprise risk management level, so privacy risk can be compared with other risks.

This is the main difference from security risk. Security risk asks what happens to the organization's assets. Privacy risk starts from what happens to people, and then connects to organizational impact.

### Analogy

Think of a hospital's duty of care. Security is the locked records room and the audit of who opened the door. Privacy is the broader question of whether the hospital should collect that information at all, who should see it, how long it is kept, and whether the patient knows. A hospital can have perfect door locks and still harm patients by using data in ways they did not expect.

The analogy breaks in one place. A hospital knows its patients. In a data processing ecosystem, data moves through processors, advertising systems and partners, and the individuals may never interact with the organization that processes their data.

### Privacy and cybersecurity risk

![Venn diagram: cybersecurity risks arise from loss of confidentiality, integrity or availability, privacy risks arise from data processing, and the overlap is cybersecurity-related privacy events. Source: NIST CSWP 29, Fig. 6, which reproduces the same relationship as the Privacy Framework.](../_assets/governance-and-compliance/nist-csf-2-cybersecurity-privacy-risk.png)

The two disciplines overlap in cybersecurity-related privacy events, for example a breach that exposes personal data. NIST states that managing cybersecurity risk contributes to managing privacy risk but is not sufficient, since privacy risks also arise by means unrelated to cybersecurity incidents. The two frameworks are designed to be used together.

### The five Functions and 18 Categories

The "-P" suffix marks a Privacy Framework Function to avoid confusion with CSF Functions. Version 1.0 has 5 Functions, 18 Categories and about 100 Subcategories (the subcategory number is a count of distinct identifiers in the document).

| Function | NIST definition (paraphrased) | Categories |
| --- | --- | --- |
| Identify-P (ID-P) | Develop the organizational understanding to manage privacy risk for individuals arising from data processing | ID.IM-P Inventory and Mapping, ID.BE-P Business Environment, ID.RA-P Risk Assessment, ID.DE-P Data Processing Ecosystem Risk Management |
| Govern-P (GV-P) | Develop and implement the governance structure for an ongoing understanding of risk management priorities informed by privacy risk | GV.PO-P Governance Policies, Processes, and Procedures, GV.RM-P Risk Management Strategy, GV.AT-P Awareness and Training, GV.MT-P Monitoring and Review |
| Control-P (CT-P) | Develop and implement activities that let organizations or individuals manage data with sufficient granularity to manage privacy risks | CT.PO-P Data Processing Policies, Processes, and Procedures, CT.DM-P Data Processing Management, CT.DP-P Disassociated Processing |
| Communicate-P (CM-P) | Develop and implement activities that let organizations and individuals have a reliable understanding of, and a dialogue about, how data are processed and the associated privacy risks | CM.PO-P Communication Policies, Processes, and Procedures, CM.AW-P Data Processing Awareness |
| Protect-P (PR-P) | Develop and implement appropriate data processing safeguards, covering data protection to prevent cybersecurity-related privacy events | PR.PO-P Data Protection Policies, Processes, and Procedures, PR.AC-P Identity Management, Authentication, and Access Control, PR.DS-P Data Security, PR.MA-P Maintenance, PR.PT-P Protective Technology |

The Core also lists the CSF Functions Detect, Respond and Recover, so that organizations can use the CSF's Detect, Respond and Recover for cybersecurity-related privacy events together with the five privacy Functions. NIST also says that organizations may use all five CSF Functions in conjunction with Identify-P, Govern-P, Control-P and Communicate-P.

Examples of Subcategories, with the NIST wording shortened:

| ID | Outcome |
| --- | --- |
| ID.IM-P1 | Systems, products and services that process data are inventoried |
| ID.IM-P8 | Data processing is mapped, illustrating the data actions and associated data elements |
| ID.RA-P4 | Problematic data actions, likelihoods and impacts are used to determine and prioritize risk |
| CT.DP-P4 | System or device configurations permit selective collection or disclosure of data elements |
| CT.DP-P5 | Attribute references are substituted for attribute values |
| CM.AW-P4 | Records of data disclosures and sharing are maintained |
| CM.AW-P7 | Impacted individuals and organizations are notified about a privacy breach or event |
| PR.DS-P6 | Integrity checking mechanisms are used to verify software, firmware and information integrity |

Control-P is the part with no equivalent in the CSF. It covers data management with granularity (for example selective disclosure, individual preferences, disassociated processing such as de-identification) and is where privacy engineering lives. Communicate-P covers transparency and the dialogue with individuals.

### Profiles and Tiers

Profiles and Tiers work as in the CSF: build a Current Profile, define a Target Profile, analyze the gap, and prioritize actions. The framework says Tiers reflect a progression from informal, reactive responses to approaches that are agile and risk informed, and that progression is encouraged but is not a compulsory goal. Tier selection should consider the Target Profile, risk management practices, how privacy risk is integrated in enterprise risk management, the data processing ecosystem relationships and the workforce.

The PF stresses **ecosystem roles**. Core elements are not assigned by ecosystem role, so an organization reviews the Core from its own position (for example controller or processor in legal terms, or provider or user of data processing) to decide what applies. This is a practical help for the "who is responsible for what" problem in data sharing.

### Version status

Privacy Framework 1.0 was released on 2020-01-16. NIST's Privacy Framework web page, fetched in 2026-10, advertised a Privacy Framework 1.1 initial public draft. Secondary sources report that the draft appeared in April 2025 with a realignment to CSF 2.0 (a Govern function that spans the others and a Protect function) and added material on AI and privacy risk, and some report a final 1.1 in September 2025. I could not confirm the final release from a NIST source, so check the current version before citing function names. The framework text above describes version 1.0.

### Relationship to laws and standards

| Item | Relationship |
| --- | --- |
| [GDPR](regulations/gdpr.md), [HIPAA](regulations/hipaa.md), [GLBA](regulations/glba.md) and other laws | The PF is not a legal compliance regime. Laws define obligations. The PF helps design, evidence and communicate the program that meets them |
| [NIST CSF](../governance-and-compliance/frameworks/nist-cybersecurity-framework.md) | Companion. Protect-P overlaps with CSF Protect, and the shared Core structure allows combined Profiles |
| [SP 800-53 Rev. 5](../governance-and-compliance/frameworks/nist-sp-800-53/README.md) | Rev. 5 integrated privacy controls with the security controls (PT family, a privacy baseline) |
| [NIST RMF](../governance-and-compliance/risk-management/risk-management-framework.md) | SP 800-37 Rev. 2 integrates privacy risk management, with a privacy plan and the senior agency official for privacy |
| NIST AI RMF | Lists privacy-enhanced as one of seven characteristics of trustworthy AI |

## Worked example

The scenario: Example Corp (`example.com`) runs a SaaS product and wants to analyze how visitors use its pricing and documentation pages. The goal is to reduce privacy risk while keeping the analytics useful. Data is synthetic.

**Identify-P.** Inventory the data actions (ID.IM-P1 and ID.IM-P8): the web app logs user ID, IP address, age, postcode and page. Name the individuals concerned (customers and prospects) and the recipients (the analytics vendor). Assess problematic data actions (ID.RA-P4): the analytics team joining behavior with age and postcode could allow someone to single out an individual, and a customer could feel profiled.

**Govern-P.** Record the policy decision: analytics uses the minimum data needed for product decisions, and an owner approves new fields.

**Control-P.** Apply two minimization steps in code: do not collect the IP address at all (CT.DP-P4, selective collection), and replace the user ID with a keyed token (CT.DP-P5, attribute references substituted for attribute values). Generalize age to a decade and postcode to a two-digit prefix. Then measure what is left. Tested with Python 3.10.12, standard library only:

```python
import hashlib
import hmac
from collections import Counter

KEY = b"demo-key-not-a-secret"   # in practice a managed secret, rotated, stored apart from the data

events = [
    {"user": "u1001", "ip": "192.0.2.10",   "age": 34, "postcode": "00-950", "page": "/pricing"},
    {"user": "u1002", "ip": "192.0.2.11",   "age": 36, "postcode": "00-951", "page": "/pricing"},
    {"user": "u1003", "ip": "198.51.100.7", "age": 52, "postcode": "31-100", "page": "/docs"},
    {"user": "u1004", "ip": "198.51.100.9", "age": 55, "postcode": "31-101", "page": "/docs"},
    {"user": "u1005", "ip": "203.0.113.5",  "age": 29, "postcode": "80-001", "page": "/pricing"},
]


def minimize(e):
    token = hmac.new(KEY, e["user"].encode(), hashlib.sha256).hexdigest()[:12]   # CT.DP-P5
    decade = f"{e['age'] // 10 * 10}s"                                             # generalize age
    return {"user": token, "age": decade, "postcode": e["postcode"][:2], "page": e["page"]}  # IP dropped (CT.DP-P4)


out = [minimize(e) for e in events]
for row in out:
    print(row)

groups = Counter((r["age"], r["postcode"]) for r in out)
print("smallest group size (k) over age band + postcode prefix:", min(groups.values()))
print("rows that are unique on those quasi-identifiers:", [k for k, v in groups.items() if v == 1])
```

Output:

```text
{'user': '6fba265be552', 'age': '30s', 'postcode': '00', 'page': '/pricing'}
{'user': 'b246ace5ab6d', 'age': '30s', 'postcode': '00', 'page': '/pricing'}
{'user': '7a1b2509cc60', 'age': '50s', 'postcode': '31', 'page': '/docs'}
{'user': '24eeb8cfbc56', 'age': '50s', 'postcode': '31', 'page': '/docs'}
{'user': '2a0515981d56', 'age': '20s', 'postcode': '80', 'page': '/pricing'}
smallest group size (k) over age band + postcode prefix: 1
rows that are unique on those quasi-identifiers: [('20s', '80')]
```

What to notice:

1. The IP address is gone and the user ID is a keyed token, so the analytics table cannot be joined to the customer table without the key. That is pseudonymization, which reduces risk, but whoever holds the key can reverse the mapping, so the data are still personal data under laws such as the GDPR.
2. The last two lines show the limit. Age band plus postcode prefix still leaves one row that is unique (`20s`, `80`), so a person who knows those two facts about this individual can find their pages. A smallest group size of 1 means the generalization is not enough, and k should be increased by coarsening further or suppressing rare rows.
3. The correct next step is risk-based: decide a target for k, apply it, and record the residual risk in the Profile. This is the ID.RA-P4 loop (likelihood and impact of a problematic data action), not a one-time anonymization claim.

**Communicate-P.** Update the privacy notice to describe the analytics, what is collected and how long it is kept (CM.PO-P and CM.AW-P outcomes), and keep records of disclosures to the analytics vendor (CM.AW-P4).

**Protect-P.** Restrict access to the token key and the raw logs, and monitor access (PR.AC-P and PR.DS-P outcomes). A breach of the raw logs is a cybersecurity-related privacy event, and the CSF Detect, Respond and Recover Functions apply, including notification (CM.AW-P7).

**Profile.** The result is a small Current and Target Profile for this system: which Subcategories are met now, which are the target, and the gap list (increase k, add the key rotation procedure, update the notice).

## Trade offs and when to use it

### Benefits

- Starts from individuals and their problems, which gives an argument that connects privacy to organizational risk and funding.
- Fits with security programs through the shared structure and the CSF.
- Technology- and law-neutral, so one Profile can serve several jurisdictions.
- Gives engineering teams a concrete vocabulary (Control-P and disassociated processing).

### Costs and limits

- **No legal compliance.** The PF does not tell you what the law requires. Use it with legal advice and regulations.
- **No certification.** There is no NIST certificate for the PF.
- **Interpretation needed.** Outcomes are generic, and small teams may need help turning them into actions. Experience in privacy engineering matters.
- **Version change.** A 1.1 update is in progress or recently released, and identifiers may change.
- **Privacy risk estimates are hard.** Likelihood of a "problem" for an individual is hard to quantify, and the PRAM catalog is a starting point.

### Alternatives and companions

| Need | Option |
| --- | --- |
| Legal obligations | [GDPR](regulations/gdpr.md), [HIPAA](regulations/hipaa.md), [GLBA](regulations/glba.md), [PIPEDA](regulations/pipeda.md), [COPPA](regulations/coppa.md) |
| Certifiable privacy management system | An ISO standard that extends an information security management system (for example ISO/IEC 27701, mentioned from memory and not reviewed here) |
| Security program | [NIST CSF](../governance-and-compliance/frameworks/nist-cybersecurity-framework.md) |
| System authorization with privacy controls | [RMF](../governance-and-compliance/risk-management/risk-management-framework.md) and [SP 800-53](../governance-and-compliance/frameworks/nist-sp-800-53/README.md) with the privacy baseline |

## Common mistakes

| Mistake | Why it is wrong | Fix |
| --- | --- | --- |
| Treating the PF as legal compliance | It is voluntary guidance, and laws impose the obligations | Map legal requirements into Govern-P and keep legal review |
| Equating privacy with security | Privacy problems occur even with perfect security (surveillance feeling, secondary use) | Assess problematic data actions, not only breaches |
| Calling pseudonymized data anonymous | A key holder can reverse tokens, and quasi-identifiers can re-identify (see the example) | Measure re-identification risk, document the residual risk |
| Skipping data inventory and mapping | Everything else depends on knowing the data actions | Start with ID.IM-P |
| Ignoring the ecosystem | Processors, vendors and partners are part of the risk | Use ID.DE-P and ecosystem roles |
| Collecting first and deciding later | Control-P and minimization are cheapest at design time | Decide fields and purposes before collection |
| Building a Profile once | Data processing changes with every feature | Revisit when data actions change |
| Citing function names from a different version | PF 1.1 realigns with CSF 2.0 | State the version used |

## Practice

1. List the five PF 1.0 Functions and say which one has no counterpart in the CSF.
2. Define a problematic data action. Give an example that happens even when the system works as designed.
3. Why is pseudonymization not anonymization? Use the example output.
4. Which PF Function covers each: a privacy notice, a data inventory, a retention policy owner, encryption of stored personal data?
5. How does the PF connect individual problems to organizational risk?
6. A vendor receives your customers' data. Which Categories help you manage that risk?

Hints and answers:

1. Identify-P, Govern-P, Control-P, Communicate-P, Protect-P. Control-P has the most distinct role, as the CSF has no function for managing data with granularity and individual control, while Protect-P overlaps the CSF Protect function.
2. A data action that could cause a problem for individuals. The smart meter example: granular household electricity use reveals behavior at home even though the system works as intended.
3. A keyed token can be reversed by whoever has the key, and a person can be re-identified by quasi-identifiers such as age band and postcode prefix. In the example one row is unique (k = 1).
4. Communicate-P (notice), Identify-P (inventory), Govern-P (policy ownership) or Control-P (data processing management, retention), Protect-P (encryption, data security).
5. A problem arises from data processing, the individual experiences a direct impact, and the organization then experiences impacts such as customer abandonment, noncompliance costs and reputation harm. Connecting them lets privacy compete for resources in enterprise risk management.
6. ID.DE-P (Data Processing Ecosystem Risk Management), ID.IM-P2 (owners and operators of systems and components inventoried), CM.AW-P4 (records of disclosures), and GV.PO-P for governance policies.

## Further reading

- NIST, Privacy Framework: A Tool for Improving Privacy through Enterprise Risk Management, Version 1.0 (2020-01-16). The primary source for this note: https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.01162020.pdf
- NIST Privacy Framework website, for the current version and the 1.0 to 1.1 mappings: https://www.nist.gov/privacy-framework
- NIST, Privacy Risk Assessment Methodology (PRAM) and the NIST privacy engineering publications cited by the framework (NIST IR 8062). Referenced in the PF and not read for this note.
- NIST, The NIST Cybersecurity Framework (CSF) 2.0 (2024), Section 5.2 on privacy risks: https://doi.org/10.6028/NIST.CSWP.29
