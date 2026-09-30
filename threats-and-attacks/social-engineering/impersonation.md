---
title: Impersonation
area: threats and attacks
level: unrated
status: draft
last_verified: unverified
tags: [migrated, impersonation, social-engineering]
migrated_from: Security.html, page 79
---

# Impersonation

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

**Impersonation** is a **social engineering attack** where an adversary pretends to be a trusted individual, entity, or role in order to **deceive the target into granting access, sharing sensitive information, or performing specific actions**.

It can occur in both **physical and digital contexts** and often leverages **authority, familiarity, or urgency**.

### Categorization

- **Vector-Based:** In-person, phone, email, chat, video conferencing, or digital identity spoofing.
- **Technique-Based:** Social engineering, identity fraud, deception.
- **Objective-Based:** Gaining trust to obtain information, access systems, or bypass security controls.

## How it works

1. **Preparation & Research:**
   - Attacker gathers information about the person or entity they plan to impersonate (name, role, appearance, communication style).
2. **Establishing Credibility:**
   - Using believable identifiers (uniforms, email domains, phone caller ID spoofing, fake IDs).
3. **Engagement:**
   - Approaching the target through in-person conversation, email, phone calls, or messaging platforms.
4. **Exploitation:**
   - Convincing the target to provide information, perform an action, or allow physical/digital access.
5. **Exit & Covering Tracks:**
   - Leaving the interaction without raising suspicion, often removing signs of unauthorized presence.

## Common forms

| **Type** | **Description** | **Example** |
| --- | --- | --- |
| **Employee Impersonation** | Pretending to be a coworker or manager. | Attacker poses as HR to request personal info. |
| **Vendor/Contractor Impersonation** | Masquerading as a service provider. | Fake IT technician requesting server access. |
| **Authority Impersonation** | Posing as police, government officials, auditors. | Caller claims to be from the tax office. |
| **Digital Identity Spoofing** | Using fake or stolen email, domain, or account. | Spear phishing from a lookalike CEO email. |
| **Help Desk/Support Impersonation** | Pretending to be IT support to request credentials. | “We need your password to resolve a system issue.” |
| **Customer Impersonation** | Acting as a legitimate customer to access accounts. | Calling bank pretending to be the account holder. |

## Psychological principles exploited

- **Authority:** Targets obey perceived figures of power.
- **Familiarity:** Pretending to be someone the target knows or expects to interact with.
- **Urgency:** Creating pressure to act quickly without verifying.
- **Trust Bias:** Exploiting the human tendency to trust apparent insiders.
- **Reciprocity:** Offering a favor to encourage cooperation.

## Tools & techniques used

- **Caller ID Spoofing:** Making a phone call appear from a trusted number.
- **Email Spoofing:** Forging sender details.
- **Fake Credentials:** Badges, uniforms, or business cards.
- **Deepfakes:** Synthetic audio or video to imitate someone’s voice or appearance.
- **Domain Squatting:** Using domains visually similar to legitimate ones.

## Impact

- **Data Breach:** Unauthorized access to sensitive information.
- **Credential Theft:** Compromised login details for systems or applications.
- **Financial Fraud:** Manipulating employees into transferring funds (e.g., Business Email Compromise).
- **Physical Security Breach:** Unauthorized access to restricted areas.
- **Reputation Damage:** Loss of trust if impersonation leads to customer or partner harm.

## Detection and prevention

## Detection

- Inconsistencies in communication style or knowledge.
- Requests bypassing standard procedures.
- Suspicious caller IDs or email domains.
- Verification failure when cross-checking identity.

### Prevention

- **Technical:**
  - Implement SPF, DKIM, DMARC for email authentication.
  - Use MFA to make stolen credentials less useful.
  - Caller verification systems.
- **Behavioral:**
  - Train employees to verify requests for sensitive actions, even from known people.
  - Establish “call back” policies for verification.
- **Physical:**
  - Require visible identification and check credentials for visitors.
  - Escort all non-employees inside secure areas.
- **Organizational:**
  - Clearly define and enforce identity verification protocols.

## Impersonation in the modern threat landscape

- **Business Email Compromise (BEC)** attacks often rely on digital impersonation of executives.
- Deepfake technology is making **voice and video impersonation** increasingly convincing.
- Hybrid work environments create more impersonation opportunities due to reduced in-person verification.

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
