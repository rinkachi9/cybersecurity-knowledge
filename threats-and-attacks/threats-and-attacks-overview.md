---
title: Threats & attacks
area: threats and attacks
level: unrated
status: draft
last_verified: unverified
tags: [migrated]
migrated_from: Security.html, page 65
---

# Threats & attacks

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## Introduction

Cybersecurity threats and attacks are deliberate attempts to breach the confidentiality, integrity, or availability of information or systems. These actions can be initiated by individuals, groups, or organizations with malicious intent. Understanding the categories, types, and broader context of threats and attacks is essential for developing effective defense mechanisms.

## Threats classifications

### Passive attacks

Passive attacks are attempts to intercept or monitor communications or data without altering them. The attacker’s primary goal is to gather information without being detected.

**Characteristics:**

- **Non-disruptive:** Does not interfere with normal system operations.
- **Stealthy:** The goal is to remain undetected while collecting sensitive information.

**Examples:**

- **Eavesdropping:** Intercepting network traffic to collect sensitive information like login credentials.
- **Traffic Analysis:** Monitoring communication patterns to deduce information, even if the content is encrypted.
- **Shoulder Surfing:** Observing someone's screen or keyboard to steal sensitive data.

**Impact:**

- Loss of confidentiality.
- Preparation for future, more harmful attacks (e.g., spear phishing).

**Defense Mechanisms:**

- Encryption (e.g., SSL/TLS for data in transit).
- Strong authentication mechanisms.
- Network monitoring to detect unusual behavior.

#### Active attacks

Active attacks involve direct actions by the attacker to alter, disrupt, or damage systems, networks, or data.

**Characteristics:**

- **Disruptive:** Actively interferes with normal system operations.
- **Detectable:** More likely to be noticed compared to passive attacks.

**Examples:**

- **Man-in-the-Middle (MitM):** Intercepting and altering communication between two parties.
- **Denial-of-Service (DoS):** Overloading a system to make it unavailable.
- **Malware Deployment:** Infecting systems with malicious software like ransomware or spyware.
- **Data Tampering:** Altering sensitive data to compromise its integrity.

**Impact:**

- Compromised integrity and availability of systems or data.
- Operational disruptions and financial losses.

**Defense Mechanisms:**

- Intrusion Detection Systems (IDS) and Intrusion Prevention Systems (IPS).
- Firewalls and secure configurations.
- Patching vulnerabilities to reduce attack vectors.

#### Insider attacks

Insider attacks are initiated by individuals within the organization, such as employees, contractors, or partners. These individuals have legitimate access to systems but misuse it for malicious purposes.

**Characteristics:**

- **Internal Threat:** Exploits authorized access.
- **Intentional or Accidental:** Can be malicious (e.g., sabotage) or unintentional (e.g., human error).

**Examples:**

- **Data Theft:** Stealing sensitive data like trade secrets or customer information.
- **Sabotage:** Deleting critical files or damaging infrastructure.
- **Privilege Abuse:** Using elevated privileges to bypass security controls.

**Impact:**

- Significant damage due to familiarity with internal systems.
- Breach of trust and loss of intellectual property.

**Defense Mechanisms:**

- Implement Role-Based Access Control (RBAC) to limit privileges.
- Monitor user activities using logging and auditing tools.
- Conduct regular training to prevent accidental insider threats.

#### Distribution attacks

Distribution attacks involve compromising hardware, software, or supply chains before they are delivered to the end user. These attacks are designed to introduce vulnerabilities into systems during production or distribution.

**Characteristics:**

- **Pre-Deployment:** Occurs during manufacturing, packaging, or distribution stages.
- **Stealthy:** Often difficult to detect until the compromised product is used.

**Examples:**

- **Supply Chain Attacks:** Introducing malicious code or hardware into legitimate software or devices.
- **Software Updates:** Distributing malware disguised as legitimate updates.
- **Hardware Trojans:** Implanting malicious hardware components into devices.

**Impact:**

- Wide-scale compromise if distributed to multiple users.
- Long-lasting vulnerabilities due to the difficulty of detection.

**Defense Mechanisms:**

- Vetting suppliers and partners through rigorous security standards.
- Verifying integrity and authenticity of software and hardware.
- Implementing secure development and deployment practices.

#### Summary

| **Category** | **Description** | **Goal** | **Key Difference** |
| --- | --- | --- | --- |
| **Passive Attack** | Intercepting data without altering it. | Stealthy data gathering. | No disruption to systems. |
| **Active Attack** | Actively interfering with systems or communications. | Disruption, damage, or theft. | Direct and disruptive. |
| **Insider Attack** | Exploiting legitimate access within an organization. | Misuse of trust or access. | Originates internally. |
| **Distribution Attack** | Compromising systems during the production or distribution phase. | Inserting vulnerabilities early. | Targets the supply chain or deployment. |

