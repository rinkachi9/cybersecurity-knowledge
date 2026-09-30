---
title: Argon2
area: cryptography
level: unrated
status: draft
last_verified: unverified
tags: [migrated, hashing, passwords]
migrated_from: Security.html, page 107
---

# Argon2

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

Argon2 is a cutting-edge cryptographic hash function designed specifically for secure password hashing. It was the **winner of the Password Hashing Competition (PHC)** in 2015 and is recognized for its high security, flexibility, and resistance to various attacks.

### Overview

| **Feature** | **Description** |
| --- | --- |
| **Type** | Password hashing algorithm |
| **Released** | 2015 (Winner of PHC) |
| **Key Strengths** | Resistant to GPU/ASIC attacks, customizable memory and time cost, salting. |
| **Applications** | Password storage, key derivation, cryptographic applications. |

### Variants

Argon2 comes in three variants, each optimized for specific use cases:

| **Variant** | **Purpose** | **Key Features** |
| --- | --- | --- |
| **Argon2i** | Ideal for password hashing and key derivation. | Resistant to side-channel attacks. Uses data-independent memory access. |
| **Argon2d** | Suitable for applications requiring high performance (non-password use cases). | Uses data-dependent memory access, faster but less secure. |
| **Argon2id** | Combines features of Argon2i and Argon2d; recommended for password hashing. | Offers a balance between security and performance. |

## How it works

Argon2 is based on three main configurable parameters: **memory cost**, **time cost**, and **parallelism**. These parameters allow fine-tuning for specific requirements, such as security level or resource constraints.

1. **Preprocessing**:
   - Input includes the password, salt, and parameters (memory cost, time cost, threads).
   - Salt: A unique random value to prevent precomputed attacks (e.g., rainbow tables).
2. **Memory Filling**:
   - Allocates a user-specified amount of memory.
   - Password and salt are mixed using iterative transformations over the allocated memory blocks.
3. **Rounds of Hashing**:
   - Repeated mixing of memory blocks based on time cost.
   - In Argon2d, this is data-dependent; in Argon2i, it is data-independent.
4. **Finalization**:
   - Produces a fixed-length hash output (configurable).

## Key features

### Memory-Hardness

- Requires a significant amount of memory, making it resistant to GPU/ASIC brute-force attacks.
- Ideal for mitigating large-scale password cracking.

#### Adjustable Parameters

- **Memory Cost**: Amount of memory (e.g., 256 MB) used during hashing.
- **Time Cost**: Number of iterations (rounds) the algorithm performs.
- **Parallelism**: Number of parallel threads used during computation.
- These parameters allow a balance between security and performance based on application needs.

#### Salted Hashing

- Salt ensures that even identical passwords produce different hashes.
- Prevents attackers from exploiting precomputed hashes.

#### Resistance to Attacks

- **Brute-Force Attacks**: High memory requirements slow down password cracking.
- **Side-Channel Attacks**: Argon2i protects against timing and cache-timing attacks.
- **ASIC/GPU Resistance**: Memory-hard design makes it inefficient for attackers using specialized hardware.

### Parameters and impact

| **Parameter** | **Description** | **Impact** |
| --- | --- | --- |
| **Memory Cost** | Amount of memory (e.g., 64 MB, 1 GB). | Higher memory increases resistance to parallel attacks. |
| **Time Cost** | Number of iterations (e.g., 1, 3, 10). | More iterations increase computational effort, slowing attackers. |
| **Parallelism** | Number of parallel threads (e.g., 1, 2, 4). | Higher threads improve speed on multi-core systems. |
| **Salt Length** | Length of the random salt (e.g., 16 bytes, 32 bytes). | Longer salts increase randomness and reduce collision risk. |
| **Output Length** | Length of the resulting hash (e.g., 128 bits, 256 bits). | Can be adjusted based on application needs. |

## Use cases

| **Use Case** | **Description** |
| --- | --- |
| **Password Hashing** | Securely store user passwords. |
| **Key Derivation** | Derive cryptographic keys from passwords. |
| **Authentication Systems** | Protect user credentials in login systems. |
| **Blockchain Applications** | Secure hash functions for cryptographic operations. |

## Advantages & disadvantages

### Advantages

| **Advantage** | **Description** |
| --- | --- |
| **Highly Secure** | Resistant to GPU/ASIC attacks due to its memory-hardness. |
| **Flexible Configuration** | Adjustable parameters allow balancing between security and performance. |
| **Side-Channel Attack Resistance** | Argon2i mitigates timing and cache-based attacks. |
| **Future-Proof** | Stronger resistance to brute-force attacks compared to older methods. |

### Disadvantages

| **Disadvantage** | **Description** |
| --- | --- |
| **Resource-Intensive** | Requires significant memory and CPU resources, which might impact performance on low-power systems. |
| **Limited Adoption** | Not as widely supported in older systems compared to SHA or bcrypt. |

### Argon2 vs. other algorithms

| **Feature** | **Argon2** | **Bcrypt** | **PBKDF2** |
| --- | --- | --- | --- |
| **Memory-Hardness** | High | Low | Low |
| **Customizability** | High | Moderate | High |
| **Side-Channel Resistance** | Strong (Argon2i) | Weak | Weak |
| **Performance** | Adjustable | Moderate | Slower |
| **Security** | High | Moderate | Moderate |

## Summary

Argon2 is the **gold standard** for password hashing, offering high security and flexibility. Its memory-hard design makes it resistant to modern hardware attacks, while its configurability allows fine-tuning for specific environments.

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
