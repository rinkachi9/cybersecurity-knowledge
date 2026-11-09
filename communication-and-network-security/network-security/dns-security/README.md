# DNS security

DNS starts almost every connection, which makes it both a prime target and a powerful control point. These notes cover the threats to name resolution, the two protocol add-ons that secure it (authenticity and privacy), the covert-channel abuse, and how to use the resolver as a defense.

## Notes

- [DNS threat landscape](dns-threat-landscape.md): spoofing, cache poisoning (Kaminsky), hijacking, amplification and the resolution path. Read first.
- [DNSSEC](dnssec.md): signing records so forgeries are detected, with a tested validation example.
- [Encrypted DNS](encrypted-dns.md): DoT, DoH and DoQ, and the enterprise visibility tension.
- [DNS tunneling](dns-tunneling/README.md): data smuggled through query names, with a tested detector.
- [Protective DNS](protective-dns.md): using the resolver to block malicious lookups and to detect infection.

Scripts: under [dns-tunneling/scripts](dns-tunneling/scripts/), a synthetic log generator and an entropy-based tunnel detector.

Back to [Network security](../README.md).
