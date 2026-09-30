---
title: Phishing
area: threats and attacks
level: unrated
status: draft
last_verified: unverified
tags: [migrated, phishing, social-engineering]
migrated_from: Security.html, page 73
---

# Phishing

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

Phishing is a **social engineering attack** where attackers impersonate trusted entities to trick individuals into revealing sensitive information, clicking malicious links, or downloading malware.

It relies on **psychological manipulation** more than technical exploitation.

Some of the most common types of phishing attacks today include:

- **Business Email Compromise (BEC):** A threat actor sends an email message that seems to be from a known source to make a seemingly legitimate request for information, in order to obtain a financial advantage.
- **Spear phishing:** A malicious email attack that targets a specific user or group of users. The email seems to originate from a trusted source.
- **Whaling:** A form of spear phishing. Threat actors target company executives to gain access to sensitive data.
- **Vishing:** The exploitation of electronic voice communication to obtain sensitive information or to impersonate a known source.
- **Smishing:** The use of text messages to trick users, in order to obtain sensitive information or to impersonate a known source.

### Categorization

**Phishing** belongs primarily to:

- **Vector-Based:** Email, messaging platforms, fake websites.
- **Technique-Based:** Social engineering.
- **Objective-Based:** Credential theft, malware delivery, fraud.

## How it works

Typical phishing campaign steps:

1. **Target Identification:** Selecting individuals or organizations.
2. **Lure Creation:** Crafting a convincing message or website.
3. **Delivery:** Sending via email, SMS, social media, or instant messaging.
4. **Deception:** Persuading the victim to take an unsafe action (click a link, open an attachment, provide credentials).
5. **Exploitation:** Capturing sensitive data or executing malicious code.
6. **Follow-Up Attack:** Using the stolen information for fraud, ransomware deployment, or lateral movement.

## Common types

| **Type** | **Description** | **Example** |
| --- | --- | --- |
| **Email Phishing** | Mass emails pretending to be from legitimate entities. | Fake “Account Suspension” email from a bank. |
| **Spear Phishing** | Highly targeted emails tailored to a specific individual or organization. | Email to CFO referencing actual internal projects. |
| **Whaling** | Spear phishing aimed at executives or high-profile targets. | CEO receives fake legal request. |
| **Clone Phishing** | Legitimate email is copied, but links or attachments are replaced with malicious ones. | Invoice email cloned with a fake payment link. |
| **Vishing** | Voice phishing over the phone. | Caller pretends to be IT support requesting login details. |
| **Smishing** | SMS-based phishing. | Fake “package delivery” text with a malicious link. |
| **Search Engine Phishing** | Malicious sites ranked in search results to trick users. | Fake banking site in Google Ads. |

## Psychological principles exploited

- **Urgency:** "Your account will be suspended in 24 hours."
- **Authority:** Pretending to be from IT, HR, law enforcement.
- **Fear:** Threatening legal action, account loss.
- **Curiosity:** "You have a new secure message."
- **Greed:** Offering rewards, prizes, or financial gain.

## Technical aspects

- **Spoofed Email Headers:** Using forged `From` addresses.
- **Lookalike Domains:** Slightly altered URLs (e.g., `paypa1.com` instead of `paypal.com`).
- **HTTPS Abuse:** Fake sites using valid SSL certificates to appear legitimate.
- **Attachment Payloads:** Malicious macros, executables, PDFs with exploits.
- **Pharming:** Redirecting legitimate domain requests to malicious servers.

## Impact of successful phishing

- **Credential Theft:** Compromised accounts, unauthorized access.
- **Financial Loss:** Fraudulent transactions, ransom demands.
- **Data Breach:** Leakage of personal or corporate data.
- **Malware/Ransomware Deployment:** Initial infection vector.
- **Reputation Damage:** Loss of customer and partner trust.

## Detection and prevention

### Detection

- Email security gateways with phishing detection.
- AI-based filtering for suspicious content and domains.
- DNS filtering to block malicious URLs.
- User reporting channels.

### Prevention

- **Technical:**
  - SPF, DKIM, DMARC for email authentication.
  - Link and attachment sandboxing.
  - Browser-based phishing protection.
- **Human:**
  - Security awareness training.
  - Phishing simulation exercises.
  - Promote “hover before click” habits.
- **Policy:**
  - Multi-factor authentication (MFA).
  - Limit privileges to reduce damage if credentials are stolen.

## Role of phishing

Phishing is often just **step one** in a more complex attack:

- Initial foothold for ransomware campaigns.
- Entry point for **Business Email Compromise (BEC)**.
- Starting point for lateral movement inside corporate networks.

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
