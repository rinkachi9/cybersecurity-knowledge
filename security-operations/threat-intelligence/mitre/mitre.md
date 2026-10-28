# MITRE

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

MITRE is a **non-profit organization** that operates federally funded research and development centers (FFRDCs) and develops widely used **cybersecurity knowledge frameworks and tools**.

It is best known for creating:

- MITRE ATT&CK®
- MITRE CAPEC
- MITRE CWE
- MITRE D3FEND

**Core objective:**

To provide **standardized, publicly available knowledge bases** that help organizations understand, detect, and defend against cyber threats.

## Importance

Modern cybersecurity requires:

- Understanding attacker behavior
- Standardizing threat intelligence
- Mapping defenses to real-world attacks

MITRE provides:

- A **common language for security teams**
- Structured models of:
  - Attacks
  - Vulnerabilities
  - Defensive techniques

This makes it:

- Foundational for:
  - Threat modeling
  - Detection engineering
  - Incident response
  - Security analytics

## Core philosophy

MITRE is built around:

### Knowledge Sharing

All frameworks are:

- Public
- Community-driven
- Continuously updated

#### Adversary-Centric Security

Focus on:

> “How attackers actually operate in the real world”

#### Standardization

Provides:

- Common taxonomy
- Unified terminology

#### Practical Security

Designed for:

- Real-world implementation
- Integration with tools and processes

## Key MITRE Frameworks

### MITRE ATT&CK®

#### What it is?

MITRE ATT&CK (Adversarial Tactics, Techniques, and Common Knowledge) is a **knowledge base of attacker behaviors**.

#### Structure

Organized into:

- **Tactics** (high-level goals)
- **Techniques** (how attackers achieve goals)
- **Sub-techniques**

#### Example Tactics

- Initial Access
- Execution
- Persistence
- Privilege Escalation
- Defense Evasion
- Credential Access
- Discovery
- Lateral Movement
- Command and Control
- Exfiltration
- Impact

#### Example Technique

- Credential Dumping
- Phishing
- Exploiting Public-Facing Application

#### Use Cases

- Threat detection
- Security monitoring (SIEM)
- Red teaming
- Threat modeling (PASTA, Attack Trees)

### MITRE CAPEC (Common Attack Pattern Enumeration and Classification)

#### What it is?

CAPEC is a catalog of:

- **Common attack patterns**
- Descriptions of how attacks are executed

#### Focus

- “How attacks work”

#### Example

- SQL Injection
- Cross-Site Scripting
- Session Fixation

#### Use Cases

- Secure design
- Threat modeling
- Security training

### MITRE CWE (Common Weakness Enumeration)

#### What it is?

CWE is a catalog of:

- **Software weaknesses**
- Root causes of vulnerabilities

#### Example

- CWE-79 → Cross-Site Scripting
- CWE-89 → SQL Injection
- CWE-522 → Weak Password Storage

#### Use Cases

- Secure coding
- SAST tools
- Code reviews

### MITRE D3FEND

#### What it is?

D3FEND is a framework for:

- **Defensive techniques**
- Countermeasures against ATT&CK techniques

#### Focus

- “How to defend”

#### Example

- Network traffic filtering
- Credential protection
- Process isolation

#### Use Cases

- Security architecture
- Defense planning
- Blue team operations

## MITRE Model Structure

```java
Attack Techniques (ATT&CK)
        ↓
Attack Patterns (CAPEC)
        ↓
Root Causes (CWE)
        ↓
Defensive Measures (D3FEND)
```

## MITRE in Practice

### Example Flow

**Scenario:**

Attacker performs credential theft

**ATT&CK:**

- Credential Access → Credential Dumping

**CAPEC:**

- Credential harvesting attack pattern

**CWE:**

- Weak credential storage

**D3FEND:**

- Credential encryption
- Access control

## MITRE in DevSecOps

MITRE integrates into:

### Design Phase

- Threat modeling using ATT&CK
- Secure design using CAPEC

#### Development

- Secure coding using CWE
- SAST tools mapping findings to CWE

#### CI/CD

- Vulnerability scanning
- Policy enforcement

#### Runtime

- Detection rules mapped to ATT&CK
- SIEM correlation

#### Example

```diff
Attack: Phishing → Credential Theft → API Abuse
Mapped to:
- ATT&CK techniques
- Detection rules in SIEM
```

## MITRE in Cloud Environments

Use cases:

- Kubernetes attack modeling
- IAM threat detection
- API abuse detection

Example:

- ATT&CK → Privilege Escalation
- Cloud mapping → IAM misconfiguration

MITRE helps:

- Detect lateral movement
- Secure multi-tenant systems
- Implement Zero Trust

## Strengths

- Widely adopted industry standard
- Real-world attacker behavior modeling
- Strong integration with tools
- Continuously updated

## Weaknesses

- Requires expertise to use effectively
- Large and complex
- Not a complete framework (needs integration)

## Common pitfalls

- Treating ATT&CK as a checklist
- Ignoring context
- Not mapping to detection/response
- Overcomplicating implementation

## Skills Required

- Threat intelligence
- Security operations (SOC)
- Detection engineering
- Security architecture

## When to Use MITRE

Best suited for:

- Threat detection
- SOC operations
- Threat modeling
- Red/Blue teaming

## When NOT to Use Alone

Avoid using MITRE as:

- Full risk management framework
- Compliance framework

## Integration with Other Frameworks

MITRE works well with:

- **NIST CSF** → governance
- **ISO 27001** → compliance
- **PASTA / STRIDE** → threat modeling
- **CVSS** → vulnerability prioritization
- **SIEM/SOAR tools** → detection & response

## Strategic Value

MITRE transforms security from:

> “Defend blindly”

into:

> “Defend against how attackers actually operate.”

## Summary

MITRE is:

- A **foundational cybersecurity knowledge ecosystem**
- Essential for:
  - Threat intelligence
  - Detection engineering
  - Modern security operations

It provides:

- Real-world attack modeling (ATT&CK)
- Vulnerability understanding (CWE)
- Attack patterns (CAPEC)
- Defensive strategies (D3FEND)

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
