# Insecure legacy protocols

## Summary

A number of protocols still common on networks were designed before authentication and encryption were expected, so they send credentials and data in cleartext and trust whoever they talk to. Telnet, FTP, HTTP, SNMPv1/v2c, SMBv1, rsh/rlogin, TFTP and the cleartext mail protocols are the main examples. Each has a secure replacement, and the security task is twofold: find where the legacy protocol is still running (often on forgotten devices and management interfaces), and migrate to or enforce the secure alternative. Where a device genuinely cannot be upgraded, the compensating control is to isolate it and tunnel or proxy its access. Finding these protocols is also a standard part of network assessment, because they are reliable evidence of weak hygiene.

## Prerequisites

- [Protocol design weaknesses](../foundations/protocol-design-weaknesses.md): cleartext by default.
- [Network threat model](../foundations/network-threat-model.md): on-path interception.
- [Network scanning](../network-attacks/network-scanning.md): how these are discovered.

## Core concepts

### Definition

An *insecure legacy protocol* is one whose design lacks confidentiality, integrity or authentication appropriate to a hostile network, and which has a modern secure replacement. The problem is not age alone (DNS and SMTP are old and still used) but the absence of protection with no safe mode available.

### Analogy

These protocols are like sending postcards and house keys through the mail: anyone handling the mail reads the message and copies the key. The secure replacements are sealed, tamper-evident envelopes with a verified sender. The hard part is not agreeing that sealed envelopes are better; it is finding every department still mailing postcards, especially the ones nobody remembers setting up.

The analogy holds well; the main break is that a protocol can be "upgraded in place" (HTTP to HTTPS) in a way physical mail cannot, which is why enforcement (redirect, refuse the insecure mode) matters as much as migration.

### The main offenders and their replacements

| Legacy protocol | Port | Exposes | Secure replacement |
| --- | --- | --- | --- |
| Telnet | 23 | Credentials and session in cleartext | SSH (22) |
| FTP | 21 | Credentials and data in cleartext | SFTP (over SSH) or FTPS |
| HTTP | 80 | Session cookies, data | HTTPS ([TLS](../secure-transport/tls-in-network-security.md)) with HSTS |
| SNMPv1 / v2c | 161 | Community string (a shared password) in cleartext; read/write device config | SNMPv3 (authentication and encryption) |
| SMBv1 | 445 / 139 | Exploitable (EternalBlue), no modern integrity | SMBv2/3 with signing and encryption |
| rsh / rlogin / rexec | 514 / 513 | Trust-based remote execution, cleartext | SSH |
| TFTP | 69 (UDP) | No authentication, cleartext; used for device configs and boot | SCP/SFTP, or confine to an isolated provisioning VLAN |
| POP3 / IMAP / SMTP (no TLS) | 110 / 143 / 25 | Mail credentials and content | IMAPS/POP3S/SMTP with STARTTLS or implicit TLS; see [email transport security](email-transport-security.md) |
| LDAP (no TLS) | 389 | Directory bind credentials | LDAPS or STARTTLS |

### Why they persist

- **Embedded and operational devices.** Printers, cameras, PLCs, old switches and out-of-band management cards often speak Telnet, SNMPv1 and TFTP and may have no secure option. See [OT network security](../ot-and-iot/ot-network-security.md).
- **Management interfaces.** The riskiest instances are on management access, where cleartext credentials are the most valuable.
- **Inertia and undocumented use.** A script from years ago still uses FTP; nobody dares change it.

SNMP deserves special attention: v1 and v2c authenticate with a *community string*, a shared secret sent in cleartext, and a writable community string lets an attacker reconfigure the device. Default community strings (`public`, `private`) are a perennial finding.

### SMBv1

SMBv1 is both cleartext-era and actively dangerous: it was the vector for the WannaCry and NotPetya worms via the EternalBlue exploit. It has no legitimate use on modern networks and Microsoft recommends removing it outright. Its presence is a high-severity finding.

## Worked example

Discovery is the first step, and it uses the same techniques as [network scanning](../network-attacks/network-scanning.md). Conceptually, an authorized internal scan for legacy services looks for the ports above and inspects banners:

