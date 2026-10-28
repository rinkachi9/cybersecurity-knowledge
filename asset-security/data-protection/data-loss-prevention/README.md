# Data loss prevention (DLP)

## Summary

Data loss prevention is a set of controls that detect sensitive data where it is stored, moves or is used, and then monitor, warn, block, encrypt or quarantine according to policy. It targets two failures: accidental disclosure (the wrong attachment, the public link, the paste into a chatbot) and deliberate exfiltration by an insider or an attacker. DLP works by classifying content with detectors and by judging context such as who, where to and through which channel. Its quality depends on the detectors (a card number regex without validation produces mostly false alarms), on the data classification that tells it what matters, and on a rollout that starts in monitor-only mode. It reduces risk but cannot stop a determined insider who can photograph a screen, so it belongs inside a program that also includes classification, access control and monitoring.

## Prerequisites

- [Asset management](../../asset-management/README.md) and information classification: DLP enforces rules about classes of data, so the classes must exist.
- [CIA triad](../../../security-and-risk-management/foundations/cia-triad/README.md), because DLP protects confidentiality.
- [Privacy regulations overview](../../../security-and-risk-management/privacy-regulations/privacy-regulations-overview.md) and [GDPR](../../../security-and-risk-management/privacy-regulations/gdpr.md), the legal drivers.
- [Hashing](../../../security-architecture-and-engineering/cryptography/hashing/hashing-algorithms.md) for fingerprinting and exact data matching.

## Core concepts

### Definition

*Data loss prevention* is the practice and the tooling that identify sensitive information and control its movement to prevent unauthorized disclosure. Microsoft describes it in its Purview documentation as a way to prevent users from inappropriately sharing sensitive data, such as financial data, proprietary data, credit card numbers, health records and Social Security numbers, with people who should not have it (Microsoft Learn, updated September 2026; vendor statement). The CISSP outline lists DLP together with DRM and CASB as data protection methods in section 2.6.

The same word covers three states of data, and a DLP program handles each differently:

| State | Where | Typical DLP method |
| --- | --- | --- |
| Data in use | On an endpoint: copy, paste, print, screenshot, upload from a browser | Endpoint agent, browser integration |
| Data in motion | Network: email, web, file transfer, messaging | Email gateway, proxy or secure web gateway, network sensor |
| Data at rest | File shares, cloud storage, databases, SaaS | Discovery scan, labeling, quarantine, see [DSPM](../data-security-posture-management/README.md) |

### Analogy

Airport baggage screening. Bags (data) are scanned for prohibited items (patterns of sensitive data), the context matters (a knife in a kitchen set versus in a pocket), the response varies (let it through, stop and ask, confiscate), and every screening point is a channel (gate, cargo, post). It breaks in two ways: airports screen everyone before a single exit, while data leaves through hundreds of channels, and a screener recognizes a knife, whereas a detector must infer sensitivity from patterns and labels.

### How detection works

Detectors fall into a few types. Combining them is what keeps false positives manageable.

| Detector | How it works | Strength | Weakness |
| --- | --- | --- | --- |
| Pattern (regular expression) | Matches formats such as card numbers | Cheap, fast | Many false positives |
| Pattern plus validation | Adds a checksum (Luhn for cards, mod-97 for IBAN) | Removes random digit strings | Only for formats with a checksum |
| Keyword and proximity | A primary match needs a supporting word nearby | Cuts noise | Language and wording dependent |
| Exact data match | Compares with hashed values from a real dataset (customer IDs) | High precision for specific records | Needs a secure, maintained reference set |
| Document fingerprinting | Matches whole or partial documents against a template | Good for forms and contracts | Fails if text changes a lot |
| Labels and metadata | Acts on a classification label applied by users or auto-labeling | Reliable if labeling is | Depends on labeling coverage |
| Machine learning classifiers | Classify content by learned features | Catch unstructured content | Opaque, needs tuning, can be evaded |

Microsoft's description of its deep content analysis lists keyword matches for the primary data, regular expressions, internal function validation, secondary matches in proximity to the primary match and machine learning algorithms, which fits this table (vendor documentation, checked 2026-10).

Context conditions complete the rule: who is the sender, who is the recipient (internal or external, managed or unmanaged), which device, which application, how many items. An example from the same documentation: 95 Social Security numbers emailed to a recipient outside the organization.

### Responses

