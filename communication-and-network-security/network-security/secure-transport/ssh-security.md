# SSH security

## Summary

SSH (Secure Shell) is the standard protocol for secure remote administration, file transfer and tunneling. It replaced the cleartext Telnet, rlogin and FTP, giving an encrypted, authenticated channel to a server's command line and to automated workflows. Because SSH grants administrative access, it is a high-value target: exposed SSH servers are constantly scanned and brute-forced, stolen or sprawling SSH keys are a common path for lateral movement, and SSH's own tunneling can be used to exfiltrate data or bypass controls. Securing SSH means strong key-based authentication, hardened server configuration, disciplined key management, and controlling where SSH may reach. Modern OpenSSH also adds post-quantum key exchange by default.

## Prerequisites

- [Network threat model](../foundations/network-threat-model.md) and [authentication methods](../../../identity-and-access-management/identity-and-access/authentication/authentication-methods.md).
- [Insecure legacy protocols](../core-protocols/insecure-legacy-protocols.md): what SSH replaced.
- Basic public-key cryptography.

## Core concepts

### Definition

*SSH* (RFC 4251 and related) is a protocol providing an encrypted, integrity-protected channel with server authentication and flexible client authentication, used for remote shell access, file transfer (SCP, SFTP), and port forwarding (tunneling). The dominant implementation is OpenSSH.

### Analogy

SSH is a secure, verified phone line into a building's control room. The caller first confirms they really reached the right control room (host key verification), then proves who they are, ideally with a physical key rather than a spoken password (public-key authentication). The line is scrambled so nobody can listen. The risks mirror a control room: thieves constantly try the door (brute force), spare keys left lying around open it (key sprawl), and the line can be used to smuggle things in or out (tunneling).

The analogy holds well; the main break is that SSH keys are files that can be copied silently and used from anywhere, so a leaked key is like a master key that was photocopied without anyone noticing.

### Authentication: keys over passwords

SSH supports several authentication methods; the security difference is large:

- *Password authentication* is exposed to brute force and [password spraying](../../../identity-and-access-management/credential-attacks/password-spray.md). On an internet-facing server it is attacked continuously. Disable it where possible.
- *Public-key authentication* uses a key pair: the public key is placed in the server's `authorized_keys`, the private key stays with the client. It resists brute force and is the default for secure deployments. The private key should itself be protected by a passphrase and, better, held in hardware (a security key or agent).
- *Certificate-based SSH* (OpenSSH certificates) has a trusted CA sign short-lived user and host certificates, so servers trust the CA rather than a sprawling list of individual keys, and access expires automatically. This is the scalable answer to key sprawl.
- *Host keys* authenticate the server to the client; the first-connection "trust on first use" prompt is a weak point, solved at scale by distributing known host keys or using host certificates.

### Key management: the real problem at scale

Individual SSH key pairs accumulate: developers generate keys, copy public keys onto many servers, and rarely remove them. The result is *key sprawl*, thousands of keys granting access with no central record of who holds the matching private key or whether it should still work. This is a leading cause of unnoticed standing access and lateral movement. Remedies:

- Prefer **SSH certificates** with short lifetimes over static `authorized_keys`.
- Inventory and rotate keys; remove orphaned keys.
- Protect private keys with passphrases and hardware; use an agent with confirmation.
- Restrict what a key can do (`authorized_keys` options: `command=`, `no-port-forwarding`, source `from=` restriction).

### Server hardening

Core OpenSSH hardening (`sshd_config`):

- `PasswordAuthentication no`, `PubkeyAuthentication yes`: keys only.
- `PermitRootLogin no` (or `prohibit-password`): no direct root password login.
- `AllowUsers` / `AllowGroups`: restrict who may log in.
- Limit exposure: bind to management networks, front with a [bastion/jump host](../architecture/management-plane-security.md), and apply rate limiting or fail2ban against brute force.
- Disable unused features: `AllowTcpForwarding no` where tunneling is not needed; restrict `X11Forwarding`.
- Keep OpenSSH current: modern versions disable weak ciphers and legacy key exchange by default.

### Tunneling: feature and risk

SSH port forwarding tunnels arbitrary TCP (and with dynamic forwarding, a SOCKS proxy) through the SSH connection. It is useful for administrators but is also a way to exfiltrate data or pivot past network controls, since it hides inside an allowed SSH session (MITRE ATT&CK Protocol Tunneling, T1572). Where tunneling is not needed, disable it; where it is, log and monitor SSH and restrict forwarding per key.

