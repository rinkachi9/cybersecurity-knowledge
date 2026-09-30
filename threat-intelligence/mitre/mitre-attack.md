# MITRE ATT&CK®

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

MITRE ATT&CK® (Adversarial Tactics, Techniques, and Common Knowledge) is a **globally recognized knowledge base of adversary behavior**, maintained by MITRE.

It models:

- **How attackers operate in real-world environments**
- The **techniques they use across the attack lifecycle**
- The **tactics (goals) they aim to achieve**

**Core objective:**

To provide a **structured, evidence-based model of attacker behavior** that enables organizations to:

- Detect threats
- Improve defenses
- Align security controls with real attack patterns

---

### Importance

Traditional security approaches:

- Focus on vulnerabilities (e.g., CVE, CVSS)
- Often ignore attacker behavior
- Lack context for detection

MITRE ATT&CK addresses this by:

- Modeling **real-world adversarial actions**
- Enabling **behavior-based detection**
- Supporting:
  - SOC operations
  - Threat hunting
  - Red teaming

This makes it:

- Foundational for **modern cybersecurity**
- Essential for **cloud, Kubernetes, API-based systems**

---

### Core philosophy

MITRE ATT&CK is built around:

---

#### Adversary Behavior Modeling

Focus on:

> “What attackers do” instead of “what vulnerabilities exist”

---

#### Evidence-Based Knowledge

All techniques are:

- Based on real-world incidents
- Continuously updated

---

#### Tactics as Objectives

Each attack step is mapped to:

- A **goal (tactic)**

---

#### Techniques as Actions

Each tactic is achieved via:

- Specific **techniques and sub-techniques**

---

### Key concepts

---

#### Tactics

High-level attacker goals.

Examples:

- Initial Access
- Execution
- Persistence
- Privilege Escalation
- Defense Evasion
- Credential Access
- Discovery
- Lateral Movement
- Collection
- Command and Control
- Exfiltration
- Impact

---

#### Techniques

Methods used to achieve tactics.

Example:

- Phishing
- Exploiting public-facing application
- Credential dumping

---

#### Sub-techniques

More granular actions.

Example:

- Credential Dumping → LSASS memory extraction

---

#### Procedures

Real-world implementations of techniques:

- Specific malware
- Specific attacker campaigns

---

#### Data Sources

Logs and telemetry used for detection:

- Process logs
- Network traffic
- API calls
- Cloud audit logs

---

### MITRE ATT&CK Matrices

ATT&CK is organized into **matrices** based on environment:

---

#### 1. Enterprise Matrix

Covers:

- Windows
- Linux
- macOS
- Cloud
- Containers

---

#### 2. Mobile Matrix

Covers:

- Android
- iOS

---

#### 3. ICS Matrix

Covers:

- Industrial Control Systems

---

### MITRE ATT&CK Model Structure

```text
Tactics (Why?)
   ↓
Techniques (How?)
   ↓
Sub-techniques (Detailed How?)
   ↓
Procedures (Real-world usage)
```

---

### ATT&CK Tactics (Detailed Breakdown)

---

#### 1. Initial Access

How attackers enter the system.

Examples:

- Phishing
- Exploiting public-facing applications
- Supply chain compromise

---

#### 2. Execution

Running malicious code.

Examples:

- Command-line execution
- Script execution
- Container execution

---

#### 3. Persistence

Maintaining access.

Examples:

- Backdoors
- Scheduled tasks
- Kubernetes cronjobs abuse

---

#### 4. Privilege Escalation

Gaining higher privileges.

Examples:

- Exploiting vulnerabilities
- IAM misconfigurations

---

#### 5. Defense Evasion

Avoiding detection.

Examples:

- Log tampering
- Obfuscation
- Disabling security tools

---

#### 6. Credential Access

Stealing credentials.

Examples:

- Keylogging
- Credential dumping
- Token theft

---

#### 7. Discovery

Understanding the environment.

Examples:

