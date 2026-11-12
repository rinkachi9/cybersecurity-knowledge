# Encryption

Symmetric and asymmetric encryption algorithms, their modes, key sizes and retirement schedules.

Status: scaffold.

## Scope

- Belongs here: block and stream ciphers, modes of operation, authenticated encryption, public key encryption and key establishment, specific algorithms such as AES and Triple DES.
- Belongs elsewhere: hash functions and password hashing are in [hashing](../hashing/README.md), certificates and trust are in [public key infrastructure](../public-key-infrastructure.md), attacks on ciphers are in [cryptographic attacks](../cryptographic-attacks/README.md), and historical ciphers are in [classical ciphers](../classical-ciphers/README.md).

## CISSP sections

3.6 (select and determine cryptographic solutions) and 3.7 (understand methods of cryptanalytic attacks) of the ISC2 CISSP Exam Outline effective April 15, 2024.

## Notes

- [Symmetric and asymmetric encryption](symmetric-and-asymmetric-encryption.md): One shared key versus a key pair, modes, hybrid encryption and measured performance.
- [Triple DES (3DES)](triple-des.md): The EDE construction, keying options, Sweet32 and NIST retirement.

## To complete

- [ ] Introduction that explains how the encryption notes fit together.
- [ ] Reading order with one line per note.
- [ ] Planned topics (AES, modes of operation and AEAD, key exchange and forward secrecy, post-quantum key establishment).
- [ ] Sidecar relations to the TLS and PKI notes.

Back to [Cryptography](../README.md).
