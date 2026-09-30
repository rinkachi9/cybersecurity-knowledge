---
title: MITRE CAPEC
area: threat intelligence
level: unrated
status: draft
last_verified: unverified
tags: [migrated, mitre, capec]
migrated_from: Security.html, page 46
---

# MITRE CAPEC

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

MITRE CAPEC is a **structured knowledge base of attack patterns** maintained by MITRE.

It describes:

- **How attacks are performed**
- The **techniques and methods attackers use**
- The **conditions required for successful exploitation**

**Core objective:**

To provide a **standardized catalog of attack patterns** that helps organizations understand:

> “How attacks actually work in practice.”

---

### Importance

Traditional approaches (e.g., CVE, CVSS):

- Focus on **specific vulnerabilities**
- Do not explain **how attacks are executed**

MITRE CAPEC fills this gap by:

- Modeling **attack behavior patterns**
- Connecting:
  - Vulnerabilities (CWE)
  - Attacker techniques (ATT&CK)

This makes it:

- Critical for:
  - Threat modeling
  - Secure design
  - Security training
  - Red teaming

---

### Core philosophy

CAPEC is built around:

---

#### Pattern-Based Security

Instead of focusing on individual vulnerabilities:

> CAPEC focuses on reusable attack patterns.

---

#### Abstraction Levels

CAPEC defines attacks at different levels:

- High-level concepts
- Detailed execution techniques

---

#### Knowledge Reuse

Attack patterns:

- Can be reused across systems
- Help anticipate new threats

---

#### Bridging Gap

CAPEC bridges:

- **CWE (weaknesses)**
- **ATT&CK (behavior)**

---

### Key concepts

---

#### Attack Pattern

A description of:

- How an attack is performed
- Preconditions
- Execution flow
- Expected outcomes

---

#### Abstraction Levels

CAPEC defines three levels:

---

##### Meta Attack Patterns

- Very high-level
- Abstract attack classes

Example:

- Manipulating input data

---

##### Standard Attack Patterns

- Most commonly used
- Balanced detail level

Example:

- SQL Injection

---

##### Detailed Attack Patterns

- Highly specific
- Step-by-step execution

Example:

- Blind SQL Injection via time-based inference

---

---

#### Relationships

CAPEC connects to:

- CWE → weaknesses exploited
- ATT&CK → attacker techniques

---

### CAPEC Model Structure

Each CAPEC entry contains:

---

#### 1. Description

- Overview of the attack

---

#### 2. Prerequisites

Conditions required:

- System state
- Misconfigurations
- Weak controls

---

#### 3. Execution Flow

Step-by-step attack process:

```text
Reconnaissance → Exploitation → Post-exploitation
```

---

#### 4. Attack Techniques

Methods used:

- Injection
- Social engineering
- API abuse

---

#### 5. Consequences

Impact:

- Data breach
- System compromise
- Privilege escalation

---

#### 6. Mitigations

Recommended controls

---

#### 7. Related Weaknesses (CWE)

Mapping to root causes

---

### CAPEC Example

---

#### CAPEC-66: SQL Injection

---

#### Description

Injection of malicious SQL into input fields.

---

#### Prerequisites

- Unsanitized user input
- Direct database queries

---

#### Execution Flow

```text
1. Identify input field
2. Inject SQL payload
3. Execute query
4. Extract data
```

---

#### Consequences

- Data leakage
- Data manipulation
- Full database compromise

---

#### Mitigations

- Parameterized queries
- Input validation
- ORM usage

---

#### Related CWE

- CWE-89 (SQL Injection)

---

### CAPEC vs ATT&CK

| Aspect | CAPEC | ATT&CK |
| --- | --- | --- |
| Focus | Attack patterns | Attacker behavior |
| Level | Application/system | Full attack lifecycle |
| Detail | Execution-focused | Behavior-focused |
| Use case | Secure design | Detection & response |

---

### CAPEC vs CWE

| Aspect | CAPEC | CWE |
| --- | --- | --- |
| Focus | Attack methods | Weaknesses |
| Perspective | Attacker | Developer |
| Use case | Threat modeling | Secure coding |

---

### CAPEC in DevSecOps

---

#### Design Phase

- Identify attack patterns for system components
- Threat modeling (STRIDE + CAPEC)

---

#### Development

- Prevent patterns via:
  - Secure coding
  - Input validation
  - API security

---

#### CI/CD

- SAST tools map findings to CWE → CAPEC patterns
- Security testing based on attack patterns

---

#### Testing

- DAST and penetration testing simulate CAPEC attacks

---

#### Runtime

- Detection rules based on:
  - Known attack behaviors

---

### CAPEC in Cloud & Kubernetes

---

#### Common Patterns

- API abuse
- Credential theft
- Misconfiguration exploitation

---

#### Kubernetes Examples

- Exploiting RBAC misconfiguration
- Container escape
- Abuse of service accounts

---

#### Cloud Examples (GCP/AWS)

- IAM privilege escalation
- Public storage exposure
- API misuse

---

CAPEC helps:

- Anticipate attack paths
- Design secure architectures
- Prevent common misconfigurations

---

### Strengths

- Detailed attack descriptions
- Strong link to vulnerabilities (CWE)
- Useful for training and design
- Reusable patterns

---

### Weaknesses

- Large and complex
- Requires interpretation
- Less focused on detection than ATT&CK

---

### Common pitfalls

- Ignoring CAPEC in design phase
- Treating it as theoretical only
- Not linking to real vulnerabilities
- Overlooking cloud-specific patterns

---

### Skills Required

- Application security knowledge
- Secure coding practices
- Threat modeling
- Understanding of OWASP Top 10

---

### When to Use CAPEC

Best suited for:

- Secure design
- Threat modeling
- Application security
- Penetration testing

---

### When NOT to Use Alone

Avoid using CAPEC alone for:

- Detection engineering
- Risk prioritization

---

### Integration with Other Frameworks

CAPEC works best with:

- **CWE** → root causes
- **ATT&CK** → attacker behavior
- **OWASP Top 10** → common risks
- **PASTA / STRIDE** → threat modeling
- **CVSS** → prioritization

---

### Strategic Value

CAPEC transforms security from:

> “Fix vulnerabilities”

into:

> “Understand how attackers exploit them.”

---

### Summary

MITRE CAPEC is:

- A **comprehensive catalog of attack patterns**
- Essential for:
  - Secure design
  - Threat modeling
  - Security testing

It provides:

- Deep understanding of attack execution
- Link between vulnerabilities and attacker behavior
- Practical guidance for prevention

## Worked example

TODO: add a concrete, reproducible example that walks through the idea end to end.

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
