# National Institute of Standards and Technology (NIST)

## Summary

NIST is a U.S. federal agency, part of the Department of Commerce, that develops measurement science, standards and technical guidance. In cybersecurity it is best known for the publications that much of the field uses as a common vocabulary: the Cybersecurity Framework, the Risk Management Framework, the SP 800-53 control catalog, the digital identity guidelines, the zero trust architecture and many others. NIST does not regulate or certify private organizations. Its documents become binding only when a law, a policy or a contract points to them, and that is the reason they are so widely used: they are free, openly reviewed and written to be reused.

Checked against nist.gov, csrc.nist.gov and the documents cited in each row, 2026-10.

## Prerequisites

- No technical prerequisite. For the documents themselves see [NIST frameworks and key publications](../governance-and-compliance/frameworks/nist-frameworks-overview.md).

## Core concepts

### Definition and mission

The National Institute of Standards and Technology was founded in 1901 and is part of the U.S. Department of Commerce. NIST describes itself as one of the nation's oldest physical science laboratories. Congress created the agency to remove a major challenge to U.S. industrial competitiveness at the time, a second-rate measurement infrastructure. It began as the National Bureau of Standards, and my understanding is that the Omnibus Trade and Competitiveness Act of 1988 renamed it NIST (from a NIST history page found through a web search, not read in full).

Most of NIST's work is outside cybersecurity (measurement, materials, time, manufacturing). Cybersecurity and privacy work sits mainly in the Information Technology Laboratory (ITL), one of NIST's six research laboratories, in the division that NIST has called the Computer Security Division and the Applied Cybersecurity Division in different publications.

### Analogy

Think of the national bureau that defines the official kilogram. Nobody is forced to buy goods weighed on its scale, but everyone who weighs things for trade uses the same definition, because it is accurate, public and free. NIST's security documents play the same role for practices: they define the reference vocabulary and methods.

The analogy breaks in one place. A kilogram is a physical fact. A security practice is a judgment about risk, so organizations reasonably choose and tailor NIST's recommendations, and different experts disagree about the right level of rigor.

### Position in government

- **Non-regulatory.** NIST has no enforcement or certification authority over private organizations. It publishes standards and guidelines.
- **Statutory role.** SP 800-53 states that NIST developed it under its responsibilities under the Federal Information Security Modernization Act (FISMA, Public Law 113-283), which charges NIST with developing information security standards and guidelines, including minimum requirements for federal information systems.
- **Binding for federal agencies, by decision of others.** The same text explains that standards and guidelines apply to federal agencies as made mandatory and binding by the Secretary of Commerce, and that they do not apply to national security systems without approval of the officials with policy authority over those systems. Policy from the Office of Management and Budget (OMB Circular A-130) is consistent with them.
- **Voluntary for everyone else.** NIST publications may be used by nongovernmental organizations on a voluntary basis and are not subject to copyright in the United States (SP 800-53 states this and asks for attribution).
- **Used outside the U.S.** The CSF 2.0 document notes that its taxonomy and referenced standards are not country-specific, and that earlier versions have been used by many governments and organizations inside and outside the United States.

### Cybersecurity programs and services

| Program | What it does | Source |
| --- | --- | --- |
| Standards and guidelines | The FIPS and SP series, and frameworks such as the CSF | Described below |
| National Cybersecurity Center of Excellence (NCCoE) | Founded in 2012 as a partnership of NIST, the State of Maryland and Montgomery County, builds example implementations with industry. Its output is the SP 1800 practice guide series | NIST pages via web search, SP 1800 name from the CSRC series list |
| National Initiative for Cybersecurity Education (NICE) | Publishes the NICE Framework, SP 800-181 Rev. 1, a common lexicon for cybersecurity work | SP 800-181 Rev. 1 |
| [National Vulnerability Database](../vulnerability-management/nvd.md) | Enriches [CVE](../vulnerability-management/cve.md) records with severity scores and metadata | See the NVD note |
| Cryptographic standards and validation | FIPS 140-3 for cryptographic modules, and the post-quantum standards FIPS 203, 204 and 205 released in August 2024 | SP 800-53A mentions FIPS 140-3 testing laboratories. The PQC release date is from secondary sources |
| Reference tools | The Cybersecurity and Privacy Reference Tool (CPRT) with mappings between CSF outcomes and other sources, and OSCAL machine-readable formats | SP 800-61 Rev. 3 and the OSCAL content repository |

