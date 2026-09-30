---
title: Brute Force Attack
area: threats and attacks
level: unrated
status: draft
last_verified: unverified
tags: [migrated, credentials]
migrated_from: Security.html, page 83
---

# Brute Force Attack

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

A **brute force attack** is a method of gaining access to a system, account, or encrypted data by **systematically trying all possible combinations** of passwords, keys, or other authentication credentials until the correct one is found.

It relies on **computational power and persistence** rather than exploiting specific vulnerabilities in software.

### Categorization

- **Vector-Based:** Network login portals, authentication systems, encrypted files, APIs.
- **Technique-Based:** Systematic guessing of credentials or encryption keys.
- **Objective-Based:** Gaining unauthorized access to accounts, systems, or encrypted data.

## How it works

1. **Target Identification:**
   - Attacker chooses a login interface, API, encrypted file, or cryptographic key.
2. **Automated Guessing:**
   - Uses scripts or tools to try credentials at high speed.
3. **Matching Credentials:**
   - When the correct combination is found, access is granted.
4. **Post-Compromise:**
   - Attacker escalates privileges, steals data, or moves laterally in the network.

## Common types

| **Type** | **Description** | **Example Tools** |
| --- | --- | --- |
| **Simple Brute Force** | Trying every possible combination. | Hydra, Medusa |
| **Dictionary Attack** | Using a precompiled list of possible passwords. | John the Ripper |
| **Credential Stuffing** | Using stolen username/password pairs from other breaches. | Sentry MBA |
| **Hybrid Attack** | Combining dictionary lists with variations (numbers, symbols). | Hashcat |
| **Reverse Brute Force** | Using a common password across many usernames. | Hydra |
| **Password Spraying** | Trying a few common passwords against many accounts to avoid lockouts. | CrackMapExec |
| **Keyspace Attack** | Exhaustively testing cryptographic keys. | Hashcat, Aircrack-ng |

## Technical aspects

- **Attack Speed:** Depends on processing power, network latency, and system rate limits.
- **Hash Cracking:** Brute force can be used against hashed passwords if hashes are leaked.
- **Distributed Attacks:** Botnets or cloud servers increase guessing speed.
- **Encryption Breaking:** High computational requirements for key brute forcing (e.g., AES, RSA).

## Psychological and strategic factors

- Relies on human tendency to:
  - Choose weak or common passwords.
  - Reuse passwords across multiple accounts.
  - Use predictable patterns (e.g., `Password123`).

## Impact

- **Unauthorized Access:** Accounts, systems, databases compromised.
- **Data Theft:** Exfiltration of sensitive or personal information.
- **Service Disruption:** Excessive login attempts may cause account lockouts.
- **Reputation Damage:** Customer trust eroded if breaches occur.
- **Regulatory Consequences:** GDPR, HIPAA violations if personal data is stolen.

## Detection and prevention

### Detection

- Monitor for:
  - High volumes of failed login attempts.
  - Multiple attempts from the same IP or across many IPs.
  - Access attempts at unusual times or geolocations.

## Prevention

- **Technical:**
  - Implement account lockouts or temporary bans after failed attempts.
  - Require strong, complex passwords.
  - Use multi-factor authentication (MFA).
  - Employ CAPTCHA challenges.
  - Rate-limit login requests.
  - Use salted and hashed password storage (bcrypt, Argon2).
- **Organizational:**
  - User education on password hygiene.
  - Security policies to enforce password rotation and uniqueness.
- **Advanced:**
  - Adaptive authentication that flags unusual behavior.
  - IP reputation filtering.

## Brute force in the modern threat landscape

- Increasingly **automated and distributed** using cloud infrastructure and botnets.
- Often part of **credential stuffing** campaigns leveraging leaked databases.
- Attackers use **rainbow tables** to speed up hash cracking (mitigated by strong salting).
- Many brute force attacks now target **APIs** and **IoT devices** with weak credentials.

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
