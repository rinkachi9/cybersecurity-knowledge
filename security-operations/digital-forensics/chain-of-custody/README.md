# Chain of custody

## Summary

Chain of custody is the documented record of who held a piece of evidence, when, where, why and what they did with it, from the moment it was found until it is no longer needed. Its job is to let a third party (a court, an auditor, a regulator, a disciplinary panel) trust that the evidence they are looking at is the same thing that was collected and that it was not altered on the way. In digital forensics the record is paired with cryptographic hashes, because digital data can be copied and changed without visible traces. A good chain of custody costs little at collection time and cannot be rebuilt afterwards.

## Prerequisites

- [CIA triad](../../../security-and-risk-management/foundations/cia-triad/README.md), especially integrity, and the hash chain example in it.
- [Hashing algorithms](../../../security-architecture-and-engineering/cryptography/hashing/hashing-algorithms.md) and [SHA](../../../security-architecture-and-engineering/cryptography/hashing/sha.md).
- The [NIST incident response lifecycle](../../defensive-operations/operations/nist-incident-response/README.md), because evidence handling happens inside incident response.

## Core concepts

### Definition

*Chain of custody* is the chronological documentation of the seizure, custody, control, transfer, analysis and disposition of evidence. RFC 3227 (*Guidelines for Evidence Collection and Archiving*, February 2002) says you should be able to describe "how the evidence was found, how it was handled and everything that happened to it". NIST SP 800-86 (August 2006) describes it as a log of every person who had physical custody of the evidence, the actions they performed and when, secure storage when the evidence is not in use, analysis only on a copy, and verification of the integrity of original and copy.

Three terms are easy to confuse:

| Term | Meaning | Who decides |
| --- | --- | --- |
| Chain of custody | The record of custody and handling. | The investigator keeps it. |
| Integrity verification | A technical check that data is unchanged, normally by comparing hashes. | A tool computes it, an analyst records it. |
| Admissibility | Whether a court accepts the evidence. | The court, under the law of its jurisdiction. |

A complete chain of custody does not make evidence admissible, and a gap does not automatically make it inadmissible. It affects how convincing the evidence is, and it removes an easy line of attack for the other side.

### Analogy

Think of a parcel with signed delivery slips. Every person who touches the parcel signs a slip with the time, and the seal on the parcel is checked at each handover. If you later receive the parcel, you can see the seal is intact and every handover is accounted for. The analogy breaks in one important way: a physical seal shows tampering, a digital file does not. That is why the hash of the data plays the role of the seal, and why the hash must be recorded at the first moment of collection and by someone other than the person who later holds the data.

### Why it exists

Digital evidence has three properties that make it fragile:

- It is easy to change by accident. Opening a file can change its access time. Booting a disk can write to it. Analysis tools can alter timestamps (RFC 3227 warns that analysis of a copy "will almost certainly alter file access times").
- It is easy to change on purpose, and the change can be perfect. An attacker or an insider with access to an image can edit it with no mark that survives inspection.
- It is often volatile. Memory, network connections and process state disappear on shutdown, and logs rotate out.

Without a record, the other side can claim that the evidence was mishandled or planted, and the investigator has no means to answer except their own word. The chain of custody replaces testimony about memory with a record created at the time.

### The elements of a good record

Combining RFC 3227 section 4.1 and NIST SP 800-86 section 3.1.2, a record answers the following for every item:

1. **Identification.** A unique ID for the item, a description, make, model and serial number, and where it was found. Photographs of the item and of the scene before it was touched. Screen content of a running machine is noted before anything else is done.
2. **Collection.** Who, when (with time zone) and where, and by what method and tool, including tool version.
3. **Integrity reference.** The hash of the data at acquisition, with the algorithm named. For a disk, the hash of the source and of the copy.
4. **Custody periods.** Who had custody, during which period, and how the item was stored.
5. **Transfers.** Each change of custody: from whom, to whom, when, how (including shipping numbers) and the condition of the seal on handover.
6. **Examination.** Who examined the item, when, where, what they did, and on which copy (not the original).
7. **Disposition.** Return, destruction or long-term retention, with the authority for the decision.

SP 800-86 adds a practical rule: designate one person at the scene as the *evidence custodian* with sole responsibility for photographing, documenting and labeling every collected item and recording every action with who, where and when. It also states that evidence should by default be preserved when it is unclear whether it is needed.

### Order of volatility

When evidence is collected, volatile data goes first. RFC 3227 gives this example order for a typical system:

```text
registers, cache
routing table, ARP cache, process table, kernel statistics, memory
temporary file systems
disk
remote logging and monitoring data relevant to the system
physical configuration, network topology
archival media
```

The same RFC lists practices that destroy evidence: shutting down before collection is complete (the attacker may have modified shutdown scripts), trusting programs on the compromised system (run trusted tools from protected media), and running programs that update the access time of all files. It also advises recording the clock drift of each system and, where feasible, checksumming and signing the collected evidence without altering it.

### Acquisition and integrity in practice

The technical side of the chain is a short sequence of steps (SP 800-86 section 3.1.2 names the process: identify sources, plan, acquire, verify integrity).

1. **Prevent writes.** Attach a disk through a hardware write blocker, or mount it read-only on a trusted forensic workstation. Software write blocking is possible but weaker as an argument, because the operating system must be configured correctly.
2. **Acquire a bit-for-bit image.** For a live host, capture memory first, then the disk. For a cloud instance, use a volume snapshot and export the audit logs to a separate account, as in the [cloud incident example](../../defensive-operations/operations/nist-incident-response/README.md).
3. **Hash source and copy** with the same algorithm and compare. SP 800-86 describes the check as computing the message digest of the original and the copy and comparing them. That 2006 text recommends SHA-1 over MD5 and plans a transition to stronger SHA by 2010. Use SHA-256 or stronger today (see [SHA](../../../security-architecture-and-engineering/cryptography/hashing/sha.md)). It is common practice to record two algorithms, which I did not verify against a standard.
4. **Work on a copy of the copy.** Keep the evidence copy sealed, because analysis alters timestamps.
5. **Seal and record.** Label the item, place it in a tamper-evident bag, write the seal number on the form, and store it in a locked location with access logging.

### A threat model for the chain itself

The chain of custody is a security control, so it has its own threats:

| Threat | Example | Control |
| --- | --- | --- |
| Alteration of evidence | Editing an image after collection | Hash at acquisition, copy for analysis, write blocker |
| Alteration of the record | Changing a transfer entry later | Append-only or hash-chained log, external anchor of the log head |
| Gaps in custody | Unknown holder for 6 hours | Every transfer needs sender and receiver entries that match |
| Weak identity | A shared analyst account | Individual accounts, signed entries |
| Time confusion | Logs with unsynchronized clocks | NTP, recorded clock drift, UTC timestamps |
| Unauthorized access | Evidence locker open to all staff | Access list, access log, tamper-evident seals |

The [CIA triad note](../../../security-and-risk-management/foundations/cia-triad/README.md) shows why a hash chain alone proves less than people think: whoever can rewrite the whole chain can recompute every hash. An external anchor (the head hash published in a ticket, an email to a third party or a timestamping service) is what makes rewriting detectable. A trusted timestamp from a time stamping authority (see [PKI](../../../security-architecture-and-engineering/cryptography/public-key-infrastructure.md)) can serve as such an anchor.

### Legal context