### Publication series

The CSRC (Computer Security Resource Center) lists the cybersecurity series and describes them:

| Series | What it is | Examples |
| --- | --- | --- |
| FIPS (Federal Information Processing Standards) | Standards. Mandatory for federal agencies when approved as described above | FIPS 199 categorization, FIPS 200 minimum requirements |
| SP 800 | Guidelines focused on computer and information security | SP 800-53, SP 800-37, SP 800-61, SP 800-207 |
| SP 1800 | Practice guides, produced with NCCoE | Example implementations |
| IR (NIST interagency or internal reports) | Reports, including Community Profiles | IR 8374 Rev. 1 (ransomware profile, June 2026) |
| CSWP (cybersecurity white papers) | Papers, including the CSF | CSWP 29 (CSF 2.0) |
| AI series | Publications such as NIST AI 100-1 | AI RMF 1.0 |

A publication has a status. The CSRC publication pages show it, and the document itself carries notices:

- **Draft.** Posted for public comment. The documents themselves encourage organizations to review all drafts during comment periods and give feedback.
- **Final.** The current version. Revisions use "Rev. N", and minor corrections appear as updates, for example SP 800-53 Rev. 5 "includes updates as of 12-10-2020" and SP 800-161 Rev. 1 Update 1 (2024-11-01).
- **Release.** SP 800-53 uses releases within a revision (Release 5.2.0 on 2025-08-27) with a planning note on the page.
- **Withdrawn and superseded.** SP 800-61 Rev. 2 was withdrawn on 2025-04-03 and superseded by Rev. 3. The withdrawn PDF carries a warning notice and is kept for history.

The numbers after SP 800 do not indicate priority. They are sequential identifiers, and a given publication may be old and still correct, or old and replaced.

### How NIST documents are developed

From the evidence in the documents:

1. NIST posts a draft for public comment (the series pages list "drafts for public comment").
2. It reviews comments, and the final document records the approval date (for example, "Approved by the NIST Editorial Review Board on 2026-04-30" in IR 8374 Rev. 1).
3. Some content moves online so that it can be updated faster than the PDF: CSF 2.0 states that Informative References, Implementation Examples and Quick-Start Guides are hosted online for that reason.
4. Related documents are developed together, with mappings (for example SP 800-37 maps to CSF constructs, SP 800-61 Rev. 3 is a CSF Community Profile).

### Where to find things

| Need | Where |
| --- | --- |
| Final and draft cybersecurity publications | csrc.nist.gov/publications |
| Cybersecurity Framework resources | nist.gov/cyberframework |
| Mappings between frameworks and controls | Cybersecurity and Privacy Reference Tool (CPRT) |
| Machine-readable catalogs, baselines | github.com/usnistgov/oscal-content |
| Vulnerability data | nvd.nist.gov |
| Privacy Framework and AI RMF | nist.gov/privacy-framework and nist.gov/itl/ai-risk-management-framework |

## Worked example

The scenario: a policy document in your company still says "follow NIST SP 800-61 Rev. 2 for incident handling". You want to find out whether that reference is current. This uses public pages and a short script. Tested with Python 3.10.12, standard library only, with network access.

```python
# Prints the status lines that NIST puts on a CSRC publication page.
import html
import re
import sys
import urllib.request

url = sys.argv[1]
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (study script)"})
page = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
page = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", page)
text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", page)))
for key in ("Date Published:", "Supersedes:", "Planning Note", "Withdrawn"):
    i = text.find(key)
    if i != -1:
        print(text[i:i + 150].split("Author(s)")[0].split("Share to")[0].strip())
```

