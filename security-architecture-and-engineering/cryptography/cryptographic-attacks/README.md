# Cryptographic attacks

## Summary

A cryptographic attack recovers a secret, forges a value or distinguishes protected data from random without breaking the intended key. Most successful attacks in practice do not defeat the mathematics of a good algorithm. They exploit a weak or retired algorithm, a short key, reused values that must be unique, a leaking implementation or a protocol that treats an error message as harmless. This note classifies the attacks by what the attacker knows and by where the weakness sits, shows five of them running on toy parameters and ends with what defenders change: algorithm choice, key management, constant-time code and authenticated encryption. All offensive content here is for study, labs and authorized testing.

## Prerequisites

- [Hashing algorithms](../hashing/hashing-algorithms.md) and [SHA](../hashing/sha.md).
- [Public key infrastructure](../public-key-infrastructure.md).
- The [CIA triad](../../../security-and-risk-management/foundations/cia-triad/README.md): cryptography serves confidentiality, integrity and authenticity.
- Basic knowledge of symmetric and asymmetric cryptography.

## Core concepts

### Definition

*Cryptanalysis* is the study of breaking cryptographic systems. A *cryptographic attack* is a concrete method of doing so. The ISC2 CISSP exam outline (effective April 15, 2024, section 3.7) lists these methods: brute force, ciphertext only, known plaintext, frequency analysis, chosen ciphertext, implementation attacks, side-channel, fault injection, timing, man-in-the-middle, pass the hash, Kerberos exploitation and ransomware. The list mixes attacks on algorithms with attacks on the way cryptography is used, which is a reminder that the system is attacked, not only the cipher.

### Analogy

A lock has a design (the mechanism), a key (the secret) and an installation (the door, the frame, the person who uses it). Most break-ins do not pick a well designed lock. They use a spare key left under the mat (key management), a door with a window next to the lock (protocol), a lock that clicks differently when the right pin is set (side channel) or a lock model with a known flaw (retired algorithm). The analogy breaks in one way: a lock attacker works on one door, a cryptographic attacker can often test billions of guesses offline against a copy of the data.

### Why it matters and how it fails

Cryptography is the last control for data that has already left the owner's hands: a stolen disk, a captured packet, a leaked database dump. If it fails, there is usually no second layer. It fails in five places:

| Failure place | Example | What the attacker needs |
| --- | --- | --- |
| Algorithm | MD5 and SHA-1 collisions | Compute, often once |
| Key size and generation | 40-bit export keys, weak random numbers | Compute or luck |
| Mode and usage | ECB mode patterns, nonce or keystream reuse | Two ciphertexts |
| Implementation | Timing differences, padding oracle error messages | Network access to the target |
| Protocol and key management | Downgrade to a weak suite, stolen keys, no validation of certificates | Position in the network or a foothold |

### Classification by attacker knowledge

The classic model orders attacks by what the attacker has. The stronger the access, the more attacks work.

| Attack | Attacker has | Typical target | Defense |
| --- | --- | --- | --- |
| Ciphertext only | Ciphertexts | Classical and badly designed ciphers | Modern ciphers hide statistics |
| Known plaintext | Pairs of plaintext and ciphertext | XOR and linear ciphers, protocol headers | Ciphers that resist it by design |
| Chosen plaintext | Can encrypt chosen messages | Weak modes, CBC with predictable IV | Random IV, authenticated encryption |
| Chosen ciphertext | Can submit ciphertext for decryption and see the result or an error | Padding oracle, RSA without proper padding | Authenticated encryption, uniform errors |
| Brute force | The ciphertext and the key space | Short keys, passwords | Long random keys, slow password hashing |
| Frequency analysis | Ciphertext of a natural language | Substitution ciphers | Not applicable to modern ciphers |

Brute force is the baseline for every other attack: an attack is called a break when it beats trying all keys. Passwords turn brute force into a practical attack on modern systems, because their entropy is low. See [brute force](../../../identity-and-access-management/credential-attacks/brute-force-attack.md) and [Argon2](../hashing/argon2.md).

### Attacks on algorithms

