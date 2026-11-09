# Network attacks

The attacks that play out across the network, viewed as stages of an intrusion and as a denial-of-service family. Each note ends with detection and mitigation, and is framed for authorized, defensive use. The link-layer, core-protocol, DNS and wireless subareas hold the attacks tied to a specific layer; this subarea holds the cross-cutting ones and the attacker's progression.

## Notes

- [Man-in-the-middle (adversary-in-the-middle)](man-in-the-middle.md): the on-path position, how it is reached, and why end-to-end encryption is the defense.
- [Network scanning](network-scanning.md): host, port and service discovery, and detecting scans.
- [Lateral movement](lateral-movement.md): spreading from one host to others east-west, and containing it.
- [Command and control traffic](command-and-control-traffic.md): the attacker's channel to implants, and disrupting it.
- [Data exfiltration](data-exfiltration.md): getting stolen data out, and the outbound controls that stop it.
- [Denial of service](denial-of-service/README.md): volumetric, protocol and application attacks on availability, with SYN flood, ICMP flood, ping of death and DDoS.

Back to [Network security](../README.md).
