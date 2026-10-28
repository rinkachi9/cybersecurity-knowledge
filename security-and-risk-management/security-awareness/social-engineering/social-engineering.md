# Social engineering

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

**Social engineering** is a **non-technical attack technique** that relies on **human manipulation** rather than direct exploitation of technical vulnerabilities.

The attacker **deceives, influences, or persuades** individuals into divulging confidential information, performing actions, or granting access that compromises security.

### Categorization

- **Vector-Based:** Human interaction (in-person, phone, email, social media, instant messaging).
- **Technique-Based:** Psychological manipulation, deception.
- **Objective-Based:** Obtaining confidential information, gaining unauthorized access, influencing behavior.

## Core principle

Social engineering works by **exploiting human psychology** - specifically:

- Trust in others.
- Desire to be helpful.
- Tendency to avoid conflict.
- Fear of consequences.
- Willingness to follow authority.

## How it works

Typical stages:

1. **Research & Reconnaissance:**
   - Gather information on the target via public records, social media, or prior breaches.
2. **Engagement:**
   - Approach the target via the chosen medium (email, phone, in-person, etc.).
3. **Exploitation:**
   - Use psychological triggers (urgency, authority, empathy) to influence the target’s behavior.
4. **Execution:**
   - The victim reveals information, clicks a malicious link, or grants physical access.
5. **Exit & Covering Tracks:**
   - The attacker leaves the interaction without raising suspicion, possibly setting up for future attacks.

## Common types

| **Type** | **Description** | **Example** |
| --- | --- | --- |
| **Phishing** | Fraudulent communication designed to steal data. | Fake “bank login” email. |
| **Spear Phishing** | Targeted phishing for a specific person/org. | CFO receives tailored invoice scam. |
| **Whaling** | Phishing aimed at executives. | CEO receives legal threat email. |
| **Vishing** | Voice phishing over the phone. | Fake tech support requesting login. |
| **Smishing** | Phishing over SMS. | “Delivery failed” message with a malicious link. |
| **Pretexting** | Creating a fabricated scenario to gain trust. | Impersonating IT staff to reset passwords. |
| **Baiting** | Offering something enticing in exchange for information. | Free USB drive loaded with malware. |
| **Tailgating** | Following someone into a restricted area. | Entering behind an employee without a badge. |
| **Shoulder Surfing** | Observing confidential information directly. | Watching someone type a password. |
| **Quid Pro Quo** | Offering a service in exchange for access. | “I’ll fix your PC if you give me admin credentials.” |

## Psychological principles exploited

- **Authority:** “I’m from IT/security, I need your password.”
- **Urgency:** “Your account will be disabled in 15 minutes unless you act.”
- **Fear:** “We’ve detected suspicious activity - verify now.”
- **Reciprocity:** Giving a small favor to encourage compliance.
- **Social Proof:** “Other employees already completed this request.”
- **Liking:** Building rapport so the victim feels obliged to help.
- **Scarcity:** “This offer expires today - sign in now.”

## Impact

- **Credential Theft:** Unauthorized access to systems or accounts.
- **Data Breach:** Confidential data exposure.
- **Financial Loss:** Fraudulent transfers, scams.
- **Operational Disruption:** System downtime, compromised workflows.
- **Reputational Damage:** Loss of trust among customers or partners.

## Detection and prevention

## Detection

- Unusual requests for sensitive data.
- Requests bypassing normal procedures.
- Inconsistencies in communication (tone, sender details).

### Prevention

- **Technical:**
  - MFA to mitigate stolen credentials.
  - Email filtering, anti-phishing tools.
- **Behavioral:**
  - Verify identities before sharing information or granting access.
  - Be cautious with unsolicited requests.
- **Organizational:**
  - Regular security awareness training.
  - Phishing simulations to test readiness.
  - Clear reporting channels for suspicious activity.

## Social engineering in modern threat landscape

- Increasingly blended with **cyber-physical attacks** (e.g., tailgating combined with malware USB drops).
- Used as a **first-stage attack** for ransomware and APT campaigns.
- Leveraged in **supply chain attacks** - targeting vendors or partners for indirect access.

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