The law is jurisdiction specific, and this note is not legal advice. Decisions on evidence handling should follow policy agreed with legal counsel (SP 800-86 says the decision to preserve evidence for legal purposes is made by the analyst or management in accordance with the organization's policies and legal advisors).

For orientation, two provisions of the United States Federal Rules of Evidence (checked 2026-10 at law.cornell.edu) show how courts treat electronic evidence:

- Rule 902(13) lets a record generated by an electronic process or system be self-authenticating, with a certification by a qualified person.
- Rule 902(14) does the same for data copied from an electronic device, storage medium or file, if "authenticated by a process of digital identification" and certified.

In practice, "process of digital identification" is normally a hash value. This is the legal reason for the hash step above. The rules also require notice to the other party.

Other jurisdictions, and standards such as ISO/IEC 27037 (guidelines for the identification, collection, acquisition and preservation of digital evidence), set their own expectations. I did not read ISO/IEC 27037 for this note, because it is a paid standard.

TODO: verify the ISO/IEC 27037 process and terms (identification, collection, acquisition, preservation) against the standard or a summary from ISO.

### Where it appears in the CISSP outline

Section 7.1 lists "Evidence collection and handling", "Reporting and documentation", "Investigative techniques" and "Digital forensics tools, tactics, and procedures". Section 1.5 lists the investigation types (administrative, criminal, civil, regulatory, industry standards), which decide how strict the handling must be. Section 3.9 includes evidence storage as a facility. See [CISSP security domains](../../../security-and-risk-management/reference/certifications/cissp-security-domains.md).

## Worked example

A server `fs01` shows signs of ransomware staging. The responder, Alice, takes a disk image. She hands it to the analyst, Bob. The example script `scripts/custody-log.py` models the record as a hash chain of JSON entries and checks it for the failures from the threat table. It uses Python 3.10 and only the standard library. The data is synthetic: the evidence file is a generated byte string, and all names are placeholders.

The log has four entries: collect (with the image hash), transfer from Alice to Bob, hash verification by Bob and storage in a locker. Each entry's hash covers the previous hash plus the record, so editing or removing an entry breaks every later hash. The verifier also applies two process rules: a transfer must name the current holder as sender, and only the current holder may act on the item.

```bash
python3 scripts/custody-log.py
```

Output:

```text
1 untouched                : ok
2 edited receiver          : ['entry 1: hash chain broken (record edited, removed or reordered)', 'entry 2: bob acted on the item while mallory held it', 'entry 3: bob acted on the item while mallory held it']
3 missing transfer         : ['entry 1: hash chain broken (record edited, removed or reordered)', 'entry 1: bob acted on the item while alice held it', 'entry 2: bob acted on the item while alice held it']
4 chain rebuilt, no anchor : ['entry 2: bob acted on the item while mallory held it', 'entry 3: bob acted on the item while mallory held it']
4 chain rebuilt, anchor    : head differs from the anchor
5 evidence file changed    : ['evidence file hash does not match the hash recorded at collection']
```

How to read it:

- **Case 2** edits the receiver of the transfer. The hash chain breaks at the edited entry, and the process rule also fires, because later entries are by Bob while the record says Mallory holds the item.
- **Case 3** deletes the transfer. The chain is broken, and Bob appears to act on an item that Alice holds.
- **Case 4** is the important one. The forger recomputed all hashes, so the chain is internally consistent and no hash error is reported. The process rule still fires here, but only because the forger edited one field carelessly. A careful forger would edit the later entries too and pass every internal check. The only defense is the anchor: the head hash recorded earlier, outside the control of the log writer, no longer matches.
- **Case 5** changes the evidence file after collection. Only the comparison with the hash recorded at collection finds it, which is why that hash is the most important single value in the record.

Note that the script verifies consistency. It does not prove that the first entry was true: if Alice recorded a wrong hash at collection, every later check passes. Truth at the first step depends on process (a second person observing, photographs, a write blocker log), not on code.

## Trade offs and when to use it

**When to use full formal custody.** When there is a realistic chance of legal action, regulatory enquiry, an employment dispute or an insurance claim. SP 800-61 Rev. 2 notes that formal evidence handling is usually not needed for every incident (most malware incidents do not merit it). The cost is time: documenting every action slows containment.

**When lighter handling is enough.** Routine incidents resolved internally. Keep a timestamped log, hashes of exported artifacts and restricted access. If the decision is unclear, preserve by default, as SP 800-86 advises, because the decision to escalate often comes later.

**Costs and limits.**

- Effort at the worst moment. Evidence is collected while the team is also containing an incident. Preparation (forms, bags, tools, trained custodian) is what makes this affordable, which is why the NIST jump kit lists chain of custody forms.
- Containment conflicts with preservation. Isolating a host may destroy volatile data. Decide what to capture first, using the order of volatility, and write down the reasoning.
- Cloud and SaaS. There is no disk to seize. Custody means exported logs, snapshots and API responses, with the provider's retention limits and shared responsibility in mind. Terms and legal process vary by provider, which I did not verify here.
- Privacy. Evidence often contains personal data, so access limits and retention periods interact with [privacy regulations](../../../security-and-risk-management/privacy-regulations/README.md).
- Tooling quality is not proof. A forensic tool producing a hash is only convincing if the tool is validated and its version is recorded.

**Alternatives and complements.** Immutable log storage and write-once media reduce the need for trust in people. Automated collection by an EDR or a cloud IR pipeline records provenance as metadata. Neither replaces a human-readable record of decisions.

## Common mistakes

| Mistake | Why it hurts | Fix |
| --- | --- | --- |
| Hashing after the first analysis | There is no proof of the state at collection | Hash at acquisition, before anything else |
| Analyzing the only copy | Analysis changes timestamps | Make a working copy of the evidence copy |
| Shared accounts and shared evidence lockers | Custody cannot be attributed to a person | Individual identities and access logs |
| Missing time zone or unsynchronized clocks | Events cannot be ordered | UTC, NTP, record the drift |
| Recording opinions in the custody log | Mixes fact with conclusions | Keep the log factual, put analysis in reports |
| Using MD5 or SHA-1 alone | Both have known collision attacks | SHA-256 or stronger, optionally a second algorithm |
| Treating the hash chain as proof | Whoever controls the log can rebuild it | Anchor the head outside the writer's control |
| Rebuilding the server before capture | The evidence is gone | Capture first, then rebuild |

## Practice

1. List the seven elements of a custody record, and say which one the hash value belongs to.
2. A responder finds a running laptop with an encrypted disk. In which order would you collect, and what is lost if you pull the power cable first?
3. In the worked example, case 4 passes all hash checks. Which two additional measures would catch a careful forger?
4. Why is the hash value of the original recorded at collection more important than the hash recorded later?
5. A cloud account has an exposed access key. What replaces "seize the disk" in the chain of custody, and what must be preserved before the provider's logs rotate?
6. Extend `custody-log.py` so that each entry is signed by the person who acts. What does a signature add that the hash chain does not?

**Answers and hints**

1. Identification, collection, integrity reference, custody periods, transfers, examination, disposition. The hash is the integrity reference.
2. Memory and running state first, then disk. Pulling the power loses memory, and with it the disk encryption key, running processes and network connections. A full disk encryption key may exist only in memory.
3. An external anchor of the head hash, and signatures by each actor (or a trusted timestamp for each entry).
4. It is the only reference against which later copies are compared. A later hash only proves that the data has not changed since then.
5. Snapshots of affected resources, exported audit logs stored in a separate account with restricted access, and a record of the API calls used. Export before retention limits delete the logs.
6. A signature binds an entry to a key held by one person, so the writer of the log can no longer forge an entry for someone else. Without it, the log writer can attribute actions to anyone.

## Further reading

- IETF, RFC 3227, *Guidelines for Evidence Collection and Archiving* (Brezinski and Killalea, February 2002): order of volatility, collection steps and the elements of the chain of custody. Read in full for this note. https://www.rfc-editor.org/rfc/rfc3227
- NIST, SP 800-86, *Guide to Integrating Forensic Techniques into Incident Response* (August 2006): the four-phase forensic process, evidence handling and the role of the custodian. Status on the NIST page checked 2026-10: final, no superseding publication listed. Much of the tool detail is dated. https://csrc.nist.gov/pubs/sp/800/86/final
- NIST, SP 800-61 Rev. 3 (April 2025) and Rev. 2 (withdrawn): where evidence handling sits in incident response, see the [incident response note](../../defensive-operations/operations/nist-incident-response/README.md).
- Cornell Legal Information Institute, [Federal Rules of Evidence, Rule 902](https://www.law.cornell.edu/rules/fre/rule_902): self-authentication, including 902(13) and 902(14).
- ISO/IEC 27037:2012, Guidelines for identification, collection, acquisition and preservation of digital evidence. Not read.
