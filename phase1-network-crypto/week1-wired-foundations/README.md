# W1 — Wired Foundations
**Jun 26 – Jul 2**

## Study topics
- Routing tables: longest prefix match, static vs dynamic (RIP/OSPF/BGP)
- VLANs (802.1Q): trunk vs access ports, inter-VLAN routing
- ARP in depth: request/reply cycle, gratuitous ARP, cache poisoning mechanics
- DNS internals: recursive vs iterative, TTL, cache poisoning
- ICMP: Type 3/11, how traceroute exploits TTL expiry
- Python NumPy: arrays, slicing, broadcasting (30 min/day)

## Lab deliverables
- [ ] Wireshark ARP capture → `lab-outputs/arp_request.png` + `arp_reply.png`
- [ ] Wireshark DNS capture → `lab-outputs/dns_query.png` + `dns_response.png`
- [ ] Wireshark ICMP/traceroute capture → `lab-outputs/icmp_traceroute.png`
- [ ] Python pcap parser → `scripts/parse_pcap.py`
- [ ] Output CSV → `lab-outputs/packets.csv`
- [ ] Protocol distribution chart → `lab-outputs/protocol_distribution.png`

## Thesis connection
ARP spoofing and DNS poisoning are two attack vectors the CV pipeline
must detect. Understanding frame-level mechanics now means feature
engineering choices in W4 will be informed, not random.
Relevant NSL-KDD features: `dst_host_count`, `service`, `flag`, `src_bytes`

## Resources
- NetworkChuck YouTube
- Practical Networking: https://www.practicalnetworking.net
- Wireshark User Guide: https://www.wireshark.org/docs/wsug_html/
- NumPy quickstart: https://numpy.org/doc/stable/user/quickstart.html
