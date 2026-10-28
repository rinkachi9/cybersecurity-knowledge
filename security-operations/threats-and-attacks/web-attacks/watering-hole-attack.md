# Watering Hole Attack

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

A **watering hole attack** is a **targeted cyberattack** where an adversary compromises a legitimate website that a specific group of victims regularly visits.

The compromised site is used to **silently deliver malware** or redirect visitors to a malicious site, infecting them without their direct awareness.

The name comes from the hunting strategy of predators waiting at a watering hole - a place prey naturally visits.

### Categorization

- **Vector-Based:** Web compromise, supply chain via legitimate sites.
- **Technique-Based:** Strategic compromise, targeted malware delivery.
- **Objective-Based:** Infecting a specific group of users by exploiting a site they trust and visit frequently.

## How it works

1. **Target Group Identification:**
   - Attacker researches the habits of the intended victims (e.g., employees of a company, members of an industry).
2. **Watering Hole Selection:**
   - A legitimate website frequently visited by the target group is identified (e.g., industry news site, vendor portal, partner website).
3. **Website Compromise:**
   - Attacker exploits a vulnerability in the site’s code, CMS, or server to insert malicious code.
4. **Infection Mechanism:**
   - When visitors access the site, they are:
     - Served with an **exploit kit** targeting their browser or plugins.
     - Redirected to a malicious site for further compromise.
     - Delivered malware via drive-by download.
5. **Post-Infection Activities:**
   - Installation of backdoors, spyware, or credential stealers.
   - Lateral movement into the target’s organization.

## Common targets

- Industry-specific news or forum websites.
- Supplier or partner portals.
- Government or defense-related resource sites.
- Niche hobby or community sites linked to the target group.

## Technical aspects

- **Exploit Kits:** Malicious toolkits exploiting browser or plugin vulnerabilities.
- **JavaScript Injection:** Adding malicious scripts to legitimate pages.
- **Redirection Chains:** Using compromised ad networks or iframe injections.
- **Zero-Day Exploits:** Often used to ensure infection before detection.

## Psychological and strategic factors

- **Trust Exploitation:** The victim trusts the legitimate site and thus lowers suspicion.
- **Routine Exploitation:** Attackers know targets will eventually visit the compromised site naturally.
- **Low Suspicion Entry:** The victim is not directly contacted (unlike phishing), so the attack is stealthier.

## Impact

- **Targeted Compromise:** Only the desired group is affected, reducing noise and increasing stealth.
- **Malware Deployment:** Remote access Trojans (RATs), spyware, ransomware.
- **Credential Theft:** Stolen login details to sensitive systems.
- **Intelligence Gathering:** Surveillance and espionage against organizations or individuals.
- **Supply Chain Impact:** Compromised partner/vendor networks.

## Detection and prevention

### Detection

- Monitor outbound network traffic for unusual destinations.
- Check website integrity with file integrity monitoring.
- Use web proxy filtering and DNS security.

### Prevention

- **For Users:**
  - Keep browsers, plugins, and OS updated.
  - Use script-blocking browser extensions.
  - Employ endpoint protection with web reputation services.
- **For Website Owners:**
  - Patch CMS and server vulnerabilities promptly.
  - Monitor for unauthorized code changes.
  - Implement a Web Application Firewall (WAF).

## Watering hole in the modern threat landscape

- Frequently used in **Advanced Persistent Threat (APT)** campaigns.
- Often combined with **zero-day exploits** for higher success rates.
- Increasingly targeting **mobile browsers** and **industry-specific apps**.
- Common in **state-sponsored attacks** for espionage.

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
