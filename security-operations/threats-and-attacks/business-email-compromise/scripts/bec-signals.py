# Python 3.10, standard library only.
# Run: python3 bec-signals.py
# Three BEC detection signals on synthetic data (reserved example domains only):
# 1 lookalike sender domain, 2 suspicious mailbox forwarding rules from an audit log, 3 payment-change gate with callback.
import unicodedata

KNOWN_PARTNERS = {"supplier-co.example", "ledger-bank.example", "acme-corp.example"}

def distance(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]

def lookalike(domain):
    if domain in KNOWN_PARTNERS:
        return "known partner"
    ascii_form = unicodedata.normalize("NFKD", domain).encode("ascii", "ignore").decode()
    flags = []
    if ascii_form != domain:
        flags.append("non-ASCII characters")
    near = [p for p in KNOWN_PARTNERS if distance(ascii_form, p) <= 2]
    if near:
        flags.append(f"edit distance <=2 from {near[0]}")
    return ", ".join(flags) or "no match"

for d in ("supplier-co.example", "supp1ier-co.example", "supplier-c0.example", "supplier-co.example.net", "newvendor.example"):
    print(f"1 sender domain {d:26} -> {lookalike(d)}")

# 2. Mailbox rules: forwarding to an outside domain, or moving mail with payment words to a hidden folder.
INTERNAL = "acme-corp.example"
audit_log = [
    {"user": "cfo@acme-corp.example", "op": "New-InboxRule", "forward_to": "ext-inbox@mailbox.example", "match": ""},
    {"user": "ap@acme-corp.example", "op": "New-InboxRule", "forward_to": "", "match": "invoice,wire,payment", "move_to": "RSS Subscriptions"},
    {"user": "hr@acme-corp.example", "op": "New-InboxRule", "forward_to": "", "match": "newsletter", "move_to": "Archive"},
]
for e in audit_log:
    reasons = []
    if e["forward_to"] and not e["forward_to"].endswith("@" + INTERNAL):
        reasons.append("forwards to an external address")
    if e.get("move_to") == "RSS Subscriptions" and any(w in e["match"] for w in ("invoice", "wire", "payment")):
        reasons.append("hides payment mail in a rarely read folder")
    print(f"2 rule by {e['user']:24} -> {', '.join(reasons) or 'looks normal'}")

# 3. Payment change gate: a change to bank details is applied only after a callback to a number already on file.
vendors = {"supplier-co.example": {"iban": "XX00 0000 0000 1111", "phone_on_file": "+00 555 0100"}}
def request_change(vendor, new_iban, callback_confirmed, number_called):
    v = vendors[vendor]
    if not callback_confirmed:
        return "held: no out-of-band confirmation"
    if number_called != v["phone_on_file"]:
        return "held: callback used a number from the email, not the number on file"
    v["iban"] = new_iban
    return "applied after callback to the number on file"
print("3 change, no callback            ->", request_change("supplier-co.example", "XX99 9999 9999 9999", False, ""))
print("3 callback to number in email    ->", request_change("supplier-co.example", "XX99 9999 9999 9999", True, "+00 555 0199"))
print("3 callback to number on file     ->", request_change("supplier-co.example", "XX11 2222 3333 4444", True, "+00 555 0100"))
