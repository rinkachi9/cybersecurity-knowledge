# Python 3.10, standard library only.
# Run: python3 dlp-detectors.py
# Content detectors of a DLP engine on a small labeled synthetic corpus: a naive regex versus validation
# (Luhn checksum for card numbers, ISO 13616 mod-97 for IBANs) plus keyword proximity. Reports precision and recall.
# Test values: 4111 1111 1111 1111 is a well-known test card number, GB82 WEST 1234 5698 7654 32 is the
# documentation example IBAN, AKIAIOSFODNN7EXAMPLE is the example access key id from AWS documentation.
import re

def luhn_ok(digits):
    total, alt = 0, False
    for ch in reversed(digits):
        d = int(ch)
        if alt:
            d = d * 2 - 9 if d * 2 > 9 else d * 2
        total += d
        alt = not alt
    return total % 10 == 0

def iban_ok(s):
    s = s.replace(" ", "").upper()
    rearranged = s[4:] + s[:4]
    return int("".join(str(int(c, 36)) for c in rearranged)) % 97 == 1

CARD = re.compile(r"\b\d(?:[ -]?\d){12,18}\b")
IBAN = re.compile(r"\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){2,7}(?: ?[A-Z0-9]{1,3})?\b")
KEY = re.compile(r"\bAKIA[0-9A-Z]{16}\b")
CONTEXT = ("card", "visa", "payment", "cvv", "iban", "account", "transfer")

def naive(text):
    return {"card"} if CARD.search(text) else set()

def validated(text):
    found = set()
    for m in CARD.finditer(text):
        digits = re.sub(r"\D", "", m.group())
        near = text[max(0, m.start() - 40): m.end() + 40].lower()
        if 13 <= len(digits) <= 19 and luhn_ok(digits) and any(w in near for w in CONTEXT):
            found.add("card")
    for m in IBAN.finditer(text):
        if iban_ok(m.group()):
            found.add("iban")
    if KEY.search(text):
        found.add("cloud-key")
    return found

corpus = [  # (text, true labels)
    ("Please charge card 4111 1111 1111 1111 for the order", {"card"}),
    ("Wire to IBAN GB82 WEST 1234 5698 7654 32 by Friday", {"iban"}),
    ("export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE", {"cloud-key"}),
    ("Order number 4111111111111112 shipped yesterday", set()),                 # 16 digits, fails Luhn
    ("Tracking 1234 5678 9012 3456 expected Tuesday", set()),                    # fails Luhn
    ("Ticket 2026-10-27-0001-4455-9981 closed", set()),                          # digit run, no card context
    ("Visa payment 4111-1111-1111-1111 declined, retry", {"card"}),
    ("Meeting notes: nothing sensitive here", set()),
]

def score(detector, label, only=None):
    tp = fp = fn = 0
    for text, truth in corpus:
        got = detector(text)
        if only:
            got, truth = got & only, truth & only
        tp += len(got & truth); fp += len(got - truth); fn += len(truth - got)
    p = tp / (tp + fp) if tp + fp else 1.0
    r = tp / (tp + fn) if tp + fn else 1.0
    print(f"{label:22} tp={tp} fp={fp} fn={fn} precision={p:.2f} recall={r:.2f}")

score(naive, "naive, card only", {"card"})
score(validated, "validated, card only", {"card"})
score(validated, "validated, all types")

def redact(text):
    return CARD.sub(lambda m: "[CARD ****" + re.sub(r"\D", "", m.group())[-4:] + "]" if luhn_ok(re.sub(r"\D", "", m.group())) else m.group(), text)
print("redaction:", redact("Please charge card 4111 1111 1111 1111 for the order"))
