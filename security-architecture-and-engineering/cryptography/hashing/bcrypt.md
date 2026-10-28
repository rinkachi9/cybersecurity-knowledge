# Bcrypt

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

**Bcrypt** is a cryptographic algorithm designed specifically for secure password hashing. Introduced in **1999** by **Niels Provos and David Mazières**, bcrypt has been a reliable standard for password security due to its ability to adapt to increasing computing power.

### Overview

| **Feature** | **Description** |
| --- | --- |
| **Type** | Password hashing algorithm |
| **Introduced** | 1999 (by Niels Provos and David Mazières) |
| **Core Idea** | Implements a computationally expensive hashing process to slow down brute-force attacks. |
| **Based On** | Blowfish cipher (uses its key schedule algorithm). |
| **Key Strengths** | Adaptive cost parameter, salting, and resistance to brute-force attacks. |

## How it works

### Core concepts

1. **Salted Hashing**:
   - Adds a unique random value (salt) to the input password.
   - Prevents identical passwords from producing identical hashes.
   - Thwarts rainbow table attacks.
2. **Cost Factor**:
   - A tunable parameter (`log_rounds`) determines the computational expense of the hashing process.
   - Higher cost factors increase the time required to compute the hash, making brute-force attacks slower.

### Process

1. **Input**:
   - Password and a randomly generated salt.
2. **Key Expansion**:
   - Uses the Blowfish key schedule algorithm to repeatedly expand the password and salt.
3. **Rounds**:
   - Executes a user-defined number of iterations (`log_rounds`) to increase computation time.
4. **Output**:
   - A fixed-length 60-character hash containing:
     - Algorithm identifier (`$2b$` or `$2a$`).
     - Cost factor (e.g., `12` for 2^12 iterations).
     - Salt and hash.

## Key features

### Adaptive Cost

- The `log_rounds` parameter increases the number of iterations, allowing bcrypt to remain secure as hardware becomes more powerful.
- Example: A cost factor of `12` means 2^12 iterations are performed.

#### Built-in Salting

- Automatically generates a 128-bit salt for each password.
- Ensures that even identical passwords produce different hashes.

#### Fixed Output Length

- Always produces a 60-character hash, regardless of input password length.

#### Resistance to Brute-Force Attacks

- Computationally expensive due to the iterative design, making it slow for attackers to hash potential passwords.

## Use cases

| **Use Case** | **Description** |
| --- | --- |
| **Password Storage** | Safely stores user passwords in applications and systems. |
| **Authentication Systems** | Verifies user credentials during login. |
| **Key Derivation** | Derives cryptographic keys from passwords. |

## Advantages & disadvantages

### Advantages

| **Advantage** | **Description** |
| --- | --- |
| **Adaptive Cost** | Can adjust the cost factor (`log_rounds`) to counteract increasing hardware speeds. |
| **Built-in Salting** | Automatically salts passwords, ensuring uniqueness for each hash. |
| **Widely Supported** | Supported by most programming languages and frameworks. |
| **Resistance to Brute-Force** | High computational cost slows down attackers. |

### Disadvantages

| **Disadvantage** | **Description** |
| --- | --- |
| **Resource-Intensive** | Slower than other algorithms, which may impact performance in high-load systems. |
| **Fixed Output Length** | The fixed 60-character output may not meet all application requirements. |
| **Limited Hash Size** | Not ideal for applications requiring very large hash outputs. |

### Bcrypt vs. other algorithms

| **Feature** | **Bcrypt** | **Argon2** | **PBKDF2** |
| --- | --- | --- | --- |
| **Cost Adjustment** | Adaptive (log_rounds) | Highly customizable | Adjustable iterations |
| **Memory-Hardness** | Moderate | High | Low |
| **Side-Channel Resistance** | Weak | Strong (Argon2i) | Weak |
| **Speed** | Moderate | Adjustable | Slower |
| **Security** | High | Very High | Moderate |

## Best practices

1. **Choose an Appropriate Cost Factor**:
   - Higher cost factors increase security but also slow hashing.
   - Example:
     - Cost factor `12`: Reasonable balance for most modern systems.
     - Cost factor `14`: Stronger security for high-risk applications.
2. **Always Use Random Salt**:
   - Bcrypt automatically generates a salt, so there’s no need to implement this separately.
3. **Verify Passwords Securely**:
   - Always compare hashes using bcrypt’s built-in functions to avoid timing attacks.

## Summary

Bcrypt is a reliable and widely supported password hashing algorithm. Its **adaptive cost** ensures that it remains effective against brute-force attacks as computational power increases. While slower than some newer algorithms like Argon2, bcrypt remains a strong choice for applications requiring high security and compatibility.

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
