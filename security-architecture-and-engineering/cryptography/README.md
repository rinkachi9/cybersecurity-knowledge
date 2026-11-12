# Cryptography

Cryptographic building blocks and the infrastructure around them.

## Notes

Suggested reading order: fundamentals, Kerckhoffs's principle, symmetric and asymmetric encryption, then PKI, hashing and attacks. The Caesar cipher and Triple DES are worked case studies of a broken historical cipher and a retired modern one.

- [Cryptography fundamentals](cryptography-fundamentals.md): Vocabulary, security services, primitives, security strength, quantum impact and where cryptography fails.
- [Kerckhoffs's principle](kerckhoffs-principle.md): Security must rest on the key, not on secrecy of the design. The 1883 text and a broken homegrown cipher.
- [Public Key Infrastructure (PKI)](public-key-infrastructure.md): Roles, components, processes and best practices for issuing and managing digital certificates.
- [Cryptographic attacks](cryptographic-attacks/README.md): Attacks by attacker knowledge and by weakness place, with five tested toy demonstrations.

### Encryption

Symmetric and asymmetric algorithms.

Entry point: [encryption](encryption/README.md).

- [Symmetric and asymmetric encryption](encryption/symmetric-and-asymmetric-encryption.md): One shared key versus a key pair, modes, hybrid encryption and measured performance.
- [Triple DES (3DES)](encryption/triple-des.md): The EDE construction, keying options, Sweet32 and NIST retirement.

### Classical ciphers

Historical ciphers and how they are broken.

Entry point: [classical ciphers](classical-ciphers/README.md).

- [Caesar cipher](classical-ciphers/caesar-cipher/README.md): Shift substitution, brute force and chi-squared frequency analysis, with a tested script.

### Hashing

Hash functions and password hashing.

Entry point: [hashing](hashing/README.md).

- [Hashing algorithms](hashing/hashing-algorithms.md): What hashing is, its properties, how it differs from encryption and where it is used.
- [SHA](hashing/sha.md): The Secure Hash Algorithm family.
- [Bcrypt](hashing/bcrypt.md): The bcrypt password hashing algorithm.
- [Argon2](hashing/argon2.md): The Argon2 password hashing function.

## Planned topics

These topics are not written yet. They are listed so the scope of the area is visible.

- AES and modes of operation
- Key exchange and forward secrecy
- Digital signatures
- TLS
- Key management
- Common cryptographic misuse

Back to the [table of contents](../../ToC.md).