Policies take actions on a match. Microsoft lists these for its product: warn with a policy tip, block with the option to override with a justification, block without override, move data at rest to a secure quarantine, and hide sensitive content in chat. All monitored activities are logged. Generic equivalents exist in other products: encrypt, redact, require approval, notify the data owner, create an incident.

Simulation or monitor mode, where actions are not applied, is part of the documented rollout: the recommended lifecycle is plan, prepare and deploy, with a policy tested in simulation first, tuned and then enabled. The same page notes that policies take effect about an hour after being turned on, and that Exchange DLP scans new messages and does not match existing items stored in a mailbox. Both are product-specific details.

### Where DLP sits in an architecture

```mermaid
flowchart LR
  A[Discover and classify data] --> B[Policy: what, who, where, action]
  B --> C[Endpoint agent]
  B --> D[Email and web gateway]
  B --> E[Cloud and SaaS API or CASB]
  C --> F[Alerts and incidents]
  D --> F
  E --> F
  F --> G[Triage, tune policy, educate users]
  G --> B
```

The diagram shows that DLP is a loop. Classification feeds policy, channels enforce it, alerts feed tuning. A CASB (cloud access security broker) extends the reach to SaaS. A secure web gateway or network DLP covers web traffic. Rights management (DRM) travels with the document and controls what a recipient can do.

Relation to SP 800-53 (control index kept in this repository): information flow enforcement (AC-4, moderate and high baselines), boundary protection (SC-7), system monitoring (SI-4), protection of information at rest (SC-28) and transmission confidentiality and integrity (SC-8). No single control is "DLP"; it is a family of mechanisms that implement parts of these.

### Limits of DLP

- **Encrypted channels.** Without TLS inspection, network DLP cannot see content. Inspection has its own privacy and risk costs.
- **Evasion.** Encoding, compression, splitting, screenshots and photos of a screen bypass pattern detectors.
- **Insiders with legitimate access.** DLP shows what moved, it does not decide intent.
- **Unmanaged devices and personal accounts.** Outside the agent and gateway coverage.
- **Generative AI tools.** Pasting data into an AI chatbot is a new egress path. Microsoft's page lists browser-based and network-based controls for several AI services (vendor claim). See [adversarial AI](../../../security-architecture-and-engineering/ai-security/adversarial-machine-learning/README.md) for the broader risks.
- **Scale and tuning.** A policy that fires thousands of times a day will be ignored.

## Worked example

The script `scripts/dlp-detectors.py` compares a naive card regex with a detector that adds validation and context, on a labeled synthetic corpus of eight messages. Test values are public: `4111 1111 1111 1111` is a standard test card number, `GB82 WEST 1234 5698 7654 32` is the documentation IBAN and `AKIAIOSFODNN7EXAMPLE` is the example key id from AWS documentation. Python 3.10, standard library only. The output is real.

```bash
python3 scripts/dlp-detectors.py
```

Output:

```text
naive, card only       tp=2 fp=4 fn=0 precision=0.33 recall=1.00
validated, card only   tp=2 fp=0 fn=0 precision=1.00 recall=1.00
validated, all types   tp=4 fp=0 fn=0 precision=1.00 recall=1.00
redaction: Please charge card [CARD ****1111] for the order
```

Reading it:

1. **The naive regex finds every real card and four false ones.** Its false positives are a 16-digit number that fails the Luhn check, a tracking number that fails it, a long ticket id of digits and the digits of the IBAN. Precision is 0.33, which means two of three alerts are noise.
2. **Validation and context remove all four.** The Luhn check rejects the random digit strings and the keyword rule (`card`, `visa`, `payment` and similar within 40 characters) rejects the ticket id. On this corpus both precision and recall are 1.00. This is a small, friendly corpus: real data has cards with no keywords nearby (a recall loss) and numbers that pass Luhn by chance about one time in ten.
3. **Redaction.** The last line shows a data minimization action: replace a validated card number with a masked form that keeps the last four digits.
4. **What the test does not cover.** Encoded or split data, images and documents inside archives. A production evaluation uses a larger corpus built from real (properly protected) examples and tracks precision and recall per detector over time.

## Trade offs and when to use it

**Where DLP pays off.** Regulated data (cards, health records, personal data), intellectual property with identifiable markers, and organizations where accidental disclosure by email or sharing is a main source of incidents. The first value usually comes from visibility: which data leaves, through which channel, by whom.

