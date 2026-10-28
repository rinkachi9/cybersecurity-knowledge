# MITRE D3FEND

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

MITRE D3FEND is a **knowledge graph of defensive cybersecurity techniques** developed by MITRE.

It provides:

- A structured catalog of **defensive methods**
- Relationships between:
  - Defensive techniques
  - Attack techniques (MITRE ATT&CK)

**Core objective:**

To answer:

> “How do we defend against specific attacker behaviors?”

---

### Importance

Traditional security approaches:

- Focus on tools (WAF, IDS, SIEM)
- Lack structured mapping to attacker behavior

MITRE D3FEND addresses this by:

- Linking **defenses directly to attack techniques**
- Enabling **defense engineering**
- Supporting:
  - Detection design
  - Security architecture
  - Blue team operations

This makes it:

- Critical for **modern defensive strategies**
- Essential for:
  - SOC teams
  - Detection engineers
  - Cloud security architects

---

### Core philosophy

MITRE D3FEND is built around:

---

#### Defense-Centric Modeling

Instead of:

> “What can attackers do?”

D3FEND asks:

> “How can we detect, prevent, and respond?”

---

#### Knowledge Graph Approach

D3FEND is not just a list:

- It models relationships between:
  - Attacks
  - Defenses
  - Data sources

---

#### Countermeasure Mapping

Every defense is linked to:

- Specific ATT&CK techniques

---

#### Engineering-Driven Security

Focus on:

- Practical implementation
- Detection and response capabilities

---

### Key concepts

---

#### Defensive Techniques

Structured actions to:

- Detect
- Prevent
- Respond

---

#### Defensive Tactics

High-level defensive goals.

Examples:

- Harden
- Detect
- Isolate
- Deceive

---

#### Artifacts

System elements analyzed or protected:

- Files
- Processes
- Network traffic
- Credentials

---

#### Relationships

D3FEND defines:

- How defenses relate to:
  - ATT&CK techniques
  - System artifacts

---

### D3FEND Model Structure

```java
ATT&CK Technique (Attack)
        ↓
D3FEND Technique (Defense)
        ↓
Artifact (What is protected/observed)
```

---

### D3FEND Defensive Techniques (Examples)

---

#### 1. Process Monitoring

**Purpose:**

Detect suspicious execution.

---

**Example:**

- Monitor unusual process behavior
- Detect credential dumping attempts

---

**Mapped ATT&CK:**

- Credential Dumping

---

---

#### 2. Network Traffic Analysis

**Purpose:**

Detect malicious communication.

---

**Example:**

- Detect Command & Control (C2)
- Identify abnormal traffic patterns

---

---

#### 3. Credential Hardening

**Purpose:**

Protect authentication data.

---

**Example:**

- Secure storage of credentials
- Token protection

---

---

#### 4. Application Hardening

**Purpose:**

Reduce attack surface.

---

**Example:**

- Input validation
- Secure configuration

---

---

#### 5. Execution Isolation

**Purpose:**

Limit impact of compromised processes.

---

**Example:**

- Container isolation
- Sandbox environments

---

---

#### 6. Access Control Enforcement

**Purpose:**

Prevent unauthorized actions.

---

**Example:**

- RBAC
- IAM policies

---

---

#### 7. Deception Techniques

**Purpose:**

Mislead attackers.

---

**Example:**

- Honeypots
- Fake credentials

---

### Practical Example

---

#### Scenario

Attack:

```java
Credential Dumping (ATT&CK)
```

---

#### D3FEND Mapping

---

**Defensive Techniques:**

- Process monitoring
- Memory protection
- Credential encryption

---

**Artifacts:**

- Process memory
- Authentication tokens

---

**Implementation:**

- Monitor LSASS access
- Detect abnormal memory reads
- Alert + isolate host

---

### D3FEND vs ATT&CK

| Aspect | D3FEND | ATT&CK |
| --- | --- | --- |
| Focus | Defense | Attack |
| Perspective | Blue team | Red team |
| Purpose | Countermeasures | Behavior modeling |
| Relationship | Maps to ATT&CK | Source of threats |

---

### D3FEND vs CAPEC

| Aspect | D3FEND | CAPEC |
| --- | --- | --- |
| Focus | Defense | Attack patterns |
| Use case | Detection & mitigation | Threat modeling |

---

### D3FEND in DevSecOps

---

#### Design Phase

- Define security controls mapped to ATT&CK

---

#### Development

- Implement defensive patterns:
  - Input validation
  - Secure APIs

---

#### CI/CD

- Enforce:
  - Security policies
  - Configuration checks

---

#### Runtime (Critical)

- Detection engineering:
  - Map logs → D3FEND techniques

---

#### Example Pipeline

```text
Threat → ATT&CK → D3FEND → Detection rule → Alert → Response
```

---

### D3FEND in Cloud & Kubernetes

---

#### Common Use Cases

- IAM hardening
- API security
- Network segmentation

---

#### Kubernetes Examples

- Pod isolation
- RBAC enforcement
- Runtime monitoring

---

#### GCP Example

- IAM least privilege
- Audit logging
- API Gateway protection

---

D3FEND helps:

- Implement Zero Trust
- Detect lateral movement
- Secure cloud-native systems

---

### Detection Engineering with D3FEND

D3FEND enables:

---

#### Structured Detection Design

- Map ATT&CK → detection logic

---

#### Example

```diff
Technique: Lateral Movement
Detection:
- Unusual API calls
- Cross-namespace access
Response:
- Block + alert
```

---

#### SIEM Integration

- Build rules based on:
  - Defensive techniques
  - Artifacts

---

### Strengths

- Direct mapping to attacker behavior
- Supports detection engineering
- Practical and actionable
- Integrates with ATT&CK

---

### Weaknesses

- Less mature than ATT&CK
- Requires expertise
- Complex knowledge graph

---

### Common pitfalls

- Not linking to ATT&CK
- Treating as theoretical
- Ignoring implementation details
- Lack of integration with SIEM

---

### Skills Required

- Detection engineering
- Security architecture
- Cloud security
- SOC operations

---

### When to Use D3FEND

Best suited for:

- Detection engineering
- Security architecture
- SOC operations
- Blue team strategy

---

### When NOT to Use Alone

Avoid using D3FEND alone for:

- Threat modeling
- Risk management

---

### Integration with Other Frameworks

D3FEND works best with:

- **MITRE ATT&CK** → attack mapping
- **CWE** → root causes
- **CAPEC** → attack patterns
- **NIST CSF** → governance
- **SIEM/SOAR** → operations

---

### Strategic Value

MITRE D3FEND transforms security from:

> “Deploy security tools”

into:

> “Engineer defenses mapped to real attacker behavior.”

---

### Summary

MITRE D3FEND is:

- A **defensive counterpart to MITRE ATT&CK**
- Focused on:
  - Detection
  - Prevention
  - Response

It provides:

- Structured defensive techniques
- Mapping to real-world attacks
- Strong support for modern security operations

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
