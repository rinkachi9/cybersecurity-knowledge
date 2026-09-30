---
title: General Data Protection Regulation (GDPR)
area: privacy and data protection
level: unrated
status: draft
last_verified: unverified
tags: [migrated, gdpr, regulations]
migrated_from: Security.html, page 29
---

# General Data Protection Regulation (GDPR)

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

The **General Data Protection Regulation (GDPR)** is a **European Union regulation** governing how **personal data of EU residents** is collected, processed, stored, and protected.

It applies to:

- Organizations within the EU
- Organizations **outside the EU** that process EU residents’ data

**Core objective:**

To ensure:

> Full control of personal data by individuals, with strict obligations on organizations to protect and justify its processing.

## Importance

GDPR is one of the **most impactful data protection laws globally**.

It enforces:

- Strict data protection requirements
- Heavy penalties (up to 4% of global annual revenue)
- Accountability and auditability

From a technical perspective, it drives:

- Secure system design
- Privacy-aware architecture
- Strong data governance

---

### Core philosophy

GDPR is built around:

---

#### User-Centric Privacy

Users own their data:

- Organizations are custodians, not owners

---

#### Accountability

Organizations must:

- Prove compliance (not just claim it)

---

#### Risk-Based Approach

Controls depend on:

- Sensitivity of data
- Risk to individuals

---

#### Privacy by Design & Default

Privacy must be:

- Embedded in architecture
- Enabled by default

---

### Key principles (Article 5)

---

#### 1. Lawfulness, Fairness, Transparency

- Data must be processed legally
- Users must be informed

---

#### 2. Purpose Limitation

- Data collected for specific purposes only

---

#### 3. Data Minimization

- Collect only what is necessary

---

#### 4. Accuracy

- Data must be up-to-date

---

#### 5. Storage Limitation

- Retain data only as long as needed

---

#### 6. Integrity and Confidentiality

- Ensure security (CIA triad)

---

#### 7. Accountability

- Must demonstrate compliance

---

### Key roles

---

#### Data Controller

- Defines:
  - Why data is processed
  - How data is processed

---

#### Data Processor

- Processes data on behalf of controller

---

#### Data Subject

- The individual whose data is processed

---

#### Data Protection Officer (DPO)

Required in certain cases:

- Monitors compliance
- Acts as contact point

---

### Data subject rights

---

#### 1. Right of Access

- Users can request their data

---

#### 2. Right to Rectification

- Correct inaccurate data

---

#### 3. Right to Erasure (“Right to be Forgotten”)

- Delete personal data

---

#### 4. Right to Restriction

- Limit processing

---

#### 5. Right to Data Portability

- Export data in machine-readable format

---

#### 6. Right to Object

- Stop certain types of processing

---

#### 7. Rights related to automated decision-making

- Protection from profiling

---

### Legal bases for processing

---

At least one must apply:

- Consent
- Contract
- Legal obligation
- Vital interests
- Public task
- Legitimate interest

---

### Data lifecycle under GDPR

---

```text
Collection → Processing → Storage → Sharing → Retention → Deletion
```

Each stage must be:

- Documented
- Secured
- Justified

---

### Technical & organizational measures (TOMs)

---

### 1. Encryption

- Data at rest (disk, DB)
- Data in transit (TLS)

---

### 2. Pseudonymization

- Replace identifiers with tokens

---

### 3. Access control

- RBAC / ABAC
- Least privilege

---

### 4. Logging & auditing

- Access tracking
- Change history

---

### 5. Data masking

- Hide sensitive fields

---

### 6. Backup & recovery

- Ensure availability

---

### 7. Incident response

- Detect and respond to breaches

---

### Data breach requirements

---

#### Definition

- Unauthorized access, disclosure, or loss

---

#### Obligations

- Notify authority within **72 hours**
- Inform users if high risk

---

### GDPR in DevSecOps

---

#### Design phase

- Data classification
- Privacy impact assessment (DPIA)

---

#### Development

- Secure coding (OWASP)
- Avoid overexposing data (DTO patterns)

---

#### CI/CD

- Secrets scanning
- Dependency scanning
- Policy enforcement

---

#### Runtime

- Monitoring access to sensitive data
- Anomaly detection

---

#### Example pipeline

```text
Design → DPIA → Development → Security checks → Deploy → Monitor → Audit
```

---

### GDPR in cloud & Kubernetes

---

#### Cloud risks

- Public storage buckets
- Misconfigured IAM
- Cross-region data transfer

---

#### Kubernetes risks

- Secrets in plaintext
- Logs with PII
- Over-permissive RBAC

---

#### Best practices (GKE context)

- Use Secret Manager
- Encrypt etcd
- Apply Workload Identity
- Enforce network policies

---

### Practical example

---

#### Scenario

User registers in an app:

---

#### GDPR-compliant approach

- Collect only:
  - Email
  - Password
- Store:
  - Password hashed (bcrypt/argon2)
  - Email encrypted
- Provide:
  - Data export endpoint
  - Data deletion endpoint
- Log:
  - Access to user data

---

### GDPR vs other frameworks

---

#### GDPR vs ISO 27001

| Aspect | GDPR | ISO 27001 |
| --- | --- | --- |
| Type | Regulation | Standard |
| Focus | Privacy | Information security |

---

#### GDPR vs NIST CSF

| Aspect | GDPR | NIST CSF |
| --- | --- | --- |
| Nature | Legal | Framework |
| Scope | Privacy | Cybersecurity |

---

#### GDPR vs CCPA

| Aspect | GDPR | CCPA |
| --- | --- | --- |
| Scope | EU | California |
| Strictness | Higher | Moderate |

---

### Strengths

- Strong user protection
- Global influence
- Forces secure design
- Clear legal obligations

---

### Weaknesses

- Complex implementation
- Ambiguity in interpretation
- High compliance cost

---

### Common pitfalls

- Over-collecting data
- Logging PII
- No deletion mechanisms
- Weak consent handling
- Ignoring third-party processors

---

### Skills required

- Data protection knowledge
- Security architecture
- Legal awareness
- DevSecOps practices

---

### When to apply GDPR

Mandatory if:

- Processing EU residents’ data

---

Recommended always for:

- Global products
- Privacy-focused systems

---

### Strategic value

GDPR transforms systems from:

> “Data-driven without constraints”

into:

> “Privacy-first, accountable, and secure.”

---

### Summary

GDPR is:

- The **most important privacy regulation globally**
- A driver of:
  - Secure architecture
  - Privacy-aware development
  - Responsible data handling

It enforces:

- User rights
- Data minimization
- Security controls

---

### Key insight

GDPR is not just compliance:

> It is a
>
> design paradigm for modern secure systems
>
> .

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
