# Typosquatting

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

**Typosquatting** (also known as **URL hijacking** or **domain mimicry**) is a cyberattack technique where an attacker registers a domain name that is a **misspelled or visually similar version** of a legitimate website.

The goal is to exploit **typing mistakes** or visual confusion to trick users into visiting the malicious site.

### Categorization

- **Vector-Based:** Domain name abuse, malicious websites.
- **Technique-Based:** Deceptive URL manipulation, brand impersonation.
- **Objective-Based:** Credential theft, malware delivery, fraud, ad revenue, phishing.

## How it works

1. **Target Selection:**
   - Attacker chooses a popular brand, service, or organization (e.g., `paypal.com`).
2. **Domain Registration:**
   - Registers a domain with:
     - Common misspellings (e.g., `payapl.com`).
     - Missing/extra letters (e.g., `paypall.com`).
     - Keyboard adjacency errors (e.g., `payoal.com`).
     - Alternate top-level domains (TLDs) (e.g., `paypal.co` instead of `.com`).
     - Homoglyphs - visually similar characters (e.g., using `paуpal.com` with a Cyrillic “у”).
3. **Malicious Setup:**
   - Hosts a phishing page that mimics the legitimate site.
   - Serves malware or redirects to unwanted ads.
   - Uses the site for harvesting credentials or credit card details.
4. **Traffic Capture:**
   - Users make typos or click spoofed links.
   - The fake site captures sensitive data or infects the system.

## Common typosquatting variants

| **Variant Type** | **Description** | **Example** |
| --- | --- | --- |
| **Misspelling** | Common spelling mistakes. | `goggle.com` for `google.com`. |
| **Omission** | Missing letters. | `goole.com`. |
| **Addition** | Extra letters. | `googgle.com`. |
| **Transposition** | Swapped letters. | `goolge.com`. |
| **Hyphenation** | Adding or removing hyphens. | `face-book.com`. |
| **TLD Change** | Different domain endings. | `amazon.net` instead of `.com`. |
| **Homoglyph Attack** | Using lookalike characters. | `microsоft.com` (Cyrillic “o”). |

## Psychological and strategic factors

- **Trust in Familiarity:** Users see a domain that “looks right” at first glance.
- **Lack of Verification:** Many users don’t check URLs closely before entering credentials.
- **Speed Typing Errors:** Mistakes are common when typing on mobile devices.
- **Link Manipulation:** Attackers embed malicious URLs in ads, emails, or QR codes.

## Impact

- **Credential Theft:** Stolen usernames, passwords, and MFA codes.
- **Financial Fraud:** Unauthorized transactions using captured banking credentials.
- **Malware Infection:** Drive-by downloads or malicious scripts.
- **Brand Damage:** Legitimate organizations lose trust if customers are victimized.
- **Ad Fraud:** Redirecting to ad-heavy pages for revenue.

## Detection and prevention

### Detection

- Domain monitoring tools to detect registrations similar to your brand.
- DNS traffic analysis to spot visits to suspicious domains.
- Browser phishing/malware warnings.

### Prevention

- **For Organizations:**
  - Register common typos and similar domains proactively.
  - Use domain monitoring services.
  - Educate customers to verify URLs.
- **For Users:**
  - Bookmark important sites instead of typing them.
  - Check browser address bars carefully.
  - Use password managers (auto-fill only on exact domains).
- **Technical Measures:**
  - Enable HTTPS with proper certificates on official domains.
  - Implement brand protection with DMARC, SPF, and DKIM for emails.

## Typosquatting in the modern threat landscape

- Frequently used in **phishing campaigns** to imitate login portals.
- Common in **malvertising**, where typos lead to ad fraud networks.
- Increasingly combined with **homoglyph attacks** using Unicode characters to evade visual detection.
- Actively exploited in **APT campaigns** for credential harvesting.

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
