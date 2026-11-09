# Email transport security

## Summary

Email was designed with no way to verify who sent a message or to keep it confidential in transit, which is why spoofing and interception are easy by default. A layered set of add-on standards fixes this at the transport and domain level: SPF says which servers may send mail for a domain, DKIM cryptographically signs messages so tampering and forgery are detectable, and DMARC ties the two together with a policy and reporting. MTA-STS and DANE then force encryption between mail servers so an on-path attacker cannot strip it. These controls are a network-security concern because they defend the transport of mail between servers and the authenticity of the sending domain; they do not secure message content end to end, which is a separate (S/MIME, PGP) problem.

## Prerequisites

- [DNS threat landscape](../dns-security/dns-threat-landscape.md): all of these publish records in DNS.
- [TLS in network security](../secure-transport/tls-in-network-security.md): MTA-STS and DANE enforce TLS.
- [Protocol design weaknesses](../foundations/protocol-design-weaknesses.md): unauthenticated sender, cleartext transport.

## Core concepts

### Definition

*Email transport security* is the set of DNS-published mechanisms that authenticate the sending domain and protect the server-to-server transport of mail. The core three are *SPF*, *DKIM* and *DMARC*; the transport-encryption enforcers are *MTA-STS* and *DANE*. They address domain spoofing and transport interception, not the confidentiality or authenticity of the message body for the end reader.

### Analogy

Sending email is like dropping a letter in the post with any name you like in the "from" line, carried between sorting offices on open trucks. SPF is a list, posted publicly by each company, of which trucks are allowed to carry its outgoing mail. DKIM is a tamper-evident wax seal the company presses on each letter, verifiable against a public sample. DMARC is the company's posted instruction: "if a letter claims to be from us but has no valid seal and did not come on an approved truck, reject it, and tell us". MTA-STS and DANE are a rule that letters between offices must travel in locked boxes, not open trucks.

The analogy breaks in that the seal (DKIM) covers the letter as sent by the server, not what the reader ultimately sees after forwarding, which is why these protect the domain and transport, not strictly the end-to-end message.

### SPF: authorizing senders

