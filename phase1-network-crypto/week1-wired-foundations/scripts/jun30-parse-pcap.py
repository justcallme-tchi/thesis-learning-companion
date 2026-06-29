#Tuesday June 30 — Python pcap script (2h code)

#Goal: a script that reads a `.pcap` file, extracts key fields per packet into a Pandas DataFrame, saves to `packets.csv` — this CSV is your input for Week 2's Python lab.

"""Step 1 — Save a pcap from Wireshark (10 min)**
- Open Wireshark, capture 1–2 minutes of normal browsing traffic
- File → Save As → `capture.pcap`
- Save it to your working folder"""

#Step 2 — Write the script (1.5h) , Create `parse_pcap.py`

from scapy.all import rdpcap
import pandas as pd

packets = rdpcap('capture.pcap')

rows = []
for pkt in packets:
    row = {
        'src_ip': None,
        'dst_ip': None,
        'protocol': None,
        'length': len(pkt)
    }
    if pkt.haslayer('IP'):
        row['src_ip'] = pkt['IP'].src
        row['dst_ip'] = pkt['IP'].dst
        row['protocol'] = pkt['IP'].proto
    rows.append(row)

df = pd.DataFrame(rows)
df.dropna(inplace=True)
print(df.head(10))
print(df['protocol'].value_counts())
df.to_csv('packets.csv', index=False)
print("Saved packets.csv —", len(df), "rows")


"""Step 3 — Run and inspect (20 min)**
- Run: `python parse_pcap.py`
- Open `packets.csv` in any spreadsheet viewer or just `print(df.describe())`
- Note: protocol 6 = TCP, protocol 17 = UDP, protocol 1 = ICMP
- Add a mapped column:
"""
proto_map = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}
df['protocol_name'] = df['protocol'].map(proto_map).fillna('OTHER')
print(df['protocol_name'].value_counts())

"""Step 4 — Commit to GitHub (10 min)
- Save `parse_pcap.py` to your repo under a `scripts/` folder
- Save `packets.csv` to `results/`
- Commit with message: `W1 complete: pcap parser + ARP/DNS Wireshark captures`
"""