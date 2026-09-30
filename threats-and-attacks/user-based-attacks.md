---
title: User-based attacks
area: threats and attacks
level: unrated
status: draft
last_verified: unverified
tags: [migrated, user-based]
migrated_from: Security.html, page 67
---

# User-based attacks

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

**User-based attacks** (also called **human-centric attacks**) are cyberattacks that target the **users of a system**, rather than its software or infrastructure directly. These attacks exploit **psychological manipulation**, **lack of awareness**, or **access privileges** to gain unauthorized access, steal information, or compromise systems.

These attacks are effective because **humans are often the weakest link** in security.

### Goals

- **Credential theft** (usernames, passwords, tokens)
- **Privilege escalation** or lateral movement
- **Sensitive data exfiltration**
- **Initial access to a secure network**
- **Bypassing technical controls via social engineering**

## Types

### Phishing

- Fraudulent emails or messages that trick users into clicking malicious links or revealing credentials.
- Variants: Spear phishing (targeted), Whaling (executive targeting), Smishing (SMS), Vishing (voice).

#### Social Engineering

- Manipulating users through deception to bypass security (e.g., pretending to be IT support).
- Includes pretexting, baiting, tailgating, and impersonation.

#### Credential Stuffing

- Attackers use previously leaked username/password pairs to try logging into user accounts on other services.

#### Password Attacks

- Brute-force: trying many combinations
- Dictionary: using common passwords
- Guessing: based on user info (e.g., birthdays, pet names)

#### Insider Threats

- Legitimate users abusing their access intentionally (malicious insider) or unintentionally (negligent insider).

#### Malicious Attachments

- Users are tricked into opening infected files that install malware (e.g., keyloggers, ransomware).

#### Session Hijacking

- Attackers steal user session tokens or cookies to impersonate users.

#### Clickjacking

- Deceptive interface tricks users into clicking hidden malicious elements.

## Mitigation

| Control | Description |
| --- | --- |
| **Security Awareness Training** | Educate users about phishing, social engineering, and suspicious behavior. |
| **Multi-Factor Authentication (MFA)** | Adds an extra layer of protection beyond passwords. |
| **Least Privilege Access** | Limit user permissions to only what’s needed for their role. |
| **Strong Password Policies** | Enforce complexity, rotation, and avoid reuse. |
| **Email Filtering & Anti-Phishing** | Block malicious emails and links before they reach users. |
| **Behavioral Monitoring** | Detect anomalies in user actions (e.g., logins from unusual locations). |
| **Zero Trust Architecture** | Trust no one by default - verify every access request. |

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
