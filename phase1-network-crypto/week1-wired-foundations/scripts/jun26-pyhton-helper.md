# I - NumPy Arrays: The Foundational Blocks

In cybersecurity, a 1D array is often used to represent the extracted attributes or metrics of a **single network packet** or a **single log event**.

```python
import numpy as np

# 1D array — like a single packet's features
features = np.array([0, 1, 234, 0, 0.5, 12])

print(features.shape)   # Output: (6,)
print(features.dtype)   # Output: float64
```

---

### Key Properties Breakdown

#### 1. The Shape Property: `(6,)`
* **What it means:** The trailing comma with nothing after it indicates a purely **1D vector** with exactly 6 elements.
* **Visual Structure:** It is a single horizontal row of data sequences.
```text
Index:     0    1    2   3    4    5
          ┌───┬───┬─────┬───┬─────┬────┐
features: │ 0 │ 1 │ 234 │ 0 │ 0.5 │ 12 │
          └───┴───┴─────┴───┴─────┴────┘
```

#### 2. The Data Type Property: `float64`
* **What it means:** All elements inside this array are stored as 64-bit floating-point decimal numbers.
* **Why did it become float64?** NumPy arrays have a strict rule: **all elements must share the exact same data type**. Even though numbers like `0`, `1`, and `234` are integers, the presence of `0.5` forces NumPy to automatically upgrade (upcast) every integer in the array to a decimal to keep them uniform.
* **Actual underlying memory values:**
  `array([0.0, 1.0, 234.0, 0.0, 0.5, 12.0])`


### The array we used was a **made-up teaching example**, not a real packet. 
 
```python
np.array([0, 1, 234, 0, 0.5, 12])
```
Six values, no labels. Meaningless without context. Let's replace it with something grounded.

SO making it real. Here's what a meaningful 1D array representing one NSL-KDD connection record actually looks like, mapped to real fields:

## A real NSL-KDD row — 6 selected features

NSL-KDD has 41 features per connection. Here are 6 that matter most for your thesis, with real values from a **normal HTTP connection**:

```python
# [duration, protocol_type, src_bytes, logged_in, serror_rate, dst_host_count]
np.array([0, 1, 234, 1, 0.0, 12])
```

| Index | Feature name | Value | What it means |
|---|---|---|---|
| `[0]` | `duration` | `0` | Connection lasted 0 seconds — typical for a quick HTTP GET request. Most normal TCP connections are 0 (sub-second). |
| `[1]` | `protocol_type` | `1` | Encoded protocol. After `LabelEncoder`: `0=icmp`, `1=tcp`, `2=udp`. So `1` = TCP. |
| `[2]` | `src_bytes` | `234` | 234 bytes sent from source to destination. Consistent with a small HTTP request header. |
| `[3]` | `logged_in` | `1` | Successful login detected in this connection. `1=yes`, `0=no`. |
| `[4]` | `serror_rate` | `0.0` | 0% of connections to this host had SYN errors. A SYN flood attack would push this toward `1.0`. |
| `[5]` | `dst_host_count` | `12` | This destination host has been contacted 12 times in the recent window. Low = normal. High = scanning. |

So the full array says: **a sub-second TCP connection, 234 bytes sent, user was logged in, no SYN errors, destination contacted 12 times recently.** That's a normal authenticated HTTP session.

---

## Now watch what a DoS attack looks like

```python
# Same 6 features, same order — DoS (SYN flood)
np.array([0, 1, 0, 0, 1.0, 511])
```

| Index | Feature | Value | What changed |
|---|---|---|---|
| `[0]` | `duration` | `0` | Still 0 — connections never complete, they're dropped |
| `[1]` | `protocol_type` | `1` | Still TCP |
| `[2]` | `src_bytes` | `0` | **Zero bytes** — SYN packets sent but no data, connection never established |
| `[3]` | `logged_in` | `0` | **Not logged in** — connection never completed the handshake |
| `[4]` | `serror_rate` | `1.0` | **100% SYN error rate** — every connection attempt failed at SYN stage |
| `[5]` | `dst_host_count` | `511` | **511 recent connections to this host** — the attack is hammering it |

Two arrays, same structure. The values tell completely different stories.

---

# II - NumPy 2D Array Slicing Visual Guide

Given the following 2D array:
```python
import numpy as np

data = np.array([,
    [0, 1, 234, 0],
    [1, 0,  10, 1],
    [0, 0,   5, 0],
])
# data.shape is (3, 4) -> 3 rows, 4 columns
```