**Costs and limits.**

- Operational effort: policy design, tuning and incident handling take staff time, usually more than the license.
- Privacy and labor law: monitoring employee content needs a legal basis, notice and works council consultation in some countries. Involve legal and HR before deployment.
- User friction: blocking legitimate work creates workarounds, such as personal email or messaging apps, which are worse.
- Coverage gaps: unmanaged devices, new SaaS and AI tools appear faster than policies.
- Detection quality limits: see the table in this note.

**Order of rollout that works.** Classify and inventory the data, start with a few high-value data types, run in monitor mode, review alerts with the data owners, tune, warn users with policy tips, then block for the highest-risk channels. Add channels one at a time.

**Alternatives and complements.** Reduce what exists (retention and minimization), restrict access ([authorization](../../../identity-and-access-management/identity-and-access/authorization.md)), encrypt data with keys that follow access policy, use rights management for documents, and monitor with a [SIEM](../../../security-operations/defensive-operations/operations/siem.md) and user behavior analytics for anomalies. For data at rest in the cloud use [DSPM](../data-security-posture-management/README.md).

## Common mistakes

| Mistake | Effect | Fix |
| --- | --- | --- |
| Enabling block mode on day one | Business disruption, then policy disabled | Monitor first, tune, then enforce |
| Pattern-only detectors | Alert fatigue | Validation, context, exact data match |
| No data classification | Policies cover guesses | Classify first, label where possible |
| Ignoring endpoints and personal cloud apps | The easy channels stay open | Cover endpoint, web and sanctioned SaaS |
| No process for alerts | Alerts pile up | Assign owners, SLAs and a feedback loop |
| Treating DLP as insider-threat detection | Misses intent | Combine with behavior analytics and HR process |
| Skipping legal review | Privacy and employment violations | Involve legal, HR and privacy early |
| Never re-testing detectors | Drift in formats and tools | Scheduled tests against a labeled corpus |

Detection and mitigation: the DLP incidents themselves are a detection source. Forward them to the SIEM and correlate with identity and endpoint events (for example a mass download followed by an upload to a personal cloud). Mitigation is the layered approach in the previous section.

## Practice

1. List the three states of data and one DLP method for each.
2. Why does adding the Luhn check change precision so much in the worked example?
3. A policy blocks emails with five or more card numbers. How could an insider evade it, and which control would catch the evasion?
4. What are the first three steps of a sensible rollout?
5. Extend the script with a detector for an internal project code word using exact data match against a SHA-256 hash list. What are the benefits and risks of storing the hash list?
6. Which CISSP section covers DLP, and which SP 800-53 controls does it support?

**Answers and hints**

1. In use: endpoint agent. In motion: email or web gateway. At rest: discovery scan or DSPM.
2. Most digit strings are not valid card numbers: the checksum passes for about one in ten random numbers, so it removes most random matches.
3. Send four at a time, encode the numbers or take photos. Behavior analytics on volume over time, and egress monitoring, would catch it.
4. Classify and decide the data types to protect, deploy in monitor mode and review alerts with data owners.
5. Benefit: precise matching without keeping plain values in the tool. Risk: short or guessable values can be reversed by brute force, so use salted or keyed hashes and protect the list.
6. Section 2.6 (data protection methods), plus 7.2 (egress monitoring). SP 800-53: AC-4, SC-7, SI-4, SC-28.

## Further reading

- Microsoft Learn, [Learn about data loss prevention](https://learn.microsoft.com/en-us/purview/dlp-learn-about-dlp) (page updated September 2026): detection methods, actions, simulation mode, lifecycle. Vendor documentation, read in full.
- ISC2, *CISSP Certification Exam Outline*, effective April 15, 2024, sections 2.6 and 7.2.
- NIST SP 800-53 Rev. 5, controls AC-4, SC-7, SC-8, SC-28 and SI-4: see the [SP 800-53 note](../../../security-and-risk-management/governance-and-compliance/frameworks/nist-sp-800-53/README.md).
- [DSPM](../data-security-posture-management/README.md) and [asset management](../../asset-management/README.md) in this repository.
- NIST has no single DLP publication that I read for this note. The ISO/IEC 27001 and NIST privacy guidance on data minimization complement DLP, see the [NIST Privacy Framework](../../privacy-and-data-protection/nist-privacy-framework.md).
