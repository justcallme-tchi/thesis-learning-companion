# W4 — IDS Concepts + NSL-KDD First Contact
**Jul 17 – Jul 24**

## Study topics
- IDS vs IPS: detection-only vs inline blocking, signature vs anomaly-based
- NIST CSF v2.0: Govern/Identify/Protect/Detect/Respond/Recover
  → thesis addresses the Detect function (know the subcategory)
- MITRE ATT&CK: tactics vs techniques. Focus: T1190, T1566, T1021, T1041
- NSL-KDD structure: 41 features, 5 classes (Normal/DoS/Probe/R2L/U2R)
- NSL-KDD feature categories: basic connection, content, traffic features

## Lab deliverables
- [ ] NSL-KDD loaded + shape + dtypes → `scripts/nslkdd_explore.py`
- [ ] Class distribution chart → `lab-outputs/nslkdd_class_distribution.png`
- [ ] Encoded + scaled clean CSV → `lab-outputs/nslkdd_clean.csv`
- [ ] Scatter plot: src_bytes vs dst_bytes by class → `lab-outputs/nslkdd_scatter.png`
- [ ] Correlation heatmap → `lab-outputs/nslkdd_correlation.png`
- [ ] Top 5 correlated features written in notes

## Phase 1 milestone (Jul 24)
- [ ] Can capture/filter/parse traffic in Wireshark and Python
- [ ] Understand ARP spoofing at frame level
- [ ] Understand 802.11 handshake mechanics
- [ ] nslkdd_clean.csv ready for Phase 2 modeling
- [ ] Pandas and NumPy are operational tools

## Resources
- NSL-KDD dataset: https://www.unb.ca/cic/datasets/nsl.html
- MITRE ATT&CK: https://attack.mitre.org
- NIST CSF v2.0: https://www.nist.gov/cyberframework
