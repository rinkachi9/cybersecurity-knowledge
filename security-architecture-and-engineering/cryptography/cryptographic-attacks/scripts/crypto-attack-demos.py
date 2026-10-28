# Python 3.10, standard library only.
# Run: python3 crypto-attack-demos.py
# Five small demonstrations of attack classes from CISSP section 3.7, on toy parameters, with synthetic data:
# ciphertext-only (frequency analysis), known plaintext, keystream reuse, hash collision (birthday) and a timing leak.
import hashlib
import hmac
import os
from collections import Counter

# 1. Ciphertext only: frequency analysis breaks a Caesar (shift) cipher without any plaintext.
# English letter frequencies in percent (a to z), the usual textbook approximation.
ENGLISH = [8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0, 0.15, 0.77, 4.0, 2.4,
           6.7, 7.5, 1.9, 0.095, 6.0, 6.3, 9.1, 2.8, 0.98, 2.4, 0.15, 2.0, 0.074]
plain = ("the purpose of a security control is to make an attack cost more than the attacker expects to gain "
         "and to make that attack visible to the people who defend the system. a single control rarely does both, "
         "so engineers combine preventive and detective measures and test whether they still work after every change "
         "to the environment, because a control that nobody tests is only a hope and not a measure of safety.")
shift = 11
cipher = "".join(chr((ord(c) - 97 + shift) % 26 + 97) if c.isalpha() else c for c in plain)

def chi2(text, k):
    letters = [chr((ord(c) - 97 - k) % 26 + 97) for c in text if c.isalpha()]
    counts, n = Counter(letters), len(letters)
    return sum((counts.get(chr(97 + i), 0) - n * ENGLISH[i] / 100) ** 2 / (n * ENGLISH[i] / 100) for i in range(26))

guess = min(range(26), key=lambda k: chi2(cipher, k))
print(f"1 ciphertext only      : true shift {shift}, guessed shift {guess} ({len(cipher)} characters)")

# 2. Known plaintext: a repeating-key XOR cipher gives up its key as soon as one plaintext block is known.
key = os.urandom(8)
msg = b"TRANSFER 1000 EUR TO ACCOUNT 12345678"
ct = bytes(m ^ key[i % 8] for i, m in enumerate(msg))
known = b"TRANSFER"                      # attacker knows the message starts with this word
recovered = bytes(c ^ k for c, k in zip(ct[:8], known))
print("2 known plaintext      : key recovered =", recovered == key)

# 3. Keystream reuse (two-time pad): c1 xor c2 = p1 xor p2, the key cancels out.
ks = os.urandom(40)
p1, p2 = b"attack at dawn, bring the keys now", b"meeting moved to noon, bring nothing"
c1 = bytes(a ^ b for a, b in zip(p1, ks)); c2 = bytes(a ^ b for a, b in zip(p2, ks))
x = bytes(a ^ b for a, b in zip(c1, c2))
crib = b"attack at"                       # a guessed word ("crib") placed at position 0
leak = bytes(a ^ b for a, b in zip(x, crib))
print("3 keystream reuse      : crib 'attack at' reveals", leak, "of the other message, without the key")

# 4. Birthday collision on a truncated hash: expected work is about 2^(n/2), not 2^n.
def trunc_hash(data, bits=32):
    return int.from_bytes(hashlib.sha256(data).digest(), "big") >> (256 - bits)

seen, tries = {}, 0
while True:
    tries += 1
    m = tries.to_bytes(8, "big")
    h = trunc_hash(m)
    if h in seen:
        break
    seen[h] = m
print(f"4 birthday (32-bit)    : collision after {tries} hashes (2^16 = 65536, 2^32 = 4294967296)")

# 5. Timing leak: an early-exit comparison reveals how many leading bytes are right.
def naive_compare(a, b):
    steps = 0
    for x_, y_ in zip(a, b):
        steps += 1
        if x_ != y_:
            return False, steps
    return True, steps

secret = hmac.new(b"k", b"msg", "sha256").digest()[:4]   # 4-byte tag, so recovery is quick
guess = bytearray(4)
for pos in range(4):
    best = max(range(256), key=lambda v: naive_compare(bytes(guess[:pos] + bytes([v]) + guess[pos + 1:]), secret))  # (ok, steps)
    guess[pos] = best
print("5 timing (step count)  : tag recovered byte by byte =", bytes(guess) == secret,
      "| constant-time compare_digest leaks no step count")