```text
# illustrative: which hosts expose cleartext management and file services
#   tcp/23  Telnet     -> replace with SSH
#   tcp/21  FTP        -> replace with SFTP
#   udp/161 SNMP v1/2c -> replace with SNMPv3, change default community strings
#   tcp/445 SMBv1      -> remove entirely
```

From a captured session, the exposure is obvious: the [packet capture note](../monitoring-and-detection/packet-capture-analysis/README.md) shows a cleartext HTTP request including headers directly readable on the wire. A Telnet or FTP login captured the same way reveals the username and password in plaintext. This is why an on-path position plus one legacy protocol equals credential compromise.

Remediation, in priority order:

1. Remove SMBv1 fleet-wide (highest severity, no legitimate use).
2. Replace Telnet with SSH and FTP with SFTP on all management and file access.
3. Move SNMP to v3, and change or remove default community strings immediately even before migrating.
4. Enforce HTTPS with HSTS; redirect and then refuse HTTP.
5. For devices that cannot be upgraded, isolate them in a restricted segment and reach them only through a jump host or protocol proxy, so the cleartext never crosses a shared or untrusted network.

## Trade offs and when to use it

- **Migrate vs isolate.** Migration is the real fix; isolation is the fallback for devices that cannot be upgraded. Isolation is a compensating control, not equivalent security, and should be documented as accepted risk.
- **Enforcement vs availability.** Refusing the insecure mode (disabling HTTP, SNMPv1) can break a forgotten dependency. Fix: discover usage first, migrate, then disable, with a rollback plan.
- **SNMPv3 complexity.** v3 adds user and key management that v2c lacks; the cost is justified for any device whose configuration or metrics matter.

## Common mistakes

- **Not knowing they are running.** The biggest problem is undiscovered instances. Fix: regular authorized scanning for these ports and banners.
- **Default SNMP community strings.** `public`/`private` grant read or write to anyone. Fix: change or disable immediately, migrate to v3.
- **Leaving SMBv1 enabled.** A wormable, cleartext-era protocol. Fix: remove it entirely.
- **Cleartext on management interfaces.** The worst place for cleartext credentials. Fix: SSH/HTTPS/SNMPv3 for all management.
- **Disabling without discovery.** Breaks forgotten dependencies. Fix: find usage, migrate, then enforce.

## Practice

1. Why is the age of a protocol not by itself what makes it a problem?
2. What does an SNMPv1/v2c community string expose, and what is the immediate fix before full migration?
3. Why is SMBv1 treated as more than just a cleartext-era protocol?
4. What is the compensating control for a device that cannot be upgraded off a legacy protocol?
5. Why are management interfaces the most important place to eliminate cleartext?

### Answers

1. Old protocols like DNS and SMTP remain in use safely; the problem is specifically the lack of confidentiality, integrity or authentication with no secure mode available, plus the existence of a modern replacement.
2. The community string is a shared secret sent in cleartext that grants read (v2c) or read/write access to the device; the immediate fix is to change or remove default strings, then migrate to SNMPv3.
3. SMBv1 is also actively exploitable (EternalBlue, used by WannaCry and NotPetya) and has no legitimate modern use, so it is a high-severity finding to remove, not just a cleartext concern.
4. Isolate it in a restricted segment and reach it only through a jump host or protocol proxy, keeping the cleartext off shared or untrusted networks, documented as accepted risk.
5. Management interfaces carry administrative credentials; intercepting those gives control of the device or network, so cleartext there is the highest-value target for an on-path attacker.

## Further reading

- Microsoft, Stop using SMB1 (guidance to remove SMBv1): https://techcommunity.microsoft.com/
- RFC 3411-3418, SNMPv3 (the User-based Security Model and View-based Access Control): https://www.rfc-editor.org/rfc/rfc3414
- NSA, Network Infrastructure Security Guide (2022), on disabling insecure management protocols: https://media.defense.gov/2022/Jun/15/2003018261/-1/-1/0/CTR_NSA_NETWORK_INFRASTRUCTURE_SECURITY_GUIDE_20220615.PDF
- CIS Benchmarks for the relevant platforms, which flag these protocols explicitly.
