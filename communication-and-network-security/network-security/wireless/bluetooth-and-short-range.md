# Bluetooth and short-range wireless

## Summary

Bluetooth and other short-range wireless technologies (Bluetooth Classic and Bluetooth Low Energy, plus NFC and Zigbee) are everywhere: peripherals, headsets, wearables, medical devices, access badges and industrial sensors. Their short range limits but does not remove the threat, an attacker only needs to be nearby, and "nearby" can be tens or hundreds of meters with the right antenna. The security issues are weak or absent pairing authentication, discoverability that aids tracking and attack, and a steady stream of implementation vulnerabilities (BlueBorne, KNOB, BLURtooth and others). For most organizations the practical defense is policy and hygiene: disable what is not needed, keep devices patched, pair in private, and treat Bluetooth-connected devices as part of the attack surface rather than ignoring them.

## Prerequisites

- [Network threat model](../foundations/network-threat-model.md): the physically-proximate attacker.
- [IoT network security](../ot-and-iot/iot-network-security.md): many short-range devices are IoT.
- Basic understanding of pairing and encryption.

## Core concepts

### Definition

*Bluetooth* is a short-range wireless standard with two main variants: *Bluetooth Classic* (BR/EDR, for audio and data) and *Bluetooth Low Energy* (BLE, for low-power sensors and wearables). *Short-range wireless* here also covers NFC (very short range, payments and badges) and Zigbee/Z-Wave (home and building automation). They share the property of pairing devices over the air with varying authentication strength.

### Analogy

Bluetooth pairing is like two people agreeing on a secret handshake while standing close together. If they agree it carefully and privately, outsiders cannot copy it. But some devices use a trivial handshake (a fixed code like 0000), some agree it in a way a nearby observer can copy, and some will "re-agree" with anyone who asks convincingly. And because devices announce "I am here and discoverable", a stranger knows exactly who is in the room and can approach.

The analogy holds well; it breaks in that the "standing close" distance can be stretched far with directional antennas, so proximity is a weaker protection than it feels.

### The security issues

- **Weak pairing authentication.** *Just Works* pairing (common on devices with no screen or keypad) provides encryption but no authentication, so it does not prevent an on-path attacker during pairing. Legacy PINs (0000, 1234) are trivially guessed. Strong pairing (numeric comparison, passkey, out-of-band) resists this but is not always used.
- **Discoverability and tracking.** Discoverable devices advertise their presence and often a stable identifier, enabling tracking of people by their devices. BLE added randomized addresses to mitigate this, but many devices still leak identifiers.
- **Implementation vulnerabilities.** A recurring stream: *BlueBorne* (2017, remote code execution over Bluetooth with no pairing), *KNOB* (2019, forcing a weak encryption key during negotiation), *BLURtooth* and *BLESA* (pairing and reconnection flaws). These are patched over time, but unpatched and unpatchable devices remain exposed.
- **Range underestimation.** Class 1 and directional antennas extend "short range" well beyond the assumed few meters, so physical proximity is less protective than designers assume.

### KNOB as an illustrative example

The KNOB (Key Negotiation of Bluetooth) attack exploited that the encryption key length was negotiated and could be forced down to a single byte of entropy, which is then brute-forced, breaking the encryption of a Classic Bluetooth link. It is instructive because it is a *negotiation-without-integrity* weakness (the same pattern as TLS downgrade), not a key-guessing attack: the fix enforces a minimum key length so the downgrade has nowhere to go. It was addressed in the specification and in patches.

### Why it matters for organizations

- Bluetooth peripherals (keyboards, headsets) can be entry points or eavesdropping channels; a compromised Bluetooth keyboard is a keylogger.
- BLE is used in access control (badges, phone-as-key) and medical devices, where a pairing or replay flaw has real safety and security impact.
- Discoverable devices aid physical reconnaissance and tracking.
- These devices are often outside normal patch and inventory processes, so they linger unpatched.

## Worked example