- Network scanning
- Service discovery
- Cloud resource enumeration

---

#### 8. Lateral Movement

Moving within the system.

Examples:

- Remote service exploitation
- SSH pivoting
- Kubernetes API abuse

---

#### 9. Collection

Gathering data.

Examples:

- File access
- Database queries

---

#### 10. Command and Control (C2)

Communicating with attacker infrastructure.

Examples:

- HTTP/HTTPS beaconing
- DNS tunneling

---

#### 11. Exfiltration

Extracting data.

Examples:

- Data transfer over API
- Cloud storage abuse

---

#### 12. Impact

Final attacker objective.

Examples:

- Data destruction
- Ransomware
- Service disruption

---

### Practical Example (Cloud-Native)

**System:**

Kubernetes + API + Keycloak (OIDC)

---

#### Attack Flow (Mapped to ATT&CK)

```sql
Initial Access → Exploit API vulnerability
Execution → Run malicious container
Persistence → Create hidden CronJob
Privilege Escalation → Abuse RBAC
Discovery → Enumerate cluster resources
Lateral Movement → Access other namespaces
Credential Access → Steal service account tokens
Exfiltration → Send data to external server
```

---

### MITRE ATT&CK in DevSecOps

---

#### Design Phase

- Threat modeling (map threats to ATT&CK)
- Define detection requirements

---

#### Development

- Secure coding aligned with:
  - CWE
  - OWASP

---

#### CI/CD

- Scan for:
  - Vulnerabilities
  - Misconfigurations

---

#### Runtime (Critical)

- Detection engineering:
  - Map logs → ATT&CK techniques

---

#### Example Detection Rule

```text
Technique: Credential Dumping
Signal: Unusual process accessing memory (LSASS)
Action: Alert + isolate host
```

---

### MITRE ATT&CK in Cloud & Kubernetes

---

#### Common Cloud Techniques

- IAM privilege escalation
- API abuse
- Token theft

---

#### Kubernetes Examples

- Abuse of service accounts
- Container escape
- Misconfigured RBAC

---

#### GCP Example

- Abuse of IAM roles
- Service account key leakage
- API misuse via Apigee

---

### Detection Engineering with ATT&CK

ATT&CK is heavily used in:

---

#### SIEM

- Map alerts to techniques

---

#### Threat Hunting

- Search for specific behaviors

---

#### SOC Playbooks

- Define response per technique

---

#### Example

```text
Technique: Lateral Movement
Detection: Unusual SSH between nodes
Response: Block + investigate
```

---

### Strengths

- Real-world attacker modeling
- Widely adopted standard
- Strong support for detection engineering
- Continuously updated

---

### Weaknesses

- Large and complex
- Requires expertise
- Not a full risk framework
- Needs integration with other models

---

### Common pitfalls

- Treating ATT&CK as a checklist
- Not mapping to actual logs
- Ignoring cloud-specific adaptations
- Lack of prioritization

---

### Skills Required

- Threat intelligence
- Detection engineering
- Cloud security
- SOC operations

---

### When to Use MITRE ATT&CK

Best suited for:

- Threat detection
- Threat hunting
- SOC operations
- Red/Blue teaming
- Cloud security

---

### When NOT to Use Alone

Avoid using ATT&CK as:

- A full risk management framework
- A compliance framework

---

### Integration with Other Frameworks

Works best with:

- **PASTA** → attack simulation
- **STRIDE** → threat identification
- **CVSS** → severity scoring
- **NIST CSF** → governance
- **SIEM/SOAR** → operations

---

### Strategic Value

MITRE ATT&CK transforms security from:

> “Detect anomalies”

into:

> “Detect specific attacker behaviors.”

---

### Summary

MITRE ATT&CK is:

- The **industry standard for modeling attacker behavior**
- Essential for:
  - Detection engineering
  - Threat hunting
  - Cloud security

It provides:

- Structured attack lifecycle
- Real-world techniques
- Direct mapping to detection and response

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
