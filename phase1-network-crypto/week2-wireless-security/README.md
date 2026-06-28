# W2 — Wireless Security
**Jul 3 – Jul 9**

## Study topics
- 802.11 MAC frame structure: management/control/data subtypes
- WPA2 4-way handshake: PTK derivation, MIC verification, offline dictionary attack
- Evil Twin attack: beacon frame spoofing, deauthentication flood
- WPA3 PMF (802.11w): Protected Management Frames
- PMKID attack: single EAPOL frame key extraction
- Python Pandas: read_csv, groupby, value_counts (30 min/day)

## Lab deliverables
- [ ] Monitor mode setup + airodump-ng scan → `lab-outputs/airodump_scan.png`
- [ ] WPA2 handshake capture (own network) → `lab-outputs/eapol_4way.pcap`
- [ ] Annotated handshake screenshot → `lab-outputs/eapol_annotated.png`
- [ ] Python lab: packets.csv analysis + top-5 talkers bar chart → `lab-outputs/top_talkers.png`

## Thesis connection
Dr. Zeraoulia published on MAC spoofing detection in 802.11 networks —
the same protocol layer studied this week. Mention this when approaching him.

## Resources
- Aircrack-ng docs: https://www.aircrack-ng.org/documentation.html
- Pandas 10-min guide: https://pandas.pydata.org/docs/user_guide/10min.html
- CISA WPA3 guidance
