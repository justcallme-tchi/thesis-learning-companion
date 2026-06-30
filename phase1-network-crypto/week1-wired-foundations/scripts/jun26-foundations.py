## NumPy in 30 minutes — what actually matters for your thesis

#You'll use NumPy constantly: packet byte arrays, image pixel matrices, feature vectors. Learn it in that context.

### Arrays — the foundation

import numpy as np

# 1D array — like a single packet's features
features = np.array([0, 1, 234, 0, 0.5, 12])
print(features.shape)   # (6,)
print(features.dtype)   # float64

# 2D array — like a batch of NSL-KDD rows (rows=samples, cols=features)
data = np.array([
    [0, 1, 234, 0],
    [1, 0,  10, 1],
    [0, 0,   5, 0],
])
print(data.shape)   # (3, 4) — 3 samples, 4 features


### Slicing — extracting what you need

# Single row (one packet)
data[0]          # array([0, 1, 234, 0])

# Single column (one feature across all packets)
data[:, 2]       # array([234, 10, 5])
#      ^ all rows, column index 2

# Submatrix — first 2 rows, first 3 columns
data[0:2, 0:3]   # array([[0,1,234],[1,0,10]])

# Boolean mask — filter rows where feature col 1 == 1 (e.g. logged_in=True)
mask = data[:, 1] == 1
data[mask]       # array([[0, 1, 234, 0]])


#The boolean mask is what you'll use to filter NSL-KDD by attack class:

labels = np.array(['normal', 'dos', 'normal'])   # 3 elements — must match data's 3 rows
dos_rows = data[labels == 'dos']

""" Real NSL-KDD usage you'll write in Week 4:
X_dos   = X[labels == 'dos']
X_probe = X[labels == 'probe']
X_normal = X[labels == 'normal']"""

### Broadcasting — operations without loops

# Normalize a feature column to [0, 1] — no for loop needed
col = np.array([0, 234, 10, 5, 512])
col_min, col_max = col.min(), col.max()
normalized = (col - col_min) / (col_max - col_min)
# array([0.0, 0.457, 0.019, 0.009, 1.0])

#Broadcasting rule: NumPy stretches the scalar across every element. This is how MinMaxScaler works internally on your NSL-KDD features.

# Binary image normalization — exactly what your malware pipeline will do
image_bytes = np.array([0, 128, 255, 64, 200], dtype=np.uint8)
normalized_image = image_bytes / 255.0
# array([0.0, 0.502, 1.0, 0.251, 0.784])

### Reshape — turning a byte stream into an image, This is the core operation of your MalImg preprocessing:

# Simulate reading a malware binary as raw bytes
binary_data = np.random.randint(0, 256, size=1024, dtype=np.uint8)

# Reshape to a 2D grayscale image (32×32 pixels)
image = binary_data.reshape(32, 32)
print(image.shape)  # (32, 32)

# In your real pipeline, width=256 is standard for MalImg
# file_bytes = np.frombuffer(open('sample.exe','rb').read(), dtype=np.uint8)
# image = file_bytes[:len(file_bytes) - len(file_bytes)%256].reshape(-1, 256)


### Axis operations — aggregating across rows or columns

data = np.array([[10, 200, 0],
                 [5,  150, 1],
                 [80,  10, 0]])

data.mean(axis=0)   # mean per feature:  [31.6, 120.0, 0.33]
data.mean(axis=1)   # mean per sample:   [70.0, 52.0, 30.0]
data.sum(axis=0)    # sum per feature
data.max(axis=0)    # max per feature  ← used in feature importance checks