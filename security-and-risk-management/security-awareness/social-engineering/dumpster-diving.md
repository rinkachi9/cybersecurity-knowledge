# Dumpster diving

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

**Dumpster diving** is a **physical reconnaissance technique** in which an attacker searches through trash or discarded items to find **confidential, sensitive, or valuable information**.

The “dumpster” may literally be a trash container, but it also includes **digital trash** such as deleted files on unsecured storage devices.

### Categorization

- **Vector-Based:** Physical retrieval of discarded materials.
- **Technique-Based:** Physical reconnaissance, information gathering.
- **Objective-Based:** Data theft, intelligence gathering for further attacks, identity theft, fraud.

## How it works

1. **Reconnaissance Targeting:**
   - Attacker identifies a location likely to discard sensitive materials (offices, data centers, homes of high-value targets).
2. **Collection:**
   - Physically retrieving discarded materials from trash bins, recycling containers, storage rooms, or e-waste disposal sites.
3. **Sorting and Analysis:**
   - Reviewing documents, media, or devices to extract valuable data (credentials, financial records, company secrets).
4. **Exploitation:**
   - Using recovered information to:
     - Conduct identity theft.
     - Craft phishing or pretexting campaigns.
     - Access systems or secure areas.

## Common targets

- **Paper Documents:** Meeting notes, printed emails, invoices, financial reports, access logs.
- **Digital Media:** USB drives, hard drives, CDs/DVDs.
- **Office Supplies:** ID badges, access cards.
- **Packaging:** Shipping labels containing customer info.
- **Prototypes or Hardware:** Old devices, development boards with embedded data.
- **Digital Trash:** Unwiped laptops or storage devices sold or discarded.

## Variants

| **Type** | **Description** | **Example** |
| --- | --- | --- |
| **Physical Dumpster Diving** | Searching physical trash/recycling for paper or devices. | Retrieving shredded but reconstructable documents. |
| **Digital Dumpster Diving** | Accessing “deleted” but recoverable files from storage media. | Recovering files from improperly formatted USB drives. |
| **E-Waste Exploitation** | Collecting disposed hardware for data extraction. | Buying old corporate laptops from surplus sales. |

## Psychological and human factors exploited

- **Negligence:** Failure to securely dispose of sensitive items.
- **Complacency:** Belief that discarded items are harmless.
- **Ignorance:** Lack of awareness of how much data is stored in everyday materials.

## Impact

- **Information Leakage:** Exposure of customer or employee data.
- **Credential Theft:** Recovery of usernames, passwords, or access cards.
- **Competitive Espionage:** Competitors gaining insights into strategies or projects.
- **Reputation Damage:** Public exposure of mishandled sensitive materials.
- **Regulatory Violations:** Breach of compliance (GDPR, HIPAA, PCI DSS).

## Detection and prevention

### Detection

- Surveillance cameras monitoring waste disposal areas.
- Security audits of disposal processes.

### Prevention

- **Technical:**
  - Shred paper documents (cross-cut shredders preferred).
  - Wipe or destroy storage devices before disposal (secure erase, degaussing, physical destruction).
- **Physical:**
  - Secure waste bins in locked areas until collection.
  - Supervise third-party disposal contractors.
- **Organizational:**
  - Implement data retention and destruction policies.
  - Train employees on secure disposal practices.

## Dumpster diving in modern threat landscape

- Increasingly tied to **supply chain attacks** - attackers retrieve discarded vendor materials.
- Relevant in **remote work** - home offices may produce sensitive waste.
- Digital dumpster diving is a growing concern with **cloud misconfigurations** and improper deletion in cloud storage.

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
