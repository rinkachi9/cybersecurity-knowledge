#!/usr/bin/env python3
"""Caesar cipher: encrypt, decrypt and break by chi-squared frequency analysis.

Python 3.10 or later, standard library only. For study and CTF practice.

Usage:
  python3 caesar.py enc 3 "attack at dawn"
  python3 caesar.py dec 3 "dwwdfn dw gdzq"
  python3 caesar.py break "<ciphertext>"     # ranks all 26 shifts
"""
import string
import sys

ALPHABET = string.ascii_uppercase

# Relative frequencies of letters in English text (percent), A..Z.
# Source: Lewand, "Cryptological Mathematics", MAA 2000, as reproduced in many
# references; small differences between corpora do not change the ranking.
ENGLISH = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966,
           0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987,
           6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]


def shift(text: str, k: int) -> str:
    """Shift letters by k positions, keep case, leave other characters alone."""
    out = []
    for ch in text:
        if ch.isascii() and ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            out.append(chr((ord(ch) - base + k) % 26 + base))
        else:
            out.append(ch)
    return "".join(out)


def counts(text: str) -> list[int]:
    c = [0] * 26
    for ch in text.upper():
        if ch in ALPHABET:
            c[ord(ch) - 65] += 1
    return c


def chi_squared(text: str) -> float:
    """Distance between the letter counts of text and English expectations."""
    c = counts(text)
    n = sum(c) or 1
    return sum((c[i] - n * ENGLISH[i] / 100) ** 2 / (n * ENGLISH[i] / 100) for i in range(26))


def crack(ciphertext: str) -> list[tuple[int, float, str]]:
    """Try every key. Return (key, chi2, plaintext) sorted best first."""
    results = []
    for k in range(26):
        candidate = shift(ciphertext, -k)
        results.append((k, chi_squared(candidate), candidate))
    return sorted(results, key=lambda r: r[1])


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == "enc":
        print(shift(sys.argv[3], int(sys.argv[2])))
    elif cmd == "dec":
        print(shift(sys.argv[3], -int(sys.argv[2])))
    elif cmd == "break":
        for k, score, pt in crack(sys.argv[2])[:5]:
            print(f"key={k:2d} chi2={score:9.2f} {pt[:60]}")
    else:
        sys.exit(__doc__)
