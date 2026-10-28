# Asset management

## Summary

Security asset management is knowing what an organization owns or depends on, who is responsible for each item, how important it is and in what state it is, and keeping that knowledge current. It covers hardware, software, cloud resources, data, services from suppliers and the identities that act on them. Almost every other control assumes it: you cannot patch, harden, monitor, back up or retire what is not on a list. The practical difficulty is not making the first list. It is keeping several partial sources, such as the configuration management database, cloud APIs, scanners and endpoint agents, in agreement, so that unknown, ownerless and unmanaged assets show up as findings. This note covers the inventory model, ownership and classification, the lifecycle, the framework controls, a tested reconciliation script and the failure modes.

## Prerequisites

- [CIA triad](../../security-and-risk-management/foundations/cia-triad/README.md), which classification and criticality ratings derive from (FIPS 199 categorization is described there).
- [Security controls](../../security-and-risk-management/governance-and-compliance/frameworks/security-controls.md) and the [NIST Cybersecurity Framework](../../security-and-risk-management/governance-and-compliance/frameworks/nist-cybersecurity-framework.md).
- [Asset security domain overview](../README.md) for the scope of this area.

## Core concepts

### Definition

An *asset* is anything of value to the organization that needs protection. In the CISSP outline (section 2.3), the inventory covers tangible and intangible assets, with ownership and asset management as the related activities (outline effective April 15, 2024). *Asset management* in security terms is the set of practices that identify assets, assign ownership and criticality, maintain the inventory through the lifecycle and make that information available to other controls.

NIST SP 1800-5 (*IT Asset Management*, September 2018) makes the point with an example: a physical asset record cannot answer "What operating systems are our laptops running?", and IT asset management ties physical and virtual assets together so analysts get a fuller picture, which improves visibility and security (abstract, checked 2026-10).

Terms used in this note:

| Term | Meaning |
| --- | --- |
| Asset inventory | The list of assets with attributes (type, owner, location, criticality, software, state) |
| CMDB | Configuration management database, a common system of record for IT assets and their relationships |
| Owner | The person accountable for the asset and its risk decisions |
| Custodian | The person or team that operates the asset on the owner's behalf |
| Shadow asset | An asset that exists on the network or in a cloud account but is not in the inventory |
| Ghost record | An inventory entry for an asset that no longer exists or is no longer seen |
| Criticality | The impact on the mission if the asset is lost, compromised or unavailable |

### Analogy

A warehouse stock list. A stock list is only useful if it matches the shelves: items that are on shelves but not on the list are shadow stock, items on the list but not on shelves are ghosts, and items with no responsible person are the ones that go missing. The analogy breaks in two ways: servers can appear and disappear within minutes in the cloud, so the list is never "finished", and some assets are intangible (data, a SaaS tenant, a domain name) and do not sit on any shelf.

### Why it matters

1. **Coverage depends on it.** Vulnerability scans, configuration audits, backups, EDR and logging can only cover known assets. A scanner coverage of 100% of the inventory says nothing when the inventory is incomplete.
2. **Attackers find what you forgot.** Forgotten internet-facing servers, test environments and old VPN profiles are common entry points, see [attack vectors](../../security-operations/threats-and-attacks/attack-vectors/README.md) and [CASM](../../security-operations/attack-surface-management/cloud-attack-surface-management/README.md).
3. **Prioritization depends on context.** Criticality and exposure decide the order of fixes, see [vulnerability remediation](../../security-operations/vulnerability-management/vulnerability-remediation/README.md).
4. **Response needs it.** During an incident the first question is "what is this host, who owns it and what does it touch?"
5. **Lifecycle control.** End-of-life software and unsupported hardware carry unpatched risk, which is why CISSP section 2.5 covers retention to end of life and end of support.

### What goes in the inventory

| Class | Examples | Minimum attributes |
| --- | --- | --- |
| Hardware | Servers, laptops, network devices, IoT and OT | ID, type, owner, location, criticality, firmware or OS version |
| Software | Operating systems, applications, libraries | Name, version, vendor, support status, license |
| Cloud resources | Accounts, subscriptions, virtual machines, buckets, functions, clusters | Provider ID, account, region, owner tag, environment |
| Services from suppliers | SaaS, managed services, APIs | Supplier, data processed, contract owner, integration points |
| Data | Datasets and stores with classification | Owner, classification, location, retention, legal requirements |
| Identities | Human, service and machine accounts | Owner, privilege level, last use |
| Network | Domains, IP ranges, certificates | Registrant, owner, expiry |

The NIST CSF 2.0 category Asset Management (ID.AM) covers the same ground. Its outcomes, from the Profile worksheet kept in this repository: inventories of hardware (ID.AM-01), of software, services and systems (ID.AM-02), representations of authorized network communication and data flows (ID.AM-03), inventories of supplier services (ID.AM-04), prioritization by classification, criticality, resources and mission impact (ID.AM-05), inventories of data and metadata for designated data types (ID.AM-07) and life cycle management of systems, hardware, software, services and data (ID.AM-08). The worksheet has no ID.AM-06; I did not check why the numbering skips it.

