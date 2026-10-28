# SANS

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

The **SANS Institute** is one of the **most influential and authoritative institutions in global cybersecurity**, specializing in:

- Cybersecurity **education and training**
- **Research and best practices**
- Development of **operational security frameworks**
- Industry-recognized **certifications (GIAC)**

Unlike NIST, ISO, or CIS, **SANS is not a regulatory or compliance body**.

Its strength lies in **deep, hands-on, practitioner-driven security knowledge** derived from real-world incidents, red-team operations, forensics, and defensive engineering.

> Key distinction:
>
> NIST defines
>
> *what*
>
> should be achieved
>
> SANS teaches
>
> *how*
>
> to actually do it in practice

## Philosophy and approach

SANS operates on several foundational principles:

### Practitioner-First

Content is developed by:

- Incident responders
- Penetration testers
- Malware analysts
- SOC engineers
- Digital forensics experts

#### Offensive + Defensive Balance

SANS treats **attack and defense as inseparable**:

- You cannot defend what you do not understand
- You cannot attack responsibly without understanding impact

#### Skills over compliance

SANS focuses on:

- Detection engineering
- Incident response
- Threat hunting
- Secure system operation

Not audits. Not paperwork.

## Contributions to cybersecurity

SANS influences the industry through **four primary pillars**:

1. **Training & Education**
2. **GIAC Certifications**
3. **Research & Security Models**
4. **Community & Knowledge Sharing**

## Training ecosystem

### Course Domains

SANS courses are grouped into **specialized security domains**:

| Domain | Focus |
| --- | --- |
| Blue Team | Detection, SOC, IR, Threat Hunting |
| Red Team | Offensive security, exploitation |
| DFIR | Digital forensics & incident response |
| Cloud Security | AWS, Azure, GCP defense & attack |
| Application Security | Secure coding, exploitation |
| ICS/OT | Industrial control system security |
| Management & GRC | Leadership, risk, governance |

Each course is mapped to **real attack scenarios** and includes:

- Labs
- Tools
- Case studies
- Adversary techniques

## GIAC Certifications

Global Information Assurance Certification

### What Is GIAC?

**GIAC** is the certification arm of SANS and is widely regarded as:

- **Technically rigorous**
- **Role-oriented**
- **Hands-on focused**

GIAC certifications validate **capability**, not memorization.

#### Major GIAC Certification Tracks

##### Blue Team / Defense

- GSEC - Security Essentials
- GCED - Enterprise Defense
- GCIA - Intrusion Analysis
- GCIH - Incident Handling
- GCED / GCTI - Threat Intelligence

##### Red Team / Offensive

- GPEN - Penetration Testing
- GXPN - Advanced Exploitation
- GWAPT - Web App Pentesting

##### DFIR

- GCFE - Forensic Examiner
- GCFA - Advanced Forensics
- GREM - Reverse Engineering Malware

##### Cloud Security

- GPCS - Cloud Security Essentials
- GCSA - Cloud Security Automation

#### GIAC vs Other Certifications

| Certification | Focus |
| --- | --- |
| CEH | Introductory, theoretical |
| CISSP | Governance & management |
| OSCP | Offensive, exploit-centric |
| **GIAC** | **Operational depth & realism** |

## Security models & frameworks

### SANS Top 25 Software Errors

The **SANS Top 25** identifies the **most dangerous programming errors**, based on:

- Exploitability
- Prevalence
- Impact

Categories include:

- Input validation flaws
- Memory corruption
- Authentication weaknesses
- Logic errors

**Security relevance:**

SANS Top 25 heavily influenced **OWASP Top 10** evolution.

#### SANS Critical Security Controls (Legacy)

SANS originally created what later became the **CIS Critical Security Controls**:

- Prioritized defensive controls
- Mapped to real attack techniques
- Operationally focused

This work shaped modern **control-based security models**.

## SANS and MITRE ATT&CK

SANS training is **deeply aligned with the MITRE ATT&CK framework**, especially in:

- Threat hunting
- Detection engineering
- SOC maturity
- Purple team operations

Typical SANS outcomes:

- Mapping detections to ATT&CK techniques
- Creating telemetry-driven detections
- Building adversary-based IR playbooks

## SANS and DevSecOps

SANS strongly supports **security integration into CI/CD and cloud-native environments**.

Practical areas:

- Secure pipeline design
- Secrets exposure detection
- Runtime threat detection
- Container & Kubernetes defense
- Cloud incident response

**Key mindset:**

Security must be **automated, observable, and testable**.

## SANS in SOC and Incident Response

SANS defines **best-in-class SOC and IR practices**:

### Detection Engineering

- Signal over noise
- Behavior-based detections
- Context-aware alerts

#### Incident Response Lifecycle

- Preparation
- Identification
- Containment
- Eradication
- Recovery
- Lessons learned

SANS IR guidance is considered **industry gold standard**.

## Research & community

### Internet Storm Center (ISC)

The **SANS Internet Storm Center**:

- Tracks emerging threats
- Shares real-time attack data
- Publishes daily handler diaries

#### Whitepapers & Consensus Docs

SANS publishes:

- Blue team playbooks
- Detection maturity models
- Forensics methodologies

## SANS vs NIST vs ISO

| Organization | Primary Role |
| --- | --- |
| NIST | Risk & governance framework |
| ISO | Formal compliance standard |
| **SANS** | **Hands-on operational mastery** |

They are **complementary**, not competing.

## Career Impact of SANS Mastery

A professional trained in SANS methodology demonstrates:

- Real attack understanding
- Practical defense capability
- Incident leadership skills
- Tool mastery
- High operational credibility

SANS is particularly valued in:

- SOCs
- CERT/CSIRT teams
- Cloud security teams
- DFIR units
- Military & intelligence contexts

## Learning path

Recommended progression:

1. Core security fundamentals (GSEC)
2. Choose specialization (Blue, Red, DFIR, Cloud)
3. Align with MITRE ATT&CK
4. Practice detection & response
5. Integrate with frameworks (NIST CSF, Zero Trust)

## Strategic perspective

SANS does not define **security posture**.

It defines **security competence**.

For a cybersecurity specialist:

- NIST tells you *where you should be*
- ISO tells you *what auditors want*
- **SANS teaches you how to survive real attacks**

## Summary

The SANS Institute represents the **operational backbone of modern cybersecurity**.

It is:

- Practical, not abstract
- Technical, not political
- Reality-driven, not checklist-based

For anyone aspiring to **true security expertise**, SANS knowledge is not optional - it is foundational.

## Worked example

TODO: add a concrete, reproducible example that walks through the idea end to end.

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Common mistakes

TODO: list frequent misunderstandings and failure modes, each with its fix.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