*Sender Policy Framework* (RFC 7208) is a DNS TXT record listing the IP addresses and hosts allowed to send mail for a domain. The receiving server checks whether the connecting server is listed. SPF authenticates the envelope sender (the `MAIL FROM`), and it breaks on forwarding (the forwarder is not in the original domain's SPF), which is part of why DKIM and DMARC are needed alongside it.

### DKIM: signing messages

*DomainKeys Identified Mail* (RFC 6376) adds a cryptographic signature over selected headers and the body, using a private key held by the sending domain; the public key is published in DNS. A receiver verifies the signature, which proves the message was authorized by the domain and was not altered in transit. Unlike SPF, DKIM survives simple forwarding because the signature travels with the message.

### DMARC: policy and alignment

*DMARC* (Domain-based Message Authentication, Reporting and Conformance) ties SPF and DKIM to the visible `From:` domain through *alignment*: it passes only if SPF or DKIM passes *and* the authenticated domain matches the `From:` domain the user sees. The domain owner publishes a policy, `p=none` (monitor only), `p=quarantine`, or `p=reject`, and receives aggregate and failure reports showing who is sending as their domain. The usual rollout is `none` to observe, then tighten to `reject`. The original DMARC was RFC 7489 (2015); the revised specification, known as DMARCbis, was published in 2026 as RFC 9989 (core) with RFC 9990 and RFC 9991 for reporting (checked 2026-10), clarifying alignment and deprecating the little-used `pct` tag and the `p=none`-via-subdomain patterns.

### MTA-STS and DANE: forcing transport encryption

SMTP between servers uses STARTTLS to upgrade to TLS, but STARTTLS can be *stripped* by an on-path attacker (remove the server's offer of TLS, and the mail falls back to cleartext). Two mechanisms close this:

- *MTA-STS* (RFC 8461): the domain publishes a policy (fetched over HTTPS, discovered via DNS) saying "my mail servers support TLS, require it". A compliant sender refuses to deliver in cleartext.
- *DANE for SMTP* (RFC 7672): the domain publishes a TLSA record in DNSSEC-signed DNS binding its mail server's certificate, so the sender both requires TLS and verifies the certificate without relying on the public CA system. DANE needs [DNSSEC](../dns-security/dnssec.md); MTA-STS relies on the web PKI and HTTPS instead.

### What this does not do

These protect the sending domain's authenticity and the server-to-server hop. They do not encrypt the message end to end (the mail provider can read it), and DMARC authenticates the domain, not the human. End-to-end confidentiality is S/MIME or PGP, a separate control.

## Worked example

Reading a domain's published records (illustrative values for `example.com`):

```text
# SPF: only these may send as example.com
example.com.          TXT  "v=spf1 ip4:203.0.113.0/24 include:_spf.provider.example -all"
# DKIM public key for selector "s1"
s1._domainkey.example.com. TXT "v=DKIM1; k=rsa; p=MIGfMA0GCSq..."
# DMARC: reject unaligned mail, send reports
_dmarc.example.com.   TXT  "v=DMARC1; p=reject; rua=mailto:dmarc@example.com; adkim=s; aspf=s"
# MTA-STS: require TLS to our mail servers
_mta-sts.example.com. TXT  "v=STSv1; id=20261008T000000Z"
```

Reading it: a receiving server that gets mail claiming to be from `example.com` checks that the sending IP is in SPF *and/or* that a DKIM signature verifies, that the passing domain aligns with the `From:` domain (`-all` and `adkim=s`/`aspf=s` enforce strict alignment), and if neither aligns, DMARC says reject. Aggregate reports go to the `rua` address so the owner sees spoofing attempts and misconfigured legitimate senders. MTA-STS tells other servers to deliver to `example.com` only over TLS, defeating STARTTLS stripping.

The `-all` (SPF hard fail) and `p=reject` are the enforcing end state; many domains sit too long at `p=none`, which detects spoofing but does not stop it.

## Trade offs and when to use it

- **DMARC `none` vs `reject`.** `none` is safe to deploy and gives visibility but stops nothing; `reject` is the goal but risks blocking legitimate mail from senders you did not account for (marketing platforms, forwarders). Roll out via reports.
- **SPF alone is insufficient.** It breaks on forwarding and only checks the envelope sender; pair it with DKIM and DMARC.
- **MTA-STS vs DANE.** MTA-STS is easier to deploy (no DNSSEC) but trusts the web PKI and has a trust-on-first-use window; DANE is stronger but requires DNSSEC, which many domains lack. Deploy MTA-STS broadly, DANE where DNSSEC exists.
- **These are anti-spoofing and anti-interception, not anti-spam by themselves**, though DMARC enforcement sharply reduces domain-spoofing phishing.

## Common mistakes

- **Stopping at `p=none`.** Detects but does not block spoofing. Fix: use reports to reach `p=quarantine` then `p=reject`.
- **SPF with `~all` (soft fail) left permanently.** Weak enforcement. Fix: move to `-all` once senders are accounted for.
- **DKIM keys too short or never rotated.** Fix: 2048-bit keys, periodic rotation via selectors.
- **Relying on STARTTLS without MTA-STS or DANE.** It can be stripped to cleartext. Fix: publish MTA-STS (and DANE with DNSSEC).
- **Assuming these encrypt the message for the recipient.** They secure transport and domain authenticity only. Fix: S/MIME or PGP for end-to-end confidentiality.

## Practice

1. What does SPF authenticate, and why does it break on forwarding?
2. How does DKIM differ from SPF in surviving forwarding?
3. What does DMARC alignment add on top of SPF and DKIM?
4. What attack do MTA-STS and DANE prevent that STARTTLS alone does not?
5. Why is `p=none` an incomplete deployment?

### Answers

1. SPF authenticates the envelope sender by checking whether the sending server's IP is authorized for the domain; it breaks on forwarding because the forwarding server is not in the original domain's SPF record.
2. DKIM's cryptographic signature travels with the message, so it still verifies after a simple forward, whereas SPF's check of the sending IP no longer matches.
3. Alignment requires that the domain authenticated by SPF or DKIM matches the visible `From:` domain, closing the gap where a message passes SPF/DKIM for one domain but displays another in `From:`.
4. STARTTLS stripping, where an on-path attacker removes the TLS offer so mail is sent in cleartext; MTA-STS and DANE make the sender require (and DANE verify) TLS.
5. It only monitors and reports spoofing; it does not instruct receivers to quarantine or reject unaligned mail, so spoofed messages are still delivered.

## Further reading

- RFC 7208 (SPF), RFC 6376 (DKIM): https://www.rfc-editor.org/rfc/rfc6376
- RFC 9989 (DMARCbis core, 2026) with RFC 9990 and RFC 9991 (reporting), superseding RFC 7489: https://www.rfc-editor.org/rfc/rfc9989
- RFC 8461 (MTA-STS) and RFC 7672 (DANE for SMTP): https://www.rfc-editor.org/rfc/rfc8461
- NIST SP 800-177 Rev. 1, Trustworthy Email: https://doi.org/10.6028/NIST.SP.800-177r1