---

### 1. `data[0]` (Select Row 0)
Extracts the first row of the matrix.

**Visual Selection:**
```text
  Col 0  Col 1  Col 2  Col 3
 ┌───────────────────────────┐
 │ [ 0,     1,   234,     0 ]│  <-- Row 0 (Selected)
 │   1,     0,    10,     1  │  <-- Row 1
 │   0,     0,     5,     0  │  <-- Row 2
 └───────────────────────────┘
```
* **Returns:** `array([0, 1, 234, 0])`
* **Resulting Shape:** `(4,)` *(collapses into a 1D array)*

---

### 2. `data[:, 2]` (Select Column 2)
The `:` means "all rows". The `2` means "only column index 2".

**Visual Selection:**
```text
  Col 0  Col 1  Col 2  Col 3
               ┌─────┐
 ┌─────────────│─────│───────┐
 │   0,     1, │ 234 │,    0 │  <-- Row 0
 │   1,     0, │  10 │,    1 │  <-- Row 1
 │   0,     0, │   5 │,    0 │  <-- Row 2
 └─────────────│─────│───────┘
               └─────┘
               Selected
```
* **Returns:** `array([234, 10, 5])`
* **Resulting Shape:** `(3,)` *(collapses into a flat 1D array)*

---

### 3. `data[:, -1]` (Select Last Column)
The `-1` index wraps around to the very last column on the right.

**Visual Selection:**
```text
  Col 0  Col 1  Col 2  Col 3
                      ┌─────┐
 ┌────────────────────│─────│┐
 │   0,     1,   234, │  0  ││  <-- Row 0
 │   1,     0,    10, │  1  ││  <-- Row 1
 │   0,     0,     5, │  0  ││  <-- Row 2
 └────────────────────│─────│┘
                      └─────┘
                      Selected
```
* **Returns:** `array([0, 1, 0])`
* **Resulting Shape:** `(3,)`

---

### 4. `data[0:2, 0:3]` (Select a Submatrix)
Python slicing ranges are **exclusive** at the end (`start:stop` does not include `stop`).
* `0:2` selects rows `0` and `1` *(excludes row 2)*.
* `0:3` selects columns `0`, `1`, and `2` *(excludes column 3)*.

**Visual Selection:**
```text
    Col 0  Col 1  Col 2    Col 3
  ┌───────────────────┐
┌─│───────────────────│─────────┐
│ │   0,     1,   234 │,    0   │  <-- Row 0
│ │   1,     0,    10 │,    1   │  <-- Row 1
└─│───────────────────│─────────┘
  │   0,     0,     5 │,    0        <-- Row 2
  └───────────────────┘
        Selected
```
* **Returns:**
  ```python
  array([[  0,   1, 234],
         [  1,   0,  10]])
  ```
* **Resulting Shape:** `(2, 3)` *(retains 2D structure because range slicing was used on both axes)*

---
# NumPy Filtering: Boolean Masking

Given our previous array!

### Step 1: `mask = data[:, 1] == 1`
This looks at **Column 1** across **all rows**, and checks if the value equals `1`. It returns a 1D array of Booleans (`True` or `False`).

**Visual Selection:**
```text
  Col 0  Col 1  Col 2  Col 3
        ┌─────┐
 ┌──────│─────│──────────────┐
 │   0, │  1  │,  234,     0 │  --> 1 == 1  --> True
 │   1, │  0  │,   10,     1 │  --> 0 == 1  --> False
 │   0, │  0  │,    5,     0 │  --> 0 == 1  --> False
 └──────│─────│──────────────┘
        └─────┘
```
* **Returns:** `array([ True, False, False])`

---

### Step 2: `data[mask]`
NumPy applies this mask back to the original array. It keeps rows where the mask is `True` and discards rows where it is `False`.

**Visual Selection:**
```text
  Mask    Data Rows
 ┌──────┐┌───────────────────────────┐
 │ True ││  0,     1,   234,     0   │  <-- Kept
 │False ││   1,     0,    10,     1  │  <-- Filtered out
 │False ││   0,     0,     5,     0  │  <-- Filtered out
 └──────┘└───────────────────────────┘
```

* **Returns:** 
  ```python
  array([[  0,   1, 234,   0]])
  ```
* **Resulting Shape:** `(1, 4)` *(retains 2D structure because it returns full rows)*

---
# Real-World Filtering: Splitting Datasets by Class Labels

