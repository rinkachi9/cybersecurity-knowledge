# Reconnaissance

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

**Reconnaissance** (often called **recon**) is the **first phase of a cyberattack or penetration test**, where an attacker collects as much information as possible about a target before attempting exploitation.

It’s essentially **digital or physical “scouting”** to identify weaknesses.

### Categorization

- **Vector-Based:** Network scanning, physical observation, open-source intelligence (OSINT), social engineering.
- **Technique-Based:** Information gathering, mapping targets.
- **Objective-Based:** Identifying potential vulnerabilities, mapping infrastructure, preparing for future attacks.

## Purpose

- Map the target’s **attack surface**.
- Identify **high-value targets** (HVTs).
- Gather details for **precision attacks**.
- Reduce risk of detection by understanding defensive measures before the attack.

## How it works

Recon is typically divided into two main types:

### Passive reconnaissance

- Gathering information **without directly interacting** with the target system.
- Harder to detect, uses public and open sources.
- Examples:
  - Searching WHOIS records.
  - Analyzing job postings for tech stack clues.
  - Gathering emails from public websites.
  - Monitoring social media posts.

### Active reconnaissance

- **Direct interaction** with the target’s systems or network.
- Easier to detect, but provides more accurate and detailed data.
- Examples:
  - Port scanning.
  - Banner grabbing.
  - Vulnerability scanning.
  - Sending crafted packets to elicit responses.

## Common methods

| **Method** | **Description** | **Example Tools** |
| --- | --- | --- |
| **OSINT Gathering** | Collecting publicly available information. | Maltego, Recon-ng, SpiderFoot |
| **WHOIS & DNS Recon** | Finding domain ownership and DNS info. | whois, nslookup, dig |
| **Network Scanning** | Identifying live hosts, open ports, services. | Nmap, Masscan |
| **Web App Mapping** | Enumerating web directories, parameters, APIs. | DirBuster, OWASP ZAP |
| **Social Media Mining** | Profiling targets via LinkedIn, Facebook, X. | Manual search, OSINT tools |
| **Email Harvesting** | Collecting valid email addresses for phishing. | theHarvester |
| **Physical Recon** | Observing premises, entry points, security measures. | Binoculars, cameras |

## Information gathered during recon

- **Technical:** IP ranges, domain names, open ports, software versions, SSL certificates, exposed APIs.
- **Human:** Names, job roles, contact details, behavioral patterns.
- **Organizational:** Suppliers, partners, technology stack, security vendors.
- **Physical:** Office layout, security cameras, employee badge protocols.

## Psychological and strategic aspects

- Reconnaissance is about **pattern discovery** - attackers look for regularities in human or system behavior.
- Often involves **blending data from multiple sources** to form a complete attack plan.
- Social engineering can be fueled by data gathered here (e.g., spear phishing emails tailored from LinkedIn info).

## Impact

- Provides attackers with **low-risk, high-value intelligence**.
- Enables highly targeted attacks (reducing chance of failure).
- Can be **ongoing** - some APTs maintain constant surveillance of targets.

## Detection and prevention

### Detection

- Monitoring for:
  - Unusual scanning activity.
  - Multiple failed login attempts from unknown IPs.
  - Abnormal DNS queries.
- Analyzing logs for reconnaissance patterns.

### Prevention

- **Technical:**
  - Restrict unnecessary service exposure.
  - Hide detailed version banners in services.
  - Use rate limiting and intrusion detection systems.
- **Organizational:**
  - Limit publicly available sensitive information.
  - Train employees on OPSEC (Operational Security).
- **Physical:**
  - Secure premises against unauthorized observation.
  - Dispose of documents securely (to prevent dumpster diving).

## Reconnaissance in the attack lifecycle

- **Stage:** First phase in the **Cyber Kill Chain**.
- Often followed by **weaponization** and **delivery** stages.
- Can be repeated throughout an attack to adapt to defenses.

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
