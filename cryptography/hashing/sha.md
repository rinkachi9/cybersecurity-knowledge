---
title: SHA
area: cryptography
level: unrated
status: draft
last_verified: unverified
tags: [migrated, hashing]
migrated_from: Security.html, page 106
---

# SHA

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

The Secure Hash Algorithm (SHA) family is a set of cryptographic hash functions widely used for security applications such as data integrity, digital signatures, and password hashing. Developed by the **National Institute of Standards and Technology (NIST)**, SHA has several versions, each tailored to specific security needs and performance considerations.

## SHA Family

| **Version** | **Bit Length** | **Year Introduced** | **Current Status** | **Use Cases** |
| --- | --- | --- | --- | --- |
| **SHA-0** | 160 bits | 1993 | Deprecated (design flaws) | Not used. |
| **SHA-1** | 160 bits | 1995 | Insecure (collision attacks) | Legacy systems; phased out for secure applications. |
| **SHA-2** | 224, 256, 384, 512 bits | 2001 | Secure (preferred) | SSL/TLS, blockchain, digital signatures. |
| **SHA-3** | 224, 256, 384, 512 bits | 2015 | Secure (quantum-resistant) | Post-quantum cryptography, blockchain, digital files. |

### SHA-0

**Introduced**: 1993.

**Key Features**:

- Produces a 160-bit hash value.
- Initial version of the SHA family.

**Why Deprecated**:

- Found to be insecure due to weaknesses in its design.
- Replaced by SHA-1 in 1995.

### SHA-1

**Introduced**: 1995.

**Key Features**:

- Produces a 160-bit hash value.
- Improved design over SHA-0 to address vulnerabilities.

**Vulnerabilities**:

- Susceptible to **collision attacks** (two different inputs producing the same hash).
- Not suitable for cryptographic security.

**Current Use**:

- Phased out in modern applications but may still be found in legacy systems.
- No longer recommended for SSL/TLS or digital signatures.

### SHA-2

SHA-2 is a family of cryptographic hash functions designed to address the vulnerabilities of SHA-1. It is the most widely used version today.

#### Variants

| **Variant** | **Bit Length** | **Output Size** | **Use Case** |
| --- | --- | --- | --- |
| **SHA-224** | 224 bits | 28 bytes | Lightweight applications. |
| **SHA-256** | 256 bits | 32 bytes | Blockchain, SSL/TLS, HMAC. |
| **SHA-384** | 384 bits | 48 bytes | High-security applications. |
| **SHA-512** | 512 bits | 64 bytes | High-security applications. |

##### How it works

1. **Preprocessing**:
   - Input data is padded to ensure its length is a multiple of 512 bits.
   - A single "1" bit is added, followed by "0" bits and a 64-bit representation of the original input length.
2. **Processing**:
   - Data is divided into 512-bit blocks (or 1024 bits for SHA-512).
   - Blocks are processed using multiple rounds of mathematical transformations, including bitwise operations, modular addition, and logical functions.
3. **Output**:
   - A fixed-length hash value is generated.

##### Use Cases

- **Blockchain**: Bitcoin uses SHA-256 for proof-of-work and transaction verification.
- **Digital Signatures**: Ensures document integrity and authenticity.
- **Password Hashing**: Often combined with salts for secure password storage.

##### Advantages

- Resistant to pre-image and second pre-image attacks.
- High performance and widely supported in software and hardware.

##### Disadvantages

- More resource-intensive than SHA-1.
- Not designed for post-quantum cryptography.

### SHA-3

SHA-3 is the latest addition to the SHA family, designed to complement SHA-2 with improved security and resistance to emerging threats like quantum computing.

#### Key features

- **Structure**: Based on the Keccak algorithm, which uses a unique sponge construction.
- **Bit Length**: Supports 224, 256, 384, and 512-bit outputs.
- **Quantum Resistance**: Resistant to theoretical quantum computing attacks.
- **Flexibility**: Can operate as both a hash function and a keyed message authentication code.

##### How it works

1. **Sponge Construction**:
   - Input data is absorbed into a fixed-size internal state.
   - The state is repeatedly permuted using a series of transformations.
   - The final hash is "squeezed" out from the state.
2. **Parallelism**:
   - Designed to leverage parallel computing for faster performance.

##### Use cases

- Post-quantum cryptographic systems.
- Applications requiring long-term security.
- Alternative to SHA-2 in systems requiring additional robustness.

##### Advantages

- Higher resistance to all known cryptographic attacks.
- Designed to future-proof applications against quantum computing.

##### Disadvantages

- Relatively new, with less widespread adoption than SHA-2.
- Slightly slower than SHA-2 in some cases.

## Comparison of SHA Variants

| **Feature** | **SHA-1** | **SHA-2** | **SHA-3** |
| --- | --- | --- | --- |
| **Security** | Vulnerable | Secure | Secure (quantum-resistant) |
| **Output Length** | 160 bits | 224, 256, 384, 512 bits | 224, 256, 384, 512 bits |
| **Structure** | Merkle - Damgård | Merkle - Damgård | Sponge (Keccak) |
| **Speed** | Fast | Moderate | Moderate |
| **Applications** | Legacy systems | Blockchain, SSL, password hashing | Post-quantum cryptography |
| **Adoption** | Deprecated | Widely adopted | Increasing adoption |

## Summary

SHA algorithms are foundational to modern cryptography, with SHA-2 being the most widely used for secure applications and SHA-3 representing the future of cryptographic hashing. Understanding their structure and use cases is crucial for implementing secure systems.

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