This technique maps a separate 1D array of labels directly to the rows of your feature matrix (`data` or `X`).

Given our previous array and a matching list of labels for each row!
```python

labels = np.array(['normal', 'dos', 'normal']) # Shape (3,)
```
---

### Step 1: Evaluating `labels == 'dos'`
NumPy checks every element in the `labels` array. It creates a boolean mask of the exact same length.

**Visual Mapping:**
```text
 Row 0: 'normal' == 'dos'  --> False
 Row 1: 'dos'    == 'dos'  --> True
 Row 2: 'normal' == 'dos'  --> False
```
* **Mask Generated:** `array([False,  True, False])`

---

### Step 2: Extracting `dos_rows = data[labels == 'dos']`
NumPy pairs the mask up with the rows of `data`. It extracts only the rows that line up with `True`.

**Visual Selection:**
```text
  Mask    Data Rows
 ┌──────┐┌───────────────────────────┐
 │False ││   0,     1,   234,     0  │  <-- Dropped
 │ True ││   1,     0,    10,     1  │  <-- KEPT!
 │False ││   0,     0,     5,     0  │  <-- Dropped
 └──────┘└───────────────────────────┘
```

* **What `dos_rows` contains:**
  ```python
  array([ 1, 0, 10, 1])
  ```
* **Shape:** `(1, 4)`

---

### Machine Learning Context (Week 4 Prep)
When separating data for training individual models (e.g., a dedicated DoS detector vs. a Probe detector):

```python
# Separate entire feature matrices by attack class
X_dos    = X[labels == 'dos']     # Extracts only DoS traffic features
X_probe  = X[labels == 'probe']   # Extracts only Probing traffic features
X_normal = X[labels == 'normal']  # Extracts only Benign traffic features
```
* **Rule of Thumb:** The length of your `labels` array must exactly match the number of rows in your `X` matrix, or NumPy will throw a `ValueError`.
---
# Feature Scaling: Min-Max Normalization

This formula scales any numerical column so all values fall strictly between `0.0` and `1.0`.

Given your column array:
```python
import numpy as np

col = np.array([0, 234, 10, 5, 512])
```
---
### Step 1: Find the Minimum and Maximum
```python
col_min, col_max = col.min(), col.max()
# col_min = 0
# col_max = 512
```

---

### Step 2: The Normalization Math
NumPy uses **broadcasting** to apply the formula `(x - min) / (max - min)` to every single element at the same time:

1. **`col - col_min`** (Shift the baseline to 0):
   * `[0-0, 234-0, 10-0, 5-0, 512-0]` \(\rightarrow\) `[0, 234, 10, 5, 512]`

2. **`col_max - col_min`** (Find the total range):
   * `512 - 0` \(\rightarrow\) `512`

3. **Divide by the range** (Scale down to 0-1):
   * `[0/512, 234/512, 10/512, 5/512, 512/512]`

---

### Visual Mapping of the Result
* The absolute lowest value (`0`) becomes exactly **`0.0`**.
* The absolute highest value (`512`) becomes exactly **`1.0`**.
* All other numbers become a proportional decimal between them.

```python
print(normalized)
# Output: array([0.        , 0.45703125, 0.01953125, 0.00976562, 1.        ])
```

| Original Value | Math Expression | Normalized Value | Meaning |
| :--- | :--- | :--- | :--- |
| **0** | `0 / 512` | **`0.0`** | Absolute Minimum |
| **5** | `5 / 512` | **`0.00976562`** | Very close to min |
| **10** | `10 / 512` | **`0.01953125`** | Slightly above min |
| **234** | `234 / 512` | **`0.45703125`** | Roughly halfway |
| **512** | `512 / 512` | **`1.0`** | Absolute Maximum |

---
# Malware Data Preprocessing: Reshaping, Normalization, & Axis Aggregations

This section covers converting raw malware binary bytes into grayscale images (like the MalImg dataset pipeline) and performing axis-based feature calculations.

---

## 1. Binary Image Normalization
When converting bytes into image pixels, data must be scaled from the standard 8-bit range `[0, 255]` down to a floating-point range `[0.0, 1.0]`. This stabilizes gradient calculations in Neural Networks.

```python
import numpy as np

# Original raw byte stream
image_bytes = np.array([0, 128, 255, 64, 200], dtype=np.uint8)

# Scale by the maximum possible pixel value
normalized_image = image_bytes / 255.0
# Returns: array([0.0, 0.50196078, 1.0, 0.25098039, 0.78431373])
```