This is conceptual (no Bluetooth radio exercised in the lab). An organization reviews its short-range wireless exposure:

1. **Inventory.** It finds Bluetooth keyboards and headsets, BLE badge readers, and staff wearables. None were in the asset inventory or patch process.
2. **Pairing hygiene.** Some devices use Just Works or legacy PIN pairing. Policy is set to require strong pairing (numeric comparison or passkey) where supported and to pair only in a private setting, not in public where an attacker could be present during the vulnerable pairing step.
3. **Discoverability.** Devices are configured non-discoverable except when actively pairing, reducing tracking and targeting.
4. **Patching.** Bluetooth stacks on phones and laptops are kept current (closing BlueBorne/KNOB-class issues); devices that cannot be patched and are not essential are removed, and essential unpatchable ones (some medical or OT devices) are isolated and compensated for, as in [IoT network security](../ot-and-iot/iot-network-security.md).
5. **Sensitive peripherals.** Wireless keyboards in high-security areas are replaced with wired ones, removing the eavesdropping and injection channel entirely.

The review treats short-range wireless as part of the attack surface with ordinary controls (inventory, patch, configuration, isolation), which is the practical defense for most organizations.

## Trade offs and when to use it

- **Convenience vs exposure.** Wireless peripherals are convenient but add an over-the-air attack surface; in high-security areas, wired alternatives remove it entirely. Decide by sensitivity.
- **Disable vs manage.** Disabling Bluetooth where unneeded is the simplest control; where it is needed (headsets, badges), manage it with strong pairing, non-discoverability and patching.
- **Range assumptions.** Do not rely on short range as a security boundary; assume a capable attacker can reach further than expected.
- **Unpatchable devices.** Medical and OT devices often cannot be patched; isolate and monitor them rather than trusting the Bluetooth link.

## Common mistakes

- **Ignoring Bluetooth/BLE in inventory and patching.** Devices linger with known vulnerabilities. Fix: inventory them and keep stacks patched.
- **Leaving devices discoverable.** Aids tracking and targeting. Fix: non-discoverable except during pairing.
- **Accepting Just Works or legacy PIN pairing for anything sensitive.** No authentication. Fix: strong pairing methods; pair in private.
- **Trusting short range as a boundary.** Antennas extend it. Fix: do not rely on proximity; secure the link and the device.
- **Wireless keyboards in sensitive areas.** Eavesdropping/injection channel. Fix: wired peripherals where it matters.

## Practice

1. Why is short range a weaker protection than it intuitively seems?
2. What is wrong with Just Works pairing, and when is it used?
3. What kind of weakness did the KNOB attack exploit, and how is it like a TLS downgrade?
4. Why are Bluetooth and BLE devices often left unpatched in organizations?
5. What is the simplest effective control for Bluetooth where it is not needed?

### Answers

1. Directional and high-power antennas extend the effective range well beyond the assumed few meters, so an attacker does not have to be as close as the technology's nominal range suggests.
2. Just Works provides encryption but no authentication, so it does not stop an on-path attacker during pairing; it is used on devices with no screen or input to confirm a code.
3. KNOB forced the negotiated encryption key length down to minimal entropy so it could be brute-forced; it is a negotiation-without-integrity (downgrade) weakness like TLS downgrade, fixed by enforcing a minimum rather than by changing the cipher.
4. They are frequently outside normal asset inventory and patch management, and many embedded and medical/OT devices cannot be patched at all.
5. Disabling Bluetooth on devices and in environments where it is not required.

## Further reading

- NIST SP 800-121 Rev. 2, Guide to Bluetooth Security: https://doi.org/10.6028/NIST.SP.800-121r2
- The BlueBorne, KNOB, BLURtooth and BLESA research publications for the specific vulnerability classes.
- Bluetooth SIG security documentation: https://www.bluetooth.com/learn-about-bluetooth/key-attributes/bluetooth-security/
- [IoT network security](../ot-and-iot/iot-network-security.md) for isolating unpatchable short-range devices.