## Categories of threats

Cybersecurity threats can be broadly categorized based on their origin, intent, and nature of impact:

1. **By Origin:**
   - **Internal Threats:** Initiated by insiders such as employees, contractors, or other individuals with access to an organization’s systems.
   - **External Threats:** Originating from external entities, such as hackers, cybercriminal organizations, or state-sponsored actors.
2. **By Intent:**
   - **Malicious Threats:** Deliberate attempts to cause harm, steal information, or disrupt services.
   - **Accidental Threats:** Resulting from unintentional actions, such as human error or misconfigurations.
   - **Environmental Threats:** Natural disasters or external events that impact systems indirectly (e.g., power outages).
3. **By Target:**
   - **Data Breaches:** Focused on accessing or exposing sensitive data.
   - **System Disruption:** Aimed at interrupting or degrading the performance of systems.
   - **Espionage:** Involves covert activities to gain unauthorized access to confidential information.

## Types of threats

1. **Human-Based Threats:**
   - **Social Engineering:** Manipulating individuals to divulge sensitive information.
   - **Phishing:** Deceptive attempts to acquire credentials or personal data.
2. **Malware Threats:**
   - **Viruses:** Malicious code that attaches to programs and spreads.
   - **Worms:** Standalone malware that replicates across systems.
   - **Ransomware:** Encrypts files and demands payment for decryption keys.
3. **Network Threats:**
   - **Man-in-the-Middle (MitM):** Intercepting and manipulating communications.
   - **DDoS Attacks:** Overloading systems or networks to disrupt service.
4. **Application Threats:**
   - Exploiting vulnerabilities in applications, such as outdated software or insecure APIs.
5. **Cloud and IoT Threats:**
   - Attacks targeting cloud environments or IoT devices, often exploiting weak security configurations.
6. **Advanced Persistent Threats (APTs):**
   - Sustained and targeted attacks, often carried out by well-funded groups, designed to gain long-term access to systems.

## Key elements

1. **Threat Actors:**
   - Individuals or entities responsible for initiating attacks.
   - Examples: Hackers, organized crime groups, nation-states, and hacktivists.
2. **Motivations:**
   - **Financial Gain:** Theft of data, extortion (e.g., ransomware).
   - **Political Objectives:** Espionage, propaganda, or sabotage.
   - **Ideological Goals:** Hacktivism to promote beliefs or values.
   - **Revenge or Malice:** Disgruntled insiders or former employees.
3. **Vectors of Attack:**
   - The methods or channels through which an attack is carried out:
     - **Email:** Phishing and spam.
     - **Web:** Insecure websites or malicious ads.
     - **Software:** Exploiting vulnerabilities in applications or systems.
     - **Networks:** Unsecured connections, such as public Wi-Fi.
4. **Stages of an Attack:**
   - **Reconnaissance:** Collecting information about the target.
   - **Weaponization:** Preparing the tools or exploits.
   - **Delivery:** Deploying the exploit or payload.
   - **Exploitation:** Executing the attack.
   - **Installation:** Establishing persistence (e.g., backdoors).
   - **Command and Control (C2):** Maintaining communication with compromised systems.
   - **Exfiltration/Impact:** Stealing data or causing disruption.

## Factors increasing threat likelihood

1. **Technological Complexity:** Increased attack surfaces due to interconnected devices, cloud services, and APIs.
2. **Human Error:** Misconfigurations, weak passwords, and unpatched systems are common vulnerabilities.
3. **Globalization and Remote Work:** Expanding threat vectors through global networks and unsecured home devices.
4. **Sophistication of Threat Actors:** Use of advanced tools and AI-driven attacks by cybercriminal organizations.

## Impact of threats

1. **Economic Losss:** Costs related to data breaches, ransomware payments, and system recovery.
2. **Reputation Damage:** Loss of trust from customers and partners due to security incidents.
3. **Regulatory Penalties:** Fines and legal actions for non-compliance with data protection laws (e.g., GDPR, HIPAA).
4. **Operational Disruption:** Downtime and reduced efficiency caused by attacks.
5. **National Security Risks:** Threats to critical infrastructure and government systems.

## Defense against threats

1. **Adopt a Multi-Layered Defense:** Implement firewalls, intrusion detection systems, endpoint protection, and regular updates.
2. **Promote Awareness:** Train users to recognize and avoid social engineering attacks.
3. **Regular Risk Assessments:** Continuously identify and mitigate vulnerabilities.
4. **Incident Response Plans:** Prepare robust protocols for detecting, responding to, and recovering from attacks.
5. **Collaborate and Share Intelligence:** Participate in threat intelligence sharing communities to stay informed about emerging threats.

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
