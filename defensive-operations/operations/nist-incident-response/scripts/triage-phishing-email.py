# Python 3.10, standard library only. Run: python3 triage-phishing-email.py
# Easy case: triage of one reported phishing email. The message is synthetic (RFC 5737 and example domains).
import hashlib
import re
from email import message_from_string
from email.utils import parseaddr
from html.parser import HTMLParser

RAW = """\
Return-Path: <billing@invoices-example.net>
Received: from mail.invoices-example.net (mail.invoices-example.net [203.0.113.44])
 by mx.example.com with ESMTPS; Tue, 06 Oct 2026 08:14:02 +0000
Authentication-Results: mx.example.com;
 spf=fail smtp.mailfrom=invoices-example.net;
 dkim=none; dmarc=fail header.from=example.com
From: "Accounts Payable" <ap@example.com>
Reply-To: ap-help@invoices-example.net
To: j.kowalska@example.com
Subject: Invoice 88231 overdue - action required
Date: Tue, 06 Oct 2026 08:13:50 +0000
Message-ID: <20261006081350.1@invoices-example.net>
MIME-Version: 1.0
Content-Type: text/html; charset=utf-8

<html><body>
<p>Your invoice is overdue. Review it here:
<a href="https://login.example.com.invoices-example.net/pay?id=88231">https://login.example.com/pay</a></p>
</body></html>
"""

msg = message_from_string(RAW)
findings = []

# 1. Authentication results are the strongest cheap signal
auth = " ".join(msg.get_all("Authentication-Results", [])).lower()
for mech in ("spf", "dkim", "dmarc"):
    m = re.search(rf"{mech}=(\w+)", auth)
    if m and m.group(1) != "pass":
        findings.append(f"{mech.upper()} result is '{m.group(1)}'")

# 2. Identity mismatches between From, Reply-To and Return-Path
from_dom = parseaddr(msg["From"])[1].split("@")[-1]
for hdr in ("Reply-To", "Return-Path"):
    dom = parseaddr(msg[hdr])[1].split("@")[-1]
    if dom and dom != from_dom:
        findings.append(f"{hdr} domain '{dom}' differs from From domain '{from_dom}'")


# 3. Visible link text versus real destination
class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links, self._href, self._text = [], None, []
    def handle_starttag(self, tag, attrs):
        if tag == "a": self._href, self._text = dict(attrs).get("href"), []
    def handle_data(self, data):
        if self._href: self._text.append(data)
    def handle_endtag(self, tag):
        if tag == "a" and self._href: self.links.append((self._href, "".join(self._text))); self._href = None


p = Links(); p.feed(msg.get_payload())
for href, text in p.links:
    host = re.sub(r"^https?://", "", href).split("/")[0]
    shown = re.sub(r"^https?://", "", text).split("/")[0]
    if shown != host:
        findings.append(f"link text shows '{shown}' but goes to '{host}'")
    if from_dom in host and not host.endswith("." + from_dom) and host != from_dom:
        findings.append(f"destination '{host}' only embeds '{from_dom}' as a label, it is not under that domain")

# 4. Evidence: hash the raw message so the record can be shown unchanged later
digest = hashlib.sha256(RAW.encode()).hexdigest()
relay_ips = re.findall(r"\[(\d+\.\d+\.\d+\.\d+)\]", RAW)

print("findings:")
for f in findings:
    print(" -", f)
print("first relay IP:", relay_ips[0])
print("evidence sha256:", digest[:16] + "...")
print("verdict:", "malicious" if len(findings) >= 3 else "needs review", f"({len(findings)} signals, several of them correlated)")