---

## 2. Reshaping: Turning a Byte Stream into an Image
Malware visualization pipelines treat raw executables (`.exe`, `.bin`) as sequential arrays of bytes and wrap them into a 2D matrix (image) where each byte becomes a single pixel.

### Simple Shape Simulation (32 × 32 Matrix)
```python
# Simulate reading 1024 raw bytes from a malware sample
binary_data = np.random.randint(0, 256, size=1024, dtype=np.uint8)

# Wrap the continuous 1D stream of 1024 bytes into a 32x32 2D grid
image = binary_data.reshape(32, 32)
print(image.shape)  # Output: (32, 32)
```

### Production Pipeline Breakdown (MalImg Standards)
In actual malware research, images are typically fixed to a strict width (e.g., 256 pixels wide), while the height varies depending on how large the executable file is.

```python
# 1. Read file as a raw array of 8-bit unsigned integers
file_bytes = np.frombuffer(open('sample.exe', 'rb').read(), dtype=np.uint8)

# 2. Trim off any remainder bytes that won't cleanly fit into rows of 256
trimmed_bytes = file_bytes[:len(file_bytes) - len(file_bytes) % 256]

# 3. Reshape using -1 (tells NumPy to calculate the required height automatically)
image = trimmed_bytes.reshape(-1, 256)
```

**Visual Concept:**
```text
Raw 1D bytes: [ B1, B2, B3, B4, B5, B6, B7, B8, B9, B10, ... ]
                     ↓ .reshape(-1, 4)
2D Matrix:   ┌───────────────────┐
      Row 0  │ B1   B2   B3   B4 │
      Row 1  │ B5   B6   B7   B8 │
      Row 2  │ B9  B10  ...      │
             └───────────────────┘
```

---

## 3. Axis Operations: Aggregating Across Rows vs. Columns
When dealing with matrices, operations like `.mean()`, `.sum()`, and `.max()` require an `axis` argument to specify the direction of the calculation.

```python
# Features Matrix Example (Rows = Network Samples, Columns = Extracted Features)
data = np.array([,  # Sample 0,  # Sample 1
    [80,  10, 0]   # Sample 2
])
```

### 🔹 `axis=0` (Vertical Operation — Column-by-Column)
Collapses the rows downward. Use this to find statistics for specific **features** across your entire dataset.
```text
Matrix Structure:
Col 0   Col 1   Col 2
[ 10,    200,     0 ],  <- Row 0
[  5,    150,     1 ],  <- Row 1
[ 80,     10,     0 ]   <- Row 2
```

### Axis=0 Calculation Breakdown
```text
       Col 0      Col 1      Col 2
     ┌──────────┬──────────┬──────────┐
     │    10    │   200    │    0     │
     │     5    │   150    │    1     │
     │    80    │    10    │    0     │
     └────┬─────┴────┬─────┴────┬─────┘
          ↓          ↓          ↓
Calculates downwards for each feature column

Math Mechanics:
1. sum(axis=0)  -> [ (10+5+80),   (200+150+10),  (0+1+0) ]   -> [95, 360, 1]
2. mean(axis=0) -> [ (95 / 3),     (360 / 3),     (1 / 3) ]   -> [31.66, 120.0, 0.33]
3. max(axis=0)  -> [ max(10,5,80), max(200,150,10), max(0,1,0) ] -> [80, 200, 1]
```
* **`data.mean(axis=0)`** \(\rightarrow\) `[31.66, 120.0, 0.33]` *(Average value of each feature)*
* **`data.sum(axis=0)`** \(\rightarrow\) `[95, 360, 1]` *(Total accumulated weight of each feature)*
* **`data.max(axis=0)`** \(\rightarrow\) `[80, 200, 1]` *(Max bounds per feature; useful for feature importance evaluations)*

### 🔸 `axis=1` (Horizontal Operation — Row-by-Row)
Collapses the columns sideways. Use this to calculate metrics per individual **sample**.
# Axis=1 Calculation Breakdown
```text
               ┌──────────┬──────────┬──────────┐
      Sample 0 │    10    │   200    │    0     │ ──> Calculates sideways across features
      Sample 1 │     5    │   150    │    1     │ ──> Calculates sideways across features
      Sample 2 │    80    │    10    │    0     │ ──> Calculates sideways across features
               └──────────┴──────────┴──────────┘
Math Mechanics:
1. sum(axis=1)  -> [ (10+200+0),   (5+150+1),   (80+10+0) ]   -> [210, 156, 90]
2. mean(axis=1) -> [ (210 / 3),    (156 / 3),   (90 / 3)  ]   -> [70.0, 52.0, 30.0]
3. max(axis=1)  -> [ max(10,200,0), max(5,150,1), max(80,10,0) ] -> [200, 150, 80]

```
* **`data.mean(axis=1)`** \(\rightarrow\) `[70.0, 52.0, 30.0]` *(Average feature value of Sample 0, Sample 1, and Sample 2)*
 
