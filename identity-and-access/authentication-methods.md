---
title: Authentication methods
area: identity and access
level: unrated
status: draft
last_verified: unverified
tags: [migrated, authentication]
migrated_from: Security.html, page 94
---

# Authentication methods

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## Methods

### Password-Based Authentication

- **Description:** Users provide a password to verify their identity.
- **Advantages:**
  - Simple and widely adopted.
  - Easy to implement.
- **Disadvantages:**
  - Susceptible to weak passwords, phishing, and brute-force attacks.
  - Difficult to manage securely without additional measures.

#### Multi-Factor Authentication (MFA)

- **Description:** Combines two or more authentication factors (e.g., password, OTP, biometric).
- **Advantages:**
  - Significantly enhances security.
  - Reduces the risk of compromised credentials.
- **Disadvantages:**
  - Requires additional setup and maintenance.
  - May impact user convenience.

##### Biometric Authentication

- **Description:** Uses unique physical characteristics (e.g., fingerprints, facial recognition).
- **Advantages:**
  - Highly secure; hard to replicate.
  - Convenient; no need to remember passwords.
- **Disadvantages:**
  - Expensive hardware and implementation.
  - Privacy concerns and potential for false positives/negatives.

##### Token-Based Authentication

- **Description:** Users authenticate using a physical or digital token (e.g., hardware device, app-generated codes).
- **Advantages:**
  - Strong security; tokens are hard to duplicate.
  - Can work offline in some cases.
- **Disadvantages:**
  - Risk of token loss or theft.
  - May add operational costs.

##### Certificate-Based Authentication

- **Description:** Users authenticate using digital certificates issued by a trusted Certificate Authority (CA).
- **Advantages:**
  - Highly secure; prevents phishing and MITM attacks.
  - Eliminates password management for users.
- **Disadvantages:**
  - Complex implementation.
  - Requires infrastructure for issuing and managing certificates.

##### Single Sign-On (SSO)

- **Description:** Allows users to access multiple systems with one set of credentials.
- **Advantages:**
  - Simplifies user experience.
  - Reduces password fatigue.
- **Disadvantages:**
  - A single compromised account can impact multiple systems.
  - Dependency on the SSO provider.

##### OAuth/OpenID Connect

- **Description:** Enables authentication via third-party providers (e.g., Google, Facebook).
- **Advantages:**
  - Eliminates password storage for the service.
  - Enhances user convenience.
- **Disadvantages:**
  - Relies on third-party security.
  - Complex to implement correctly.

##### SMS/Email-Based One-Time Passwords (OTPs)

- **Description:** Sends a temporary code via SMS or email for authentication.
- **Advantages:**
  - Easy to use and implement.
  - Adds a second layer of security.
- **Disadvantages:**
  - Vulnerable to SIM-swapping and phishing.
  - Depends on network availability.

##### Hardware Security Keys (e.g., YubiKey)

- **Description:** Users authenticate by connecting a physical key to their device.
- **Advantages:**
  - Extremely secure; resistant to phishing.
  - Simple and fast for users.
- **Disadvantages:**
  - Cost of hardware.
  - Risk of loss or theft.

##### Behavioral Biometrics

- **Description:** Analyzes user behavior patterns (e.g., typing speed, mouse movement).
- **Advantages:**
  - Non-intrusive and continuous.
  - Hard to replicate.
- **Disadvantages:**
  - Requires advanced technology and processing.
  - May have accuracy issues.

##### IP Address-Based Authentication

- **Description:** Grants access based on the user's IP address.
- **Advantages:**
  - Simple to configure.
  - Useful for restricting access by location.
- **Disadvantages:**
  - Ineffective against IP spoofing.
  - Limits access flexibility.

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
