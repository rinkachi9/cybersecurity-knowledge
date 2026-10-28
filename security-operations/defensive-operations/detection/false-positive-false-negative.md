# False Negative / False Positive

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

In cybersecurity, detection systems (like antivirus, intrusion detection systems, or SIEM platforms) must decide whether an event is **malicious (a threat)** or **benign (not a threat)**. Errors in this decision-making can fall into two categories:

## False Positive (Type I Error)

A **false positive** occurs when a security system **incorrectly flags benign activity as malicious**.

**Impact:**

- Wastes time and resources investigating non-threats
- Can block legitimate user actions or services
- Leads to "alert fatigue" in security teams
- Can cause users to lose trust in the system

**Real-World Example:**

- A user tries to **upload a large file** to a cloud service, and the firewall detects it as a data exfiltration attempt - even though it's just a backup.
- **Legitimate scripts** used by IT for automation are flagged as malware by an antivirus.

## False Negative (Type II Error)

A **false negative** occurs when a real malicious action **goes undetected** by the security system.

**Impact:**

- The **most dangerous** kind of error
- Real threats enter the system without detection
- Can lead to data breaches, ransomware attacks, system compromise
- Undermines trust in the security system's effectiveness

**Real-World Example:**

- A **new variant of ransomware** bypasses traditional antivirus because its signature hasn’t been added yet - resulting in undetected file encryption and ransom demand.
- A **phishing email** evades spam filters and is delivered to a CEO’s inbox, leading to a compromised account.

## Balancing detection

Security teams strive to:

- **Maximize:**
  - **True Positives**: Correctly detected threats
  - **True Negatives**: Correctly ignored benign actions
- **Minimize:**
  - **False Positives**: Avoid unnecessary alerts
  - **False Negatives**: Never miss a real threat

This tradeoff is often visualized in **machine learning** and **SIEM tuning**, where tuning sensitivity too high can cause false positives, while setting it too low can let attacks slip by.

## Example

| Tool | False Positive Example | False Negative Example |
| --- | --- | --- |
| **Antivirus** | Flags a safe program as malware | Misses a zero-day trojan |
| **WAF (Web App Firewall)** | Blocks legitimate form submission | Fails to detect a SQL injection |
| **SIEM** | Raises alert for normal user behavior | Misses lateral movement by attacker |
| **Spam Filter** | Flags a newsletter as phishing | Misses a real phishing email |

## Best practices

- **Regular tuning** of security tools
- Use **behavioral-based and anomaly detection**, not just signature matching
- Implement **threat intelligence** and context-aware alerts
- Train **analysts to validate alerts** effectively
- Use **machine learning models** with precision/recall optimization

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Common mistakes

TODO: list frequent misunderstandings and failure modes, each with its fix.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