Run it for Rev. 2 and Rev. 3:

```bash
python3 nist_status.py https://csrc.nist.gov/pubs/sp/800/61/r2/final
python3 nist_status.py https://csrc.nist.gov/pubs/sp/800/61/r3/final
```

Output (page text as read on 2026-10, and it can change):

```text
Date Published: August 2012 Supersedes: SP 800-61 Rev. 1 (03/07/2008)
Supersedes: SP 800-61 Rev. 1 (03/07/2008)
Withdrawn on April 03, 2025 . Superseded by SP 800-61 Rev. 3 Computer Security Incident Handling Guide
Date Published: April 2025 Supersedes: SP 800-61 Rev. 2 (08/06/2012)
Supersedes: SP 800-61 Rev. 2 (08/06/2012)
```

How to read it:

1. Rev. 2 was published in August 2012, and its page says it was withdrawn on 2025-04-03 and superseded by Rev. 3. The reference in your policy is out of date.
2. Rev. 3 (April 2025) names Rev. 2 as the document it supersedes.
3. The next question is substantive, not bibliographic: Rev. 3 is organized as a CSF 2.0 Community Profile and drops the four-phase cycle. Update the policy text to say which model you use. The details are in [NIST incident response guidance](../defensive-operations/operations/nist-incident-response/README.md).
4. Do the same check for every NIST reference in a policy: SP 800-53 shows a planning note for Release 5.2.0, and SP 800-161 Rev. 1 was withdrawn on 2024-11-01 in favor of Update 1, according to the notice in the withdrawn PDF.

## Trade offs and when to use it

### Strengths of using NIST documents

- **Open and free.** No license fee, and in the United States they are not subject to copyright.
- **Peer-reviewed in public.** Drafts and comment periods reduce the risk of single-author blind spots.
- **Consistent family.** Documents refer to each other, so a program can scale from outcome view to controls.
- **Widely mapped.** Other standards and vendors publish mappings to NIST documents, which lowers translation costs.

### Limits

- **U.S. orientation.** Roles, laws and examples reflect U.S. federal context, and other jurisdictions have their own regulation and standards (for example ISO/IEC 27001 and national schemes).
- **Voluntary and generic.** A NIST document does not tell you what your regulator requires, and does not substitute for legal advice.
- **No certification.** There is no NIST certificate for the CSF or SP 800-53. Claims need to name the document, the version and the scope.
- **Version churn.** Documents are revised, withdrawn or superseded, and cross-references lag. Always check status.
- **Volume.** Reading everything is not practical. Start from the question.

### Alternatives and companions

| Need | Organization or standard |
| --- | --- |
| Internationally recognized management system | ISO/IEC, see [ISO/IEC 27001](../governance-and-compliance/standards/iso-iec-27001.md) |
| Security training and research | [SANS](sans.md) |
| Adversary behavior knowledge | MITRE, see [MITRE](../threat-intelligence/mitre/mitre.md) |
| Incident response and threat intelligence | [Mandiant](mandiant.md) |
| Prioritized safeguards | [CIS Controls](../governance-and-compliance/frameworks/cis-controls.md) |

## Further reading

- NIST, About NIST and history pages. The source for the founding year and mission: https://www.nist.gov/about-nist and https://www.nist.gov/history
- NIST CSRC, Publications. The series list, drafts open for comment, and status of every cybersecurity publication: https://csrc.nist.gov/publications
- NIST, The NIST Cybersecurity Framework (CSF) 2.0 (2024), for the use of the CSF outside the U.S. and the online resources: https://doi.org/10.6028/NIST.CSWP.29
- NIST, SP 800-53 Rev. 5 (2020), front matter. The statutory authority, and the statement on voluntary use and copyright: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- NIST, From NBS to NIST, on the 1988 renaming. Found through a web search and not read in full: https://www.nist.gov/coo/nist-100-foundations-progress/nbs-nist
