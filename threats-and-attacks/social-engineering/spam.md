# Spam

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

**Spam** refers to the mass sending of unsolicited, irrelevant, or inappropriate messages - typically via email - to a large number of recipients.

Although spam may sometimes be harmless advertising, it frequently carries **malicious payloads** or **links to phishing sites**.

### Categorization

Spam is primarily:

- **Vector-Based:** Email, instant messaging, social media.
- **Technique-Based:** Mass unsolicited communication.
- **Objective-Based:** Advertising, fraud, phishing delivery, malware distribution.

While spam itself is often seen as a **nuisance attack**, it is also a **delivery mechanism** for more dangerous threats like phishing or ransomware.

## How it works

1. **Email Address Harvesting:**
   - Spammers collect email addresses from public websites, data breaches, malware-infected devices, or purchased lists.
2. **Message Creation:**
   - The spam message may be promotional, fraudulent, or malicious in nature.
3. **Mass Sending:**
   - Using botnets, compromised accounts, or bulk mailing tools to send millions of messages.
4. **Delivery and Bypass:**
   - Techniques like **domain spoofing**, **snowshoe spamming** (spreading messages over multiple IPs/domains), or abusing legitimate email services to bypass spam filters.
5. **Action by Recipient:**
   - Clicking a link, opening an attachment, replying with sensitive info, or simply being exposed to unwanted content.

## Types

| **Type** | **Description** | **Example** |
| --- | --- | --- |
| **Advertising Spam** | Unwanted promotional messages. | Fake weight loss pills. |
| **Phishing Spam** | Email designed to steal credentials. | “Your PayPal account is locked” link. |
| **Malware Spam** | Spam carrying malicious attachments or links to infected downloads. | Word doc with macro virus. |
| **419/Nigerian Scams** | Advance-fee fraud promising large sums in exchange for upfront payment. | “I am a prince who needs your help…” |
| **Snowshoe Spam** | Low-volume spam sent from many IP addresses/domains to avoid detection. | Promotional emails from hundreds of domains. |
| **SEO Spam** | Messages intended to boost search rankings via posted links. | Forum posts with backlinks. |

## Technical aspects

- **Botnets:** Many spam campaigns are powered by infected devices sending emails without user knowledge.
- **Email Spoofing:** Faking sender details to appear trustworthy.
- **Use of Open Relays:** Exploiting poorly configured mail servers to send spam anonymously.
- **Content Obfuscation:** Using misspellings or special characters to bypass keyword filters.
- **Image Spam:** Embedding text in images to evade text-based spam filters.

## Psychological principles exploited

- **Curiosity:** Intriguing subject lines to encourage opening.
- **Greed:** Promises of prizes, winnings, or investments.
- **Fear:** Threats of account closures or legal issues.
- **Urgency:** “Act now before your account is closed!”

## Impact of spam

- **Productivity Loss:** Wastes employee time.
- **Security Risk:** Serves as a delivery vector for phishing and malware.
- **Financial Impact:** Possible fraud or ransom payments.
- **Reputation Damage:** If an organization’s domain is hijacked for spam.

## Detection and Prevention

### Detection

- Spam filters based on:
  - **Heuristic analysis:** Pattern recognition of spam traits.
  - **Bayesian filtering:** Statistical probability models.
  - **Blacklists:** IP/domain reputation databases.
  - **Machine learning models:** AI-driven content analysis.

### Prevention

- **Technical:**
  - Implement SPF, DKIM, and DMARC to prevent spoofing.
  - Maintain updated spam filter rules.
  - Use real-time blocklists (RBLs) for known spam IPs.
- **User Awareness:**
  - Train employees not to click on suspicious links or attachments.
- **Incident Response:**
  - Block compromised accounts and reset credentials immediately.

## Spam vs. SPIM

- **Spam:** Unsolicited messages via **email**.
- **SPIM (Spam over Instant Messaging):** Unsolicited messages sent via instant messaging apps (e.g., Teams, Slack, WhatsApp).
- SPIM often contains phishing links or malware, exploiting the perceived trust in direct messaging.

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