Other frameworks: CIS Controls Control 1 is inventory and control of enterprise assets, covering end-user devices, network devices, IoT devices and servers, connected physically, virtually, remotely or through the cloud, with the goal of knowing all assets that need monitoring and protection and identifying unauthorized and unmanaged ones (CIS page, checked 2026-10; the safeguard list was not on the page I read). SP 800-53 CM-8 is System Component Inventory (in the low, moderate and high baselines). ISO/IEC 27001:2022 has an Annex A control for the inventory of information and other associated assets, which I know from memory and did not verify. See [CIS Controls](../../security-and-risk-management/governance-and-compliance/frameworks/cis-controls.md) and [ISO/IEC 27001](../../security-and-risk-management/governance-and-compliance/standards/iso-iec-27001.md).

### Ownership and classification

Every asset needs an *owner* with the authority to make risk decisions and a *custodian* that runs it. Without an owner, no one approves an exception, no one is called when a finding appears, and the asset lives on after it is needed. Owners also assign the classification of information assets (for example public, internal, confidential, restricted) and the criticality rating that other processes use. The CIA-based categorization of FIPS 199 is one way to derive criticality: rate the impact of loss of confidentiality, integrity and availability, and take the highest value per property, as described in the [CIA triad note](../../security-and-risk-management/foundations/cia-triad/README.md).

### Discovery and the reconciliation problem

No single source is complete.

| Source | Strength | Blind spot |
| --- | --- | --- |
| CMDB or procurement records | Owner, purpose, business context | Stale, misses shadow assets |
| Cloud provider APIs | Authoritative for cloud resources | Only the accounts you know about |
| Network scanning and passive monitoring | Sees what is actually reachable | Misses powered-off, segmented or roaming assets |
| Endpoint agents (EDR, management) | Software and state detail | Only where installed |
| DHCP, DNS and authentication logs | Evidence of use | Indirect |
| Vulnerability scanner | Finds assets as a side effect | Depends on scan scope |
| Identity provider and SaaS admin APIs | Users, apps, OAuth grants | Per-vendor |

The approach: pull from all of them, normalize identifiers (hostname, IP, MAC, cloud ID, serial), merge into one view and treat the differences as findings. A source that sees an asset the system of record does not know is the best signal for shadow assets.

### Lifecycle

```mermaid
flowchart LR
  A[Request and approve] --> B[Procure or provision]
  B --> C[Register: ID, owner, criticality]
  C --> D[Operate: patch, configure, monitor]
  D --> E[Change: move, upgrade, new owner]
  E --> D
  D --> F[End of life or end of support]
  F --> G[Retire: data removal, access revocation]
  G --> H[Dispose and update the record]
```

Registration at provisioning (C) is the most effective control, because automation in infrastructure as code can create the record with the resource. Retirement (G) is where data remanence matters: media and cloud volumes must be sanitized or destroyed, see CISSP section 2.4. For end-of-life tracking, record the vendor's end of support date as an attribute and report on assets that pass it.

## Worked example

The script `scripts/reconcile-inventory.py` merges five synthetic sources and prints the standard findings. All names use the reserved `example.com` domain. Python 3.10, standard library only. The output is real.

```bash
python3 scripts/reconcile-inventory.py
```

Output:

```text
sources: cmdb 4 | cloud 3 | scanner 5 | edr 2
shadow assets (discovered, not in CMDB): ['ci-runner-9.example.com', 'print-3.example.com']
ghost records (in CMDB, not seen for 30+ days or by any source): ['old-ftp.example.com']
assets without owner: ['old-ftp.example.com']
critical or medium assets without EDR: ['db-01.example.com']
end-of-life software: [('old-ftp.example.com', 'CentOS 7')]
scanner coverage of CMDB assets: 75%; of all discovered assets: 100%
```

What each line means:

1. **Shadow assets.** `ci-runner-9` appears in the cloud API and the scanner but not in the CMDB. A CI runner is a high-value target (it holds build credentials, see [supply-chain attacks](../../software-development-security/application-security/supply-chain/supply-chain-attacks/README.md)), so this is the most serious finding. `print-3` is a printer found only by the scanner.
2. **Ghost record and ownerless asset.** `old-ftp` has not been seen since June, has no owner and runs CentOS 7. It appears in three findings at once, which is typical: an unowned, unseen legacy system. It should be confirmed and retired.
3. **EDR gap.** `db-01` is a high-criticality database that no endpoint agent covers. It is a coverage hole that only an inventory joined with EDR data reveals.
4. **End of life.** The script uses 2024-06-30 as the CentOS 7 end of maintenance date. Real programs read this from a vendor lifecycle feed.
5. **Coverage.** The scanner covers 75% of CMDB assets (it misses `old-ftp`) and 100% of discovered assets. Both numbers are true, which shows why the denominator matters: coverage of the CMDB flatters, coverage of everything discovered is the honest one, and neither counts assets that no source sees.

