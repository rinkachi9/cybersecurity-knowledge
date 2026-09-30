# Federal Trade Commission (FTC) Act

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

The **Federal Trade Commission (FTC)** is an independent U.S. government agency responsible for:

- Consumer protection
- Competition enforcement
- Privacy and data security oversight

Unlike regulations (e.g., GDPR, HIPAA), the FTC:

> Enforces privacy and security through legal authority rather than prescribing a single formal framework.

---

### Core objective

To prevent:

> Unfair or deceptive practices in commerce
>
> , including misuse of personal data and weak security practices.

---

### Why FTC matters in cybersecurity

FTC acts as a **de facto regulator of data security in the U.S.**

It enforces:

- Reasonable security practices
- Truthful privacy policies
- Protection against data misuse

Key implication:

> If your system is insecure or your privacy claims are misleading → FTC can take legal action.

---

### Legal foundation

---

#### Section 5 of the FTC Act

The FTC enforces:

- **Unfair practices**
- **Deceptive practices**

---

#### Definitions

---

##### Deceptive

- Misleading statements about:
  - Security
  - Privacy
  - Data handling

Example:

- Claiming “data is encrypted” when it is not

---

##### Unfair

- Practices causing harm not reasonably avoidable

Example:

- Storing sensitive data without protection

---

### FTC enforcement model

---

FTC does NOT define strict controls like:

- GDPR
- HIPAA

Instead, it enforces:

> “Reasonable security” based on industry standards

---

#### What “reasonable security” means

Depends on:

- Data sensitivity
- System complexity
- Industry practices

---

### Core areas of FTC enforcement

---

### 1. Data Security

---

Organizations must:

- Protect personal data
- Prevent unauthorized access

---

### 2. Privacy Practices

---

Must ensure:

- Transparency
- Honesty in data usage

---

### 3. Data Minimization

---

- Collect only necessary data

---

### 4. Third-Party Risk

---

- Responsible for vendors and partners

---

### 5. Incident Response

---

- Proper handling of breaches

---

### Key FTC expectations (derived from cases)

---

#### 1. Reasonable Security Controls

- Encryption
- Access control
- Secure storage

---

#### 2. Secure Development Practices

- Avoid common vulnerabilities (OWASP)
- Regular testing

---

#### 3. Monitoring & Detection

- Log access
- Detect anomalies

---

#### 4. Data Lifecycle Management

- Secure deletion
- Retention policies

---

#### 5. Employee Training

- Security awareness

---

### FTC in DevSecOps

---

#### Design phase

- Define:
  - Data usage
  - Privacy commitments

---

#### Development

- Align code with:
  - Declared privacy policy

---

#### CI/CD

- Security testing:
  - SAST
  - DAST
  - Dependency scanning

---

#### Runtime

- Monitor:
  - Data access
  - Security events

---

#### Example pipeline

```text
Design → Privacy alignment → Development → Security testing → Deploy → Monitor → Audit
```

---

### FTC in cloud & Kubernetes

---

#### Cloud risks

- Misconfigured storage
- Weak IAM
- Public exposure of data

---

#### Kubernetes risks

- Secrets leakage
- Over-permissive RBAC
- Logging sensitive data

---

#### FTC expectation

If breach occurs due to:

- Poor configuration
- Negligence

→ FTC may classify as **unfair practice**

---

### Practical example

---

#### Scenario

Company states:

> “We use industry-standard security”

---

#### Reality

- No encryption
- Weak authentication
- No logging

---

#### FTC interpretation

- **Deceptive practice** (false claim)
- **Unfair practice** (inadequate security)

---

#### Result

- Fines
- Mandatory security improvements
- Ongoing audits

---

### FTC vs GDPR

| Aspect | FTC | GDPR |
| --- | --- | --- |
| Type | Enforcement agency | Regulation |
| Approach | Case-based | Rule-based |
| Scope | U.S. commerce | EU personal data |

---

### FTC vs HIPAA

| Aspect | FTC | HIPAA |
| --- | --- | --- |
| Scope | General commerce | Healthcare |
| Structure | Flexible | Prescriptive |

---

### FTC vs OWASP

| Aspect | FTC | OWASP |
| --- | --- | --- |
| Role | Enforcement | Guidance |
| Nature | Legal | Technical |

---

### Strengths

- Flexible and adaptable
- Broad enforcement scope
- Strong deterrent through penalties

---

### Weaknesses

- Lack of clear technical standards
- Reactive (case-based)
- Ambiguity in “reasonable security”

---

### Common pitfalls

- Misleading privacy policies
- Weak security controls
- Lack of documentation
- Ignoring third-party risks
- No incident response plan

---

### Skills required

- Security architecture
- Legal awareness
- Risk management
- DevSecOps practices

---

### When FTC applies

Applies when:

- Operating in the U.S. market
- Handling consumer data

---

### Strategic approach

---

#### 1. Align policy with reality

- Privacy policy must reflect actual implementation

---

#### 2. Implement reasonable security

- Based on:
  - OWASP
  - NIST
  - Industry best practices

---

#### 3. Document everything

- Policies
- Controls
- Decisions

---

#### 4. Monitor continuously

- Logs
- Alerts

---

#### 5. Manage third-party risk

- Vendor security assessments

---

### Integration with other frameworks

---

FTC enforcement aligns with:

- NIST CSF → defines “reasonable security”
- ISO 27001 → structured controls
- OWASP → application security
- GDPR → stricter privacy model

---

### Strategic value

FTC transforms organizations from:

> “We say we are secure”

into:

> “We must prove that our security and privacy claims are real and enforced.”

---

### Summary

FTC is:

- A **key enforcement authority in U.S. cybersecurity and privacy**
- Focused on:
  - Consumer protection
  - Data security
  - Honest practices

It enforces:

- Reasonable security
- Truthful data handling
- Accountability

---

### Key insight

FTC does not tell you exactly how to secure systems.

Instead, it ensures:

> If your security is weak or misleading, you will be held accountable.

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
