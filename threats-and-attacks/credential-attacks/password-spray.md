---
title: Password Spray
area: threats and attacks
level: unrated
status: draft
last_verified: unverified
tags: [migrated, credentials]
migrated_from: Security.html, page 84
---

# Password Spray

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

A **password spraying attack** is a **brute force variant** where an attacker attempts to log into **many accounts using a small set of common passwords**, rather than trying many passwords against a single account.

The key goal is to **avoid account lockouts** caused by too many failed attempts on a single user.

### Categorization

- **Vector-Based:** Authentication systems (web portals, VPNs, cloud apps, APIs, Active Directory).
- **Technique-Based:** Low-frequency brute force attack.
- **Objective-Based:** Gaining unauthorized access to multiple accounts without triggering lockouts.

## How it works

1. **Target Enumeration:**
   - Attacker collects a list of usernames (via OSINT, breached data, scraping directories).
2. **Password List Selection:**
   - Chooses a handful of **common or likely passwords** (e.g., `Winter2025!`, `Password123`).
3. **Slow & Distributed Attempts:**
   - Tries one password against many accounts, waits a period of time (hours or days), then tries the next password.
4. **Credential Match:**
   - If one account uses the guessed password, the attacker gains access.
5. **Post-Compromise:**
   - Uses the compromised account for data theft, privilege escalation, or lateral movement.

## Password spray vs brute force

| **Brute Force** | **Password Spraying** |
| --- | --- |
| Focuses on **one account**, tries many passwords. | Focuses on **many accounts**, tries few passwords. |
| Triggers account lockouts quickly. | Designed to avoid lockouts by spreading attempts. |
| Loud and easy to detect. | Stealthier and harder to spot in logs. |

## Common targets

- **Enterprise Email Portals:** OWA, Microsoft 365, Gmail for Business.
- **VPN Gateways & Remote Access Tools:** Cisco AnyConnect, Pulse Secure.
- **Cloud Applications:** Salesforce, AWS console, Azure.
- **Single Sign-On (SSO) Systems.**
- **Active Directory Services.**

## Technical aspects

- Uses **slow rate attempts** (low-and-slow attack) to bypass security thresholds.
- May leverage **botnets** or **cloud IP rotation** to avoid IP-based detection.
- Often automated with tools like:
  - **CrackMapExec**
  - **Hydra**
  - **MSOLSpray**
  - **FireProx** (for IP rotation)
- Relies on users choosing **weak or seasonal passwords**.

## Psychological & strategic factors

- Exploits human habits:
  - Use of predictable passwords tied to seasons, company names, or years (`Summer2025!`).
  - Password reuse across services.
  - Minimal variation in password changes.

## Impact

- **Initial Foothold:** Access to internal systems or email accounts.
- **Data Breach:** Exfiltration of sensitive information.
- **Business Email Compromise (BEC):** Wire fraud, invoice scams.
- **Privilege Escalation:** Moving from standard to admin accounts.
- **Lateral Movement:** Accessing other internal systems.

## Detection and prevention

## Detection

- Look for:
  - Multiple failed login attempts **across many accounts** from a single IP.
  - Low-frequency login failures spread over time.
  - Authentication attempts from unusual geolocations.
- Use SIEM rules and correlation searches.

### Prevention

- **Technical:**
  - Enforce **multi-factor authentication (MFA)** for all accounts.
  - Implement **account lockout thresholds** and **incremental delays**.
  - Require strong password policies (length, complexity, no reuse).
  - Enable conditional access rules (geofencing, risk-based login challenges).
- **Organizational:**
  - User training to avoid predictable password patterns.
  - Regular password audits and automated expiration.
- **Monitoring:**
  - Deploy identity protection tools (e.g., Microsoft Defender for Identity).
  - Enable detailed logging on authentication endpoints.

## Password spraying in the modern threat landscape

- Common in **APT campaigns** as a stealthy initial access vector.
- Often used in combination with **credential stuffing** when partial credentials are known.
- Particularly effective against organizations **without MFA**.
- Frequently automated and **run over weeks** to evade detection.

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