**Hash collisions.** A hash with an `n`-bit output should need about `2^(n/2)` operations to find two inputs with the same hash (the birthday bound), and `2^n` to find an input for a given hash. MD5 and SHA-1 fell below these bounds. In February 2017 researchers at CWI Amsterdam and Google published the first practical SHA-1 collision, two different PDF files with the same SHA-1 value, which cost about nine quintillion SHA-1 computations, roughly 6,500 CPU-years and 110 GPU-years (shattered.io, checked 2026-10). NIST says SHA-1 should be phased out by December 31, 2030 and recommends SHA-2 or SHA-3 (NIST news item, December 2022). A collision lets an attacker prepare two documents or certificates that share a signature. It does not by itself reveal a preimage, so older uses such as password storage were not broken by collisions, but they were weak for other reasons (see [hashing algorithms](../hashing/hashing-algorithms.md)).

**Length extension.** Hashes built with the Merkle-Damgard construction (MD5, SHA-1, SHA-256) allow an attacker who knows `H(secret || message)` to compute `H(secret || message || padding || extra)` without the secret. Keyed constructions such as HMAC avoid this. Using `H(key || message)` as a MAC is the mistake. SHA-3 is not affected. I describe this from the standard construction and did not re-check it against a source for this note.

**Weak keys and small key spaces.** A 56-bit DES key was exhaustible by special hardware in the late 1990s, which is why it was retired. The rule today: symmetric keys of at least 128 bits, with security strength tables in NIST SP 800-57 and the transition rules in NIST SP 800-131A. I did not re-read those for this note.

### Attacks on usage

**Keystream and nonce reuse.** A stream cipher or a counter mode produces a keystream from a key and a nonce. If the same pair encrypts two messages, `C1 xor C2 = P1 xor P2`, so the key cancels out and the attacker can recover both plaintexts with guessed words (cribs). The same effect breaks AES-GCM badly: repeating a nonce under one key allows forgery of tags and leaks the XOR of plaintexts. The fix is a unique nonce per key, from a counter or a sufficiently large random value, and misuse-resistant modes where reuse is hard to avoid.

**ECB mode.** Electronic Codebook mode encrypts equal blocks to equal ciphertexts, so patterns in the data remain visible. A well known demonstration is an ECB-encrypted bitmap that still shows its picture. Do not use ECB for data longer than one block.

**Padding oracle.** If a server decrypts a CBC message and then reveals, by an error code, a message or timing, whether the padding was valid, an attacker can decrypt the message byte by byte without the key. Vaudenay described the attack in 2002. The defense is authenticated encryption (verify the MAC before decrypting) and identical responses for every failure. The CWE entries "Observable Timing Discrepancy" (CWE-208) and "Use of a Broken or Risky Cryptographic Algorithm" (CWE-327) are the closest weakness classes; CWE-327 lists CWE-208 as a follow-on.

**Predictable randomness.** Keys, IVs and nonces from a weak generator can be guessed. Use the operating system's cryptographic random source.

### Implementation and side-channel attacks

An implementation attack targets the code or hardware that runs a sound algorithm.

- **Timing attacks** measure how long an operation takes. Kocher showed in 1996 that timing differences in modular exponentiation leak private key bits. A comparison that stops at the first wrong byte leaks how many leading bytes are correct, so a MAC can be guessed one byte at a time. Use constant-time comparison (`hmac.compare_digest` in Python, `crypto/subtle` in Go).
- **Other side channels**: power consumption, electromagnetic emission, cache access patterns and acoustic noise.
- **Fault injection**: induce an error (voltage glitch, laser, rowhammer-style memory faults) so that the device outputs a faulty result that reveals the key.
- **Error oracles**: any difference in error response, such as the padding oracle above and Bleichenbacher's 1998 attack on RSA PKCS#1 v1.5 padding.

Defenses are constant-time code, blinding, hardware countermeasures, secure elements and hardware security modules for keys.

### Attacks on protocols and key management

- **Man-in-the-middle** places the attacker between two parties. It works when authentication of the peer is missing or skipped, for example certificates that are not validated. See [PKI](../public-key-infrastructure.md).
- **Downgrade attacks** force a weaker algorithm or protocol version.
- **Pass the hash** and **Kerberos exploitation** (CISSP 3.7) use a credential representation that works as the credential. They are authentication attacks, covered in [authentication](../../../identity-and-access-management/identity-and-access/authentication/README.md).
- **Key theft** is often easier than cryptanalysis: keys in source code, in environment variables, in backups or in memory of a compromised host.
- **Ransomware** in the CISSP list is a misuse of cryptography by the attacker: the attacker encrypts the victim's data with a key that only the attacker holds.

