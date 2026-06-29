"""
W1 NumPy side-thread — June 28
Network-flavored array exercise.

Fake packet table: 10 rows × 4 columns
  col 0: src_ip   (encoded as int, e.g. 192168001010 → just use small ints)
  col 1: dst_ip
  col 2: protocol (6=TCP, 17=UDP, 1=ICMP)
  col 3: bytes_sent
"""

import numpy as np

# ── 1. Build the array ──────────────────────────────────────────────────────
packets = np.array([
    [101, 201, 6,  1500],   # TCP
    [101, 202, 17,  300],   # UDP
    [102, 201, 6,  4200],   # TCP
    [103, 203, 1,    64],   # ICMP
    [101, 201, 6,   800],   # TCP
    [104, 202, 17,  150],   # UDP
    [102, 203, 1,    64],   # ICMP
    [101, 204, 6,  9000],   # TCP
    [103, 201, 17,  500],   # UDP
    [104, 203, 6,  2200],   # TCP
], dtype=np.int64)

print("Shape:", packets.shape)          # (10, 4) — 10 packets, 4 features
print("All bytes_sent:", packets[:, 3]) # column slice — axis=0 is rows, axis=1 is columns

# ── 2. Mean bytes per protocol ───────────────────────────────────────────────
# np.mean(array, axis=0) → mean down each column (across all rows)
# np.mean(array, axis=1) → mean across each row (across all columns)
# We want per-protocol, so we filter rows first, then mean the bytes column.

for proto, name in [(6, "TCP"), (17, "UDP"), (1, "ICMP")]:
    mask = packets[:, 2] == proto        # boolean array: True where protocol matches
    subset = packets[mask]               # fancy indexing — select only matching rows
    mean_bytes = np.mean(subset[:, 3])   # mean of bytes_sent column for this protocol
    count = subset.shape[0]
    print(f"{name:>4}  packets={count}  mean_bytes={mean_bytes:.1f}")

# ── 3. Broadcasting example ──────────────────────────────────────────────────
# Normalize bytes_sent to [0, 1] range — subtract min, divide by range.
# NumPy broadcasts the scalar across all 10 rows automatically.
bytes_col = packets[:, 3].astype(float)
normalized = (bytes_col - bytes_col.min()) / (bytes_col.max() - bytes_col.min())
print("\nRaw bytes:      ", bytes_col)
print("Normalized:     ", np.round(normalized, 3))
# Notice: 64 → 0.0 (smallest), 9000 → 1.0 (largest)
# This is exactly what MinMaxScaler does to NSL-KDD features in Week 4.

# ── 4. Axis operation — column means ─────────────────────────────────────────
col_means = np.mean(packets, axis=0)   # axis=0 = collapse rows → one value per column
print("\nColumn means (across all 10 packets):")
print(f"  src_ip mean:    {col_means[0]:.1f}")
print(f"  dst_ip mean:    {col_means[1]:.1f}")
print(f"  protocol mean:  {col_means[2]:.1f}")
print(f"  bytes mean:     {col_means[3]:.1f}")

row_means = np.mean(packets, axis=1)   # axis=1 = collapse columns → one value per row
print("\nRow means (one per packet — not that useful here, just axis practice):")
print(row_means)