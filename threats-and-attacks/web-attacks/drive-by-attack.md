# Drive-By Attack

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

A **drive-by attack** (or **drive-by download attack**) is a cyberattack where **malware is automatically downloaded and executed** on a victim’s device simply by visiting a compromised or malicious website - without the victim intentionally downloading anything.

The key characteristic: **no obvious interaction required** (other than viewing the page), making it stealthy and dangerous.

### Categorization

- **Vector-Based:** Web browsing, malicious advertisements, compromised websites.
- **Technique-Based:** Exploitation of browser or plugin vulnerabilities, silent malware delivery.
- **Objective-Based:** Infect a victim’s system without explicit user action beyond visiting a webpage.

## How it works

1. **Website Compromise or Malicious Setup:**
   - Attacker compromises a legitimate site or creates a malicious one.
2. **Exploit Delivery:**
   - Injects malicious code into the website (often JavaScript or iframe) or through malvertising (malicious ads on legitimate sites).
3. **Vulnerability Exploitation:**
   - When the victim visits the page, an **exploit kit** scans for vulnerabilities in:
     - Browsers (Chrome, Firefox, Edge, Safari)
     - Plugins (Flash, Java, Silverlight)
     - PDF readers, media players
     - Outdated operating systems
4. **Silent Download and Execution:**
   - Malware is downloaded in the background without prompts.
   - Exploits browser/OS flaws to bypass security warnings.
5. **Payload Execution:**
   - Installs ransomware, spyware, cryptominers, or remote access tools (RATs).
   - Establishes persistence and may connect to a command-and-control (C2) server.

## Common delivery mechanisms

- **Compromised Legitimate Websites:** Often high-traffic or industry-specific sites.
- **Malvertising:** Injecting malicious ads into trusted ad networks.
- **Watering Hole Attacks:** Compromising sites frequented by a specific target group.
- **Search Engine Poisoning:** Using SEO techniques to push malicious sites to top search results.

## Technical aspects

- **Exploit Kits:** Toolkits (e.g., RIG, Magnitude) automate vulnerability scanning and exploitation.
- **Redirect Chains:** Multiple hidden redirections to hide the source of infection.
- **Fileless Malware:** Sometimes directly executes in memory without writing files to disk.
- **Zero-Day Exploits:** Drive-bys often use unpatched vulnerabilities for maximum effectiveness.

## Psychological and strategic factors

- **Trust in Websites:** Victims assume the visited site is safe (especially if it’s familiar).
- **Invisible Nature:** The attack leaves no visible download prompt.
- **Routine Behavior:** Exploits normal web browsing patterns, increasing exposure.

## Impact

- **Immediate Malware Infection:** Without user awareness.
- **Credential Theft:** Through keyloggers or form grabbers.
- **System Compromise:** Remote access for further exploitation.
- **Financial Loss:** Ransomware payments, fraud.
- **Botnet Enrollment:** Device becomes part of a larger attack network.

## Detection and prevention

### Detection

- Monitor for unusual outbound traffic (C2 connections).
- Endpoint detection & response (EDR) tools to catch suspicious processes.
- Website integrity monitoring for owners.

### Prevention

- **For Users:**
  - Keep browsers, plugins, and OS fully patched.
  - Disable or remove unnecessary plugins.
  - Use script-blocking browser extensions (e.g., NoScript, uBlock Origin).
  - Use reputable endpoint protection with web-filtering.
- **For Website Owners:**
  - Apply CMS and plugin updates promptly.
  - Use a Web Application Firewall (WAF).
  - Scan for injected scripts regularly.
- **Organizational:**
  - DNS filtering to block known malicious domains.
  - Security awareness training about malicious ads and untrusted links.

## Drive-By attacks in the modern threat landscape

- Frequently used as **initial infection vector** for ransomware campaigns.
- Common in **watering hole** and **malvertising** strategies.
- Increasing shift towards **fileless drive-bys** to evade antivirus.
- Often part of **state-sponsored APT campaigns** for stealthy initial access.

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