### Post-quantum key exchange

OpenSSH 10.0 (released April 2025) makes the hybrid post-quantum algorithm `mlkem768x25519-sha256` the default key exchange, protecting SSH session keys against harvest-now-decrypt-later attacks, and disables finite-field Diffie-Hellman by default (checked 2026-10). On this reference host (OpenSSH 8.9) the hybrid `sntrup761x25519-sha512@openssh.com` is already available, showing the migration was underway before it became default.

## Worked example

Checking the key-exchange algorithms a client supports, on the reference host (OpenSSH 8.9, 2026-10):

```bash
ssh -Q kex | grep -iE "mlkem|sntrup|curve25519"
```

Output:

```text
curve25519-sha256
curve25519-sha256@libssh.org
sntrup761x25519-sha512@openssh.com
```

Reading it: the classical modern exchange `curve25519-sha256` is present, and so is the hybrid post-quantum `sntrup761x25519-sha512@openssh.com`, which combines a post-quantum KEM with Curve25519. A server and client that both prefer the hybrid negotiate quantum-resistant session keys; OpenSSH 10.0 makes an ML-KEM-based hybrid the default so this happens without configuration. A hardened `sshd_config` for an internet-reachable jump host would then add: keys-only authentication, no root login, a restricted user list, and no TCP forwarding unless required, with the host itself reached only through a bastion where possible.

## Trade offs and when to use it

- **Keys vs certificates.** Static keys are simple but sprawl and never expire; SSH certificates add a CA and short lifetimes, solving sprawl at the cost of running the CA. Prefer certificates at scale.
- **Convenience vs restriction.** Agent forwarding and tunneling are convenient but expand risk (a forwarded agent can be abused on a compromised host). Enable only where needed, with confirmation and restrictions.
- **Direct access vs bastion.** A bastion/jump host centralizes logging and reduces exposed SSH surface, at the cost of an extra hop.
- **Fail2ban/rate limiting vs disabling passwords.** Disabling password auth is the stronger control; rate limiting helps where some password use remains.

## Common mistakes

- **Password authentication on internet-facing SSH.** Continuously brute-forced. Fix: disable passwords, use keys or certificates, front with a bastion.
- **Key sprawl with no inventory or expiry.** Standing access nobody tracks. Fix: SSH certificates, key inventory and rotation, remove orphaned keys.
- **Unprotected private keys.** A copied key is silent full access. Fix: passphrases, hardware-backed keys, agents with confirmation.
- **Direct root login and no user restriction.** Fix: `PermitRootLogin no`, `AllowUsers`/`AllowGroups`.
- **Leaving TCP forwarding enabled by default.** Enables pivoting and exfiltration. Fix: disable where unneeded; log and monitor SSH; restrict per key.

## Practice

1. Why is public-key authentication preferred over passwords for SSH?
2. What is SSH key sprawl, and how do SSH certificates address it?
3. What does the host key authenticate, and what is the weakness of trust-on-first-use?
4. How can SSH tunneling be abused, and what is the mitigation where tunneling is not needed?
5. What does OpenSSH 10.0's default key exchange protect against?

### Answers

1. It resists brute force and password spraying (there is no guessable secret sent), and the private key can be hardware-protected, whereas passwords are continuously attacked on exposed servers.
2. The uncontrolled accumulation of individual key pairs across many servers with no record of who holds the private keys; SSH certificates have a trusted CA issue short-lived certificates, so servers trust the CA instead of a growing `authorized_keys` list and access expires automatically.
3. The host key authenticates the server to the client; trust-on-first-use means the first connection accepts whatever key is presented, so an attacker intercepting that first connection can insert their own host key.
4. It can tunnel arbitrary TCP to exfiltrate data or pivot past network controls inside an allowed SSH session; where not needed, disable `AllowTcpForwarding` and monitor SSH usage.
5. Harvest-now-decrypt-later attacks on the session keys, by using a hybrid post-quantum key exchange (`mlkem768x25519-sha256`) resistant to future quantum computers.

## Further reading

- RFC 4251-4254, the SSH protocol architecture and components: https://www.rfc-editor.org/rfc/rfc4251
- OpenSSH release notes, especially 10.0 (post-quantum default): https://www.openssh.com/releasenotes.html
- NIST SP 800-57 and the OpenSSH `sshd_config` manual for hardening guidance.
- NIST IR 7966, Security of Interactive and Automated Access Management Using Secure Shell (SSH), on key management: https://doi.org/10.6028/NIST.IR.7966