The script does not fix anything. Each finding needs an owner, a decision and a due date, tracked as work.

## Trade offs and when to use it

**What to automate.** Registration at provisioning, discovery from cloud APIs, daily reconciliation and alerts on shadow assets and ownerless assets. Manual inventories decay within weeks in a dynamic environment.

**Costs and limits.**

- Normalization of identifiers across sources is the hard part. Hostnames change, IPs are reused, containers live for minutes.
- Ephemeral assets (containers, serverless) fit better in a service-level inventory (image, workload, namespace) than in a host list.
- Data and SaaS assets need other discovery methods, see [DSPM](../data-protection/data-security-posture-management/README.md).
- Ownership data goes stale after reorganizations. Review it on a schedule.
- Tools that claim "complete" discovery still miss assets outside their reach.

**Alternatives.** Cloud provider asset services and CNAPP platforms provide inventory for cloud resources, see [CSPM](../../security-architecture-and-engineering/cloud-and-infrastructure-security/cloud-security-posture-management.md). External attack surface management finds what is reachable from the internet, see [CASM](../../security-operations/attack-surface-management/cloud-attack-surface-management/README.md). Use both with the internal inventory.

## Common mistakes

| Mistake | Effect | Fix |
| --- | --- | --- |
| One source of truth with no cross-check | Shadow assets stay hidden | Reconcile several sources daily |
| Inventory without owners | Findings go unattended | Make the owner a required field |
| One-time inventory project | Decays | Automate registration and discovery |
| Counting only servers | Misses SaaS, cloud accounts, identities, data | Define the asset classes |
| Reporting coverage against the CMDB only | False confidence | Report against discovered assets too |
| No lifecycle end date | End-of-life systems stay in production | Record end of support, report on it |
| Ignoring retirement | Data and access remain after decommission | Retirement checklist with sanitization and access revocation |
| Treating all assets as equal | Poor prioritization | Criticality rating per asset |

Detection and mitigation: alert on new unmanaged devices, on cloud resources created without owner tags, on certificates and domains not in the inventory, and on assets that stop reporting. Mitigation is the combination of registration at creation and daily reconciliation.

## Practice

1. Which NIST CSF 2.0 outcome corresponds to "inventories of services provided by suppliers are maintained"?
2. Define shadow asset and ghost record, and say which one is more dangerous and why.
3. In the worked example, `old-ftp` appears in three outputs. What single decision removes the risk, and what must happen to its data?
4. Why is "scanner coverage of all discovered assets: 100%" not a proof of good coverage?
5. Add a rule to the script that flags assets whose owner field names a team that does not exist in a list of valid teams.
6. Which CISSP sections does asset management touch?

**Answers and hints**

1. ID.AM-04.
2. A shadow asset exists but is not in the inventory. A ghost record is in the inventory but no longer exists or is no longer seen. Shadow assets are more dangerous because they are unmanaged and invisible to every control.
3. Confirm its status and retire it. Its data must be reviewed for retention requirements, archived or sanitized according to policy, and access and DNS entries removed.
4. Assets that no source sees are not counted. The denominator is only what was discovered.
5. Add a set `VALID_TEAMS` and print the names where `a["owner"] not in VALID_TEAMS`.
6. 2.1 to 2.5 (classification, handling, provisioning and inventory, data lifecycle, retention), 3.10 (system lifecycle) and 7.3 (configuration management). See [CISSP security domains](../../security-and-risk-management/reference/certifications/cissp-security-domains.md).

## Further reading

- NIST, [SP 1800-5, IT Asset Management](https://csrc.nist.gov/pubs/sp/1800/5/final) (September 2018): the practice guide on IT asset management. Only the abstract and status were read.
- NIST, [CSF 2.0](https://doi.org/10.6028/NIST.CSWP.29), category ID.AM, see the [CSF note](../../security-and-risk-management/governance-and-compliance/frameworks/nist-cybersecurity-framework.md) and the Profile worksheet in `_assets`.
- CIS, [Control 1: Inventory and Control of Enterprise Assets](https://www.cisecurity.org/controls/inventory-and-control-of-enterprise-assets) and Control 2 for software. The safeguards were not available on the page I read.
- ISC2, *CISSP Certification Exam Outline*, effective April 15, 2024, Domain 2 ([PDF](https://edge.sitecorecloud.io/internationf173-xmc4e73-prodbc0f-9660/media/Project/ISC2/Main/Media/documents/exam-outlines/CISSP-Exam-Outline-April-2024-English.pdf)).
- NIST SP 800-53 Rev. 5, control CM-8 (System Component Inventory): see the [SP 800-53 note](../../security-and-risk-management/governance-and-compliance/frameworks/nist-sp-800-53/README.md).
