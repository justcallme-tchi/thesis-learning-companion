# Thesis Learning Companion
**GPU-Accelerated ML for Cybersecurity — Study & Lab Tracker**

This repo tracks my learning journey alongside my M2 thesis:
*"GPU-Accelerated Machine Learning for Real-Time Cybersecurity Threat Detection with FPGA-Based Edge Deployment"*

> ⚠️ This is the **learning companion repo** — notes, lab outputs, and week-by-week scripts.
> The **thesis prototype repo** lives separately at `thesis-gpu-fpga-ids`.

---

## Timeline

| Phase | Topic | Dates |
|-------|-------|-------|
| Phase 1 | Network security & cryptography | Jun 26 – Jul 24 |
| Phase 2 | OS internals + ML fundamentals + CV intro | Jul 25 – Aug 14 |
| Phase 3 | Deep learning + malware + prototype build | Aug 15 – Sep 30 |
| Phase 4 | Advanced CV + FPGA first deployment | Oct – Nov 2026 |
| Phase 5 | Edge AI + adversarial basics | Dec 2026 – Jan 2027 |
| Phase 6 | Integration + benchmarks + results | Feb – Mar 2027 |
| Phase 7 | Thesis writing + defense | Apr – Jun 2027 |

---

## Repo structure

```
phase1-network-crypto/
  week1-wired-foundations/
    notes/        ← study notes per topic
    lab-outputs/  ← screenshots, CSVs, figures from labs
    scripts/      ← Python scripts written during the week
  week2-wireless-security/  ...
  week3-cryptography/       ...
  week4-ids-nslkdd/         ...

phase2-os-ml-cv/   ... (weeks 5–7)
phase3-deeplearning-malware-proto/  ... (weeks 8–13)
phase4-advanced-cv-fpga/   ... (oct–nov)
phase5-edge-ai-adversarial/  ... (dec–jan)
phase6-integration-results/  ... (feb–mar)
phase7-writing-defense/      ... (apr–jun)

results/
  figures/      ← all thesis-quality figures generated from code
  benchmarks/   ← benchmarks.csv and timing tables
  captures/     ← Wireshark .pcap files
```

---

## Commit convention

```
W1: add ARP/DNS Wireshark screenshots
W1: pcap parser script working
W6: random forest F1 results on NSL-KDD
W9: CPU vs GPU benchmark table
```

## Current week
**W1 — Wired foundations** (Jun 26 – Jul 2)
