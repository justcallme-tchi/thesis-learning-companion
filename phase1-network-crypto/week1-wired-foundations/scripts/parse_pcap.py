"""
W1 Lab — pcap parser
Reads a Wireshark capture, extracts IP-layer fields into a DataFrame, saves CSV.
Usage: python parse_pcap.py capture.pcap
Output: lab-outputs/packets.csv + lab-outputs/protocol_distribution.png
"""

import sys
import pandas as pd
import matplotlib.pyplot as plt
from scapy.all import rdpcap

PCAP_FILE = sys.argv[1] if len(sys.argv) > 1 else "capture.pcap"

proto_map = {1: "ICMP", 6: "TCP", 17: "UDP"}

packets = rdpcap(PCAP_FILE)
rows = []
for pkt in packets:
    row = {"src_ip": None, "dst_ip": None, "protocol": None,
           "protocol_name": None, "length": len(pkt)}
    if pkt.haslayer("IP"):
        row["src_ip"] = pkt["IP"].src
        row["dst_ip"] = pkt["IP"].dst
        row["protocol"] = pkt["IP"].proto
        row["protocol_name"] = proto_map.get(pkt["IP"].proto, "OTHER")
    rows.append(row)

df = pd.DataFrame(rows).dropna()
print(f"Total packets with IP layer: {len(df)}")
print("\nProtocol distribution:")
print(df["protocol_name"].value_counts())
print("\nPacket length stats per protocol:")
print(df.groupby("protocol_name")["length"].agg(["mean", "max"]).round(1))

# Save CSV
df.to_csv("../lab-outputs/packets.csv", index=False)
print("\nSaved → lab-outputs/packets.csv")

# Plot
counts = df["protocol_name"].value_counts()
fig, ax = plt.subplots(figsize=(7, 4))
counts.plot(kind="barh", ax=ax, color="#378ADD")
ax.set_xlabel("Packet count")
ax.set_title("Protocol distribution — W1 pcap capture")
plt.tight_layout()
plt.savefig("../lab-outputs/protocol_distribution.png", dpi=150)
print("Saved → lab-outputs/protocol_distribution.png")
