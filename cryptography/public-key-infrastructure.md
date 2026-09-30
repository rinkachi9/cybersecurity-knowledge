---
title: Public Key Infrastructure (PKI)
area: cryptography
level: unrated
status: draft
last_verified: unverified
tags: [migrated, pki, certificates]
migrated_from: Security.html, page 3
---

# Public Key Infrastructure (PKI)

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

A public key infrastructure (PKI) is a set of roles, policies, hardware, software, and procedures to create, manage, distribute, use, store and revoke digital certificates and public-key encryption. The purpose of a PKI is to facilitate the secure electronic transfer of information for a range of network activities such as e-commerce, internet banking, and confidential email. It is required for activities where simple passwords are an inadequate authentication method, and the more rigorous proof is required to confirm the identity of the parties involved in the communication and to validate the information being transferred.

### Use cases

- Providing a recovery key for an encrypted hard drive
- Securing internal communications with database servers
- Signing documents
- Securing local networks: PKI capacities are built into Microsoft’s Active Directory, for instance, and can work with physical keycards that store digital certificates to ensure that users are who they say they are.
- Secure messaging: the Signal protocol uses PKI, for instance
- Email Encryption
- Securing access to internet of things (IoT) devices

### Advantages

- PKI is a standards-based technology.
- It allows the choice of trust provider.
- It is highly scalable. Users maintain their own certificates, and certificate authentication only involves the data exchange between the client and server. This means that no third-party authentication server needs to be online. There is, thus, no limit to the number of users who can be supported using PKI.
- PKI allows delegated trust. A user who has obtained a certificate from a recognized and trusted certificate authority can authenticate himself to a server the first time he connects to that server without having previously been registered with the system.
- Although PKI is not notably a single sign-on service, it can be implemented in such a way as to enable single sign-on.

### Challenges

- Complexity in implementation and management.
- Requires robust security for key storage and CA infrastructure.
- Revocation and renewal processes can be slow or inefficient.

## Components

- **Digital certificates:** digital “identities” issued by trusted third parties, that identify users and machines. They may be securely stored in wallets or in directories.
- **Public and private keys:** form the basis of a PKI for secure communications, based on a secret private key and a mathematically related public key
- **Secure sockets layer (SSL):** An Internet-standard secure protocol
- **Certificate Authority (CA):** acts as a trusted, independent provider of digital certificates
- **Registration Authority (RA):** Acts as a mediator between users and the CA, verifying the identity of certificate requesters.
- **Certificate Revocation List (CRL):** A list of revoked certificates no longer considered valid.

## Processes

### Key Pair Generation

- A pair of cryptographic keys (public and private) is created.
- Keys are unique to each user or system.

#### Certificate Request (CSR)

- A user or system generates a Certificate Signing Request (CSR) containing their public key and identity information.
- This CSR is sent to the RA or CA.

##### Certificate Issuance

- The CA verifies the identity through the RA.
- A digital certificate is issued, signed by the CA, binding the identity to the public key.

##### Certificate Distribution

- The issued certificate is made available to the requester and potentially published in a certificate repository.

##### Authentication and Encryption

- The public key from the certificate is used to encrypt or authenticate data.
- The private key, kept secret by the owner, is used for decryption or signing.

##### Certificate Revocation

- When a certificate is no longer valid (e.g., compromised, expired), the CA adds it to a CRL or revokes it via Online Certificate Status Protocol (OCSP).

##### Certificate Renewal

- Before expiration, the certificate is renewed through a new CSR.

## Example

### SSL/TLS in Web Security

1. **Website Certificate:**
   - A website (e.g., `example.com`) generates a CSR and submits it to a CA.
   - The CA verifies the domain ownership and issues an SSL certificate.
2. **Browser Validation:**
   - When a user accesses `https://example.com`, their browser checks the certificate against the CA's trusted root store.
   - The public key in the certificate is used to establish a secure encrypted session via the TLS handshake.
3. **Secure Communication:**
   - Data exchanged between the browser and the server is encrypted, ensuring confidentiality and integrity.

## Best practices

1. **Use Strong Cryptography:**
   - Use at least 2048-bit RSA keys or equivalent (e.g., ECC).
2. **Secure Key Storage:**
   - Store private keys in Hardware Security Modules (HSMs).
3. **Regularly Rotate Keys and Certificates:**
   - Periodically update keys and renew certificates.
4. **Implement Certificate Revocation:**
   - Use CRL or OCSP for real-time certificate validation.
5. **Enforce Policies:**
   - Define certificate policies, such as allowed usages and validity periods.
6. **Monitor for Expired Certificates:**
   - Use automation to track and renew certificates before expiration.
7. **Protect the CA:**
   - Use a multi-tier CA architecture (root CA, intermediate CA) to minimize risk.
8. **Educate Users:**
   - Train users on recognizing phishing and certificate errors.

## Ecosystem updates and trends

- **Advancements in Cryptography:** Quantum computing poses a potential threat to traditional cryptographic algorithms (e.g., RSA, ECC). Post-quantum cryptography (PQC) is an emerging area to address this.
- **Automation in Certificate Management:** Tools like Let's Encrypt and Certbot automate certificate issuance and renewal, making PKI more accessible and scalable.
- **Shortened Certificate Lifespans:** To enhance security, the industry is moving toward shorter certificate validity periods (e.g., one year or less) to reduce the impact of compromised keys.
- **Decentralized PKI (DPKI):** Blockchain-based PKI is gaining attention for its ability to eliminate centralized CAs, offering trustless systems.

## Common pitfalls

- **Failure to Monitor Certificates:** Expired certificates can disrupt services. Use monitoring and alerting tools to track certificate status.
- **Improper Key Management:** Exposing private keys leads to severe breaches. Use hardware-based solutions like HSMs or secure enclaves.
- **Misconfigured Certificate Authorities:** A compromised CA can lead to widespread trust issues. Always secure your CA with strict access controls and audits.
- **Over-Reliance on Single CA:** Avoid vendor lock-in by using multiple CAs or intermediate CAs to ensure flexibility.

## Regulatory and compliance

- PKI implementations often need to comply with legal and industry standards, such as:
  - **GDPR (General Data Protection Regulation):** Protects user data and requires encrypted communications.
  - **HIPAA (Health Insurance Portability and Accountability Act):** Ensures data security in healthcare.
  - **PCI-DSS (Payment Card Industry Data Security Standard):** Requires encryption for cardholder data.
- Regular audits are essential to demonstrate compliance with these standards.

## Applications beyond SSL/TLS

- **Email Security:** Protocols like S/MIME use PKI to encrypt and sign emails, ensuring authenticity and confidentiality.
- **Code Signing:** Developers use PKI to sign software, assuring users that the software is authentic and untampered.
- **VPNs and Wi-Fi Security:** PKI enables secure connections to VPNs and authenticates Wi-Fi devices using protocols like WPA2-Enterprise.
- **Document Signing:** Digital signatures based on PKI validate document integrity and authenticity (e.g., in PDFs).
- **IoT Security:** PKI secures communication between IoT devices, enabling authentication and data encryption.

## Practical considerations

- **Scalability:** For large organizations, consider Certificate Lifecycle Management (CLM) tools to handle thousands of certificates efficiently.
- **Redundancy:** Implement a backup CA or redundant infrastructure to ensure continuity in case of failure.
- **Root CA Security:** Keep the root CA offline and protected in a secure facility to prevent compromise.
- **OCSP Stapling:** Use OCSP stapling to improve certificate validation speed and reduce dependency on external revocation servers.
- **Integrations:** Ensure PKI integrates seamlessly with existing systems like Active Directory, LDAP, or custom applications.

## Real-World challenges and solutions

- **Challenge: Managing Certificate Sprawl**
  - **Solution:** Use centralized management platforms (e.g., HashiCorp Vault, AWS Certificate Manager) to track and manage certificates.
- **Challenge: Lack of Expertise**
  - **Solution:** Invest in training for IT staff or consider managed PKI solutions.
- **Challenge: Interoperability Issues**
  - **Solution:** Adhere to widely accepted standards like X.509 for certificates and ensure compatibility between systems.

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
