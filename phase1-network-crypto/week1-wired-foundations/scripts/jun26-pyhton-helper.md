# NumPy 2D Array Slicing Visual Guide

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