---
# Standard Deviation (std)

standard deviation measures how spread out or how varied your numbers are.

* A low standard deviation means the numbers are all very close to the average (mean).
* A high standard deviation means the numbers are spread far apart, ranging from very small to very large. 

When you run data.std(axis=0), NumPy calculates this variance vertically, column-by-column (feature-by-feature). 

## A Cybersecurity Example
Let's look at your matrix columns to see why this is useful for detecting malware or network attacks:
```
data = np.array([,  # Packet 0
                 ,  # Packet 1
                 ]) # Packet 2
```
## Column 2: Protocol Type (Values: 0, 1, 0)

* All numbers are very similar and close together (0 or 1).
* data.std(axis=0)[2] will be a low number (0.47).
* Meaning: This feature is highly stable and consistent. [12, 13] 

## Column 1: Packet Size (Values: 200, 150, 10)

* The numbers are wildly spread out. One packet is tiny (10), and another is massive (200).
* data.std(axis=0)[1] will be a high number (81.65).
* Meaning: This feature has huge variations. It tells your machine learning model that traffic size fluctuates violently. 

```
print(data.std(axis=0))
# Output: [34.359, 81.649, 0.471]
```
### Visual Breakdown of the Output:
* **Col 0 Std (`34.359`):** Moderate spread between the values 10, 5, and 80.
* **Col 1 Std (`81.649`):** High spread. The values (200, 150, 10) are far apart from each other.
* **Col 2 Std (`0.471`):** Low spread. The values (0, 1, 0) are highly uniform and tightly clustered.

# Mathematical Steps for Standard Deviation (std)

Formula Overview:
1. Find Mean (μ)
2. Subtract Mean from each number (x - μ)
3. Square the results (x - μ)²
4. Find the average of those squares (Variance)
5. Take the Square Root of the Variance

### Example with data: [10, 5, 80]

| Number ($x$) | Distance ($x - \text{Mean}$) | Squared Distance ($x - \text{Mean}$)^2 |
| :--- | :--- | :--- |
| **10** | $10 - 31.67 = -21.67$ | $(-21.67)^2 = \mathbf{469.59}$ |
| **5** | $5 - 31.67 = -26.67$ | $(-26.67)^2 = \mathbf{711.29}$ |
| **80** | $80 - 31.67 = 48.33$ | $(48.33)^2 = \mathbf{2335.79}$ |

* **Sum of Squares:** $469.59 + 711.29 + 2335.79 = 3516.67$
* **Variance:** $3516.67 / 3 = 1172.22$
* **Standard Deviation ($\sigma$):** $\sqrt{1172.22} = \mathbf{34.24}$

---

# When you'll use each:

| Operation | Axis | When |
|---|---|---|
| Mean per feature | 0 | Checking if a feature has useful variance |
| Std per feature | 0 | Finding constant/useless features before training |
| Mean per sample | 1 | Anomaly scoring (how unusual is this one packet?) |
| Max per feature | 0 | Feature importance sanity check |Notice feature 2 has std `0.47` — it's almost always 0 with one 1. In NSL-KDD, features like `urgent` (number of urgent packets) are nearly always zero. Low variance features add noise without signal — `std(axis=0)` lets you identify and drop them before training.

---

## The full picture — where each concept lands in your thesis

| NumPy concept | Where it appears in your pipeline |
|---|---|
| `np.array`, `dtype` | Loading any dataset row; dtype errors are the #1 PyTorch bug |
| `shape` | Debugging every array throughout — first thing you check when something breaks |
| Slicing `[:, col]` | Extracting individual NSL-KDD features for plotting and analysis |
| Boolean mask | Filtering by attack class; selecting misclassified samples for error analysis |
| Broadcasting + normalize | MinMaxScaler internals; pixel normalization before CNN input |
| `reshape(-1, 256)` | The first line of your MalImg binary visualization function |
| `mean/std(axis=0)` | Feature variance analysis; identifying low-signal features to drop |