### Quantum and future threats

Large quantum computers would break RSA and elliptic curve cryptography with Shor's algorithm and would reduce symmetric key strength by a square root bound with Grover's algorithm. The current CISSP outline already lists quantum in section 3.6. Data that must stay secret for decades can be recorded now and decrypted later. NIST has standardized post-quantum algorithms; I did not verify the current list of standards for this note.

TODO: verify the NIST post-quantum standards (FIPS numbers and algorithm names) and the transition timeline against NIST publications.

## Worked example

The script `scripts/crypto-attack-demos.py` runs five attacks on toy parameters. Python 3.10, standard library only, synthetic data. The output is real.

```bash
python3 scripts/crypto-attack-demos.py
```

Output:

```text
1 ciphertext only      : true shift 11, guessed shift 11 (409 characters)
2 known plaintext      : key recovered = True
3 keystream reuse      : crib 'attack at' reveals b'meeting m' of the other message, without the key
4 birthday (32-bit)    : collision after 58968 hashes (2^16 = 65536, 2^32 = 4294967296)
5 timing (step count)  : tag recovered byte by byte = True | constant-time compare_digest leaks no step count
```

What each line shows:

1. **Ciphertext only.** A shift cipher is broken by comparing letter statistics of the ciphertext with English: for each of 26 candidate shifts, a chi-squared score against the English frequency table, lowest score wins. The attack needs enough text: an earlier version of this script used a short, unusual sentence and guessed the wrong shift, because the "most frequent letter is e" shortcut fails on small samples.
2. **Known plaintext.** The attacker knows the message starts with `TRANSFER`. XOR of the first 8 ciphertext bytes with the known text gives the 8-byte repeating key. Protocol headers and file formats make known plaintext common.
3. **Keystream reuse.** Two messages encrypted with the same keystream. XORing the ciphertexts removes the key. Placing the guessed word `attack at` at position 0 of the first message yields `meeting m` from the second.
4. **Birthday collision.** For a hash truncated to 32 bits a collision appears after 58,968 hashes, close to the square root of `2^32` (65,536) and nowhere near `2^32`. For comparison, the nine quintillion SHA-1 computations of the 2017 collision are about 2^63, well below the 2^80 birthday bound of a 160-bit hash, because better methods than plain birthday search exist.
5. **Timing.** The naive comparison returns at the first wrong byte, so the number of steps reveals the count of correct leading bytes. The script uses the step count as a stand-in for time, which makes it deterministic. In a real network attack the signal is noisy and the attacker averages many measurements. `hmac.compare_digest` takes the same time regardless of where the first difference sits.

The toy parameters are the point: the same logic on real systems needs more data, more time or a noisier channel, but not a different idea.

## Trade offs and when to use it

For defenders, the practical decision is not "which attack" but "which control removes the most cases":

| Control | Removes | Cost |
| --- | --- | --- |
| Use standard, current primitives (AES-GCM or ChaCha20-Poly1305, SHA-256 or SHA-3, ECDSA or Ed25519) | Algorithm weaknesses and many mode mistakes | Migration of old systems |
| Authenticated encryption instead of encrypt-then-hope | Chosen ciphertext, padding oracle, tampering | API change |
| Libraries that manage nonces and padding | Nonce reuse, ECB, custom constructions | Dependency |
| Constant-time primitives and comparisons | Timing leaks | Rarely a cost if the library does it |
| Keys in an HSM, KMS or secure enclave, short lifetimes and rotation | Key theft, long exposure | Operations and cost |
| Algorithm agility and an inventory of cryptography | Slow reaction to a retired algorithm | Effort to catalog |
| Strong, slow password hashing | Offline brute force of passwords | CPU and memory per login |

An attacker chooses by cost. A defender who encrypts correctly and stores the key on the same host has built the strongest lock on the weakest door.

When this analysis is the wrong tool: if the data is not sensitive after the next hour, or if the real risk is a stolen session, the effort belongs elsewhere. Do not invent your own algorithm or protocol; review by experts is the only evidence that a design works.

## Common mistakes

| Mistake | Effect | Fix |
| --- | --- | --- |
| Building a custom cipher or MAC (for example `H(key + message)`) | Length extension and unknown weaknesses | Use HMAC or an AEAD from a maintained library |
| Reusing a nonce or IV with the same key | Plaintext leak or forgery | Unique nonce per key, library-managed |
| Returning distinct errors for padding, MAC or format failures | Oracles | One generic error, same timing |
| Using SHA-1 or MD5 for signatures or certificates | Collisions | SHA-256 or stronger |
| Comparing secrets with `==` | Timing leak | Constant-time comparison |
| Hardcoding keys | Anyone with the code has the key | Secrets manager or KMS |
| Treating encryption as integrity | Ciphertext can be modified | Authenticated encryption |
| Ignoring randomness | Predictable keys | OS cryptographic random source |
| Detection blind spots | Attacks look like normal traffic | Log failed decryptions and MAC failures and alert on spikes |

Detection and mitigation: oracle attacks need many requests, so rate limiting and alerts on repeated decryption or signature failures expose them. Offline attacks leave no trace at the victim, so mitigation depends on strong primitives and key hygiene. Log cryptographic failures at the application and at the TLS terminator.

## Practice

1. For each of ciphertext only, known plaintext and chosen ciphertext, name the attacker's access and one realistic target.
2. Why did the 32-bit truncated hash collide after about 59,000 hashes and not after billions?
3. Why is `H(key || message)` unsafe as a MAC for SHA-256 but fine in principle for SHA-3?
4. A service returns "bad padding" for one kind of failure and "bad MAC" for another. What is the attack, and what is the minimal fix?
5. Modify demo 3 so that the key is a one-time pad of the same length as the message and each message gets its own key. What does the XOR of two ciphertexts reveal now?
6. Which CISSP sections list the attacks in this note?

**Answers and hints**

1. Ciphertext only: captured traffic, a substitution cipher. Known plaintext: a file header or fixed protocol field, an XOR cipher. Chosen ciphertext: an online service that decrypts and reports errors.
2. The birthday bound: with `2^32` possible values a collision is expected after about `2^16` hashes because each new hash is compared with all earlier ones.
3. Merkle-Damgard hashes expose their internal state as the output, so it can be continued. SHA-3 uses a sponge construction whose output does not reveal the whole state. HMAC is still the standard choice.
4. A padding oracle. Verify the MAC first and return one error for all failures. Better, use AEAD.
5. Nothing useful: with independent random keys of the same length the XOR of two ciphertexts is uniformly random. The pad must never be reused.
6. Section 3.7 (cryptanalytic attacks), section 3.6 (cryptographic solutions and key management) and section 3.4 (security capabilities such as the TPM). See [CISSP security domains](../../../security-and-risk-management/reference/certifications/cissp-security-domains.md).

## Further reading

- ISC2, *CISSP Certification Exam Outline*, effective April 15, 2024, sections 3.6 and 3.7: the list of attacks used for the classification ([PDF](https://edge.sitecorecloud.io/internationf173-xmc4e73-prodbc0f-9660/media/Project/ISC2/Main/Media/documents/exam-outlines/CISSP-Exam-Outline-April-2024-English.pdf)).
- Stevens et al., [The first collision for full SHA-1](https://shattered.io/) (CWI Amsterdam and Google, February 2017).
- NIST, [NIST retires SHA-1 cryptographic algorithm](https://www.nist.gov/news-events/news/2022/12/nist-retires-sha-1-cryptographic-algorithm) (December 2022): the 2030 phase-out date.
- MITRE, [CWE-327](https://cwe.mitre.org/data/definitions/327.html) and CWE-208: weakness classes for risky algorithms and timing discrepancies.
- Kocher (1996), Timing attacks on implementations of Diffie-Hellman, RSA, DSS and other systems; Vaudenay (2002), Security flaws induced by CBC padding; Bleichenbacher (1998), Chosen ciphertext attacks against protocols based on RSA encryption standard PKCS #1. Cited from memory, not re-read for this note.
- NIST SP 800-57 (key management) and SP 800-131A (transitions of algorithms and key lengths). Not re-read for this note.
