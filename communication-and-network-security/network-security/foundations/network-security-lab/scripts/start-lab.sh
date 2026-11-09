#!/usr/bin/env bash
# Bash 5, iproute2, Linux 5.x or later with unprivileged user namespaces enabled. No root needed.
# Run: ./start-lab.sh            (interactive shell inside the lab)
#      ./start-lab.sh script.sh  (run a script inside the lab, then tear everything down)
#
# Builds a throwaway network out of Linux network namespaces inside a user namespace, so it
# cannot touch the host network and disappears when the shell exits:
#
#   client 192.0.2.10 ---+                        +--- server 198.51.100.20
#                        |-- switch --- fw ---|
#   attacker 192.0.2.66 -+   (bridge)  (router,   (198.51.100.0/24, "inside")
#                                       nftables)
#   (192.0.2.0/24, "outside" LAN)
#
# Inside the lab use: ip netns exec <node> <command>, for example
#   ip netns exec client ping -c1 198.51.100.20
set -euo pipefail

if [[ "${LAB_INSIDE:-}" != 1 ]]; then
    # Re-execute inside a new user, mount and network namespace. We become "root" only there.
    exec unshare --user --map-root-user --net --mount env LAB_INSIDE=1 "$0" "$@"
fi

mount -t tmpfs lab-run /run          # private /run so "ip netns add" works without real root
mkdir -p /run/netns
for n in client attacker switch fw server; do ip netns add "$n"; ip -n "$n" link set lo up; done

ip -n switch link add lan type bridge
ip -n switch link set lan up
for n in client attacker fw; do
    # one veth pair per host: "eth0" in the host, "p-<host>" as a switch port on the bridge
    ip link add eth0 netns "$n" type veth peer name "p-$n" netns switch
    ip -n switch link set "p-$n" master lan up
    ip -n "$n" link set eth0 up
done
ip link add eth1 netns fw type veth peer name eth0 netns server
ip -n fw link set eth1 up
ip -n server link set eth0 up

ip -n client   addr add 192.0.2.10/24 dev eth0
ip -n attacker addr add 192.0.2.66/24 dev eth0
ip -n fw       addr add 192.0.2.1/24 dev eth0
ip -n fw       addr add 198.51.100.1/24 dev eth1
ip -n server   addr add 198.51.100.20/24 dev eth0
ip -n client   route add default via 192.0.2.1
ip -n attacker route add default via 192.0.2.1
ip -n server   route add default via 198.51.100.1
ip netns exec fw sysctl -qw net.ipv4.ip_forward=1

echo "lab ready: client 192.0.2.10, attacker 192.0.2.66, fw 192.0.2.1 / 198.51.100.1, server 198.51.100.20"
if [[ $# -gt 0 ]]; then
    bash "$@"
else
    PS1='[lab] \w # ' bash --norc
fi
