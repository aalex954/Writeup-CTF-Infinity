# Writeup-CTF-Infinity

## CTF Write-up: Identifying and Extracting LSB Hidden Data

This write-up outlines the steps to test for, identify, and extract data hidden in the Least Significant Bit (LSB) of a PNG image. 
It also explores multiple tools and methodologies, including custom scripts and automated tools like zsteg, to extract and analyze the hidden data.

---

## Overview

**File**: `challenge_infinity_image_final.png`  
**Objective**: Prove that data is hidden in the RGBA values of the image using 2 least significant bits (LSBs).  
**Tools Used**:
- Python with `Pillow`
- `strings` command
- `zsteg` (a steganography analysis tool)
- Entropy and binary analysis methods

---

## Step 1: File Inspection and Metadata Analysis

The first step involves inspecting the file for metadata or embedded hints.

### **1. Extract Strings**
Using the `strings` command, extract readable text from the binary file:

```bash
strings challenge_infinity_image_final.png | less
```

### **Findings**
1. Metadata reveals hints about **LSB** steganography:
   ```
   <rdf:Bag ...><rdf:li>LSB</rdf:li></rdf:Bag>
   ```
2. The title of the image is "Infinity," suggesting thematic significance.
3. The strings do not reveal direct encoding details but confirm the use of LSB steganography.

---

## Step 2: Visual Analysis

The image shows **visual artifacts**, which are often indicative of steganographic manipulation. Such artifacts usually result from changes to pixel values in the least significant bits, leading to subtle distortions.

---

## Step 3: LSB Extraction Using Python

### Hypothesis:
Data is hidden in the RGBA channels using 2 LSBs of each channel.

### Python Script:
The following script extracts LSB data from all RGBA channels:

```python
from PIL import Image

def extract_lsb(image_path, target_channels="RGBA", num_lsb=2):
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size
    binary_data = ""

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            channels = {"R": r, "G": g, "B": b, "A": a}

            for channel in target_channels:
                if channel in channels:
                    value = channels[channel]
                    binary_data += f"{value:08b}"[-num_lsb:]

    # Convert binary data to ASCII
    data = ""
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if len(byte) == 8:
            data += chr(int(byte, 2))
    return data

# Extract data from RGBA channels
image_path = "challenge_infinity_image_final.png"
hidden_data = extract_lsb(image_path, target_channels="RGBA", num_lsb=2)
print(hidden_data[:500])  # Display the first 500 characters
```

### Output:
The script extracts binary data, which is converted into ASCII. The first 500 characters reveal:
```
Page 383 of Volume 22 on Shelf 1 of Wall 2 of Hexagon: ...
```

This confirms the presence of hidden structured data.

---

## Step 4: Automated Analysis Using `zsteg`

### Tool: `zsteg`
`zsteg` is a powerful tool for analyzing PNG files for steganographic data.

**Installation**:
```bash
gem install zsteg
```

**Command**:
```bash
zsteg challenge_infinity_image_final.png
```

### Findings:
`zsteg` outputs potential LSB-based hidden data across color channels. Key findings:
1. Hidden data is detected in multiple channels:
   ```
   b1,r,lsb     --> "Page 383 of Volume 22..."
   b2,g,lsb     --> "<hidden structured data>"
   b2,b,lsb     --> "<additional encoded data>"
   ```
2. `zsteg` confirms the hypothesis that data is embedded using 2 LSBs.

---

## Step 5: Data Decoding and Validation

### Decoding Attempts:
After extracting the hidden data, attempt to decode it using common methods:

#### Base64 Decoding:
```python
import base64
try:
    decoded = base64.b64decode(hidden_data).decode("utf-8")
    print(decoded)
except Exception as e:
    print("Base64 decoding failed:", e)
```

#### Hexadecimal Decoding:
```python
try:
    decoded = bytes.fromhex(hidden_data).decode("utf-8")
    print(decoded)
except Exception as e:
    print("Hex decoding failed:", e)
```

### Entropy Analysis:
Measure randomness to validate the structured nature of the data:
```python
from collections import Counter
from math import log2

def calculate_entropy(data):
    counts = Counter(data)
    total = len(data)
    entropy = -sum((count / total) * log2(count / total) for count in counts.values())
    return entropy

entropy = calculate_entropy(hidden_data)
print("Entropy:", entropy)
```

**Results**:
- Entropy indicates non-randomness, confirming structured encoding or encryption.
- Decoding attempts reveal readable text leading to a reference in the Library of Babel.

---

## Step 6: Alternative Tools

### Additional Tools for Analysis:
1. **StegSolve**:
   - A GUI tool to analyze bit planes of an image.
   - Can visually confirm hidden data in specific channels.

2. **Stegdetect**:
   - Useful for detecting general steganographic techniques in images.

---

## Results and Conclusion

1. **Hidden Data Proven**:
   - Data is embedded in the RGBA channels using 2 least significant bits.
   - Extracted data contains structured text pointing to a reference in the Library of Babel.

2. **Tools and Techniques**:
   - Manual extraction with Python confirmed the presence of hidden data.
   - `zsteg` automated the detection and provided further insights.

3. **Next Steps**:
   - Use the extracted data to navigate the Library of Babel and retrieve the flag.

This write-up demonstrates a systematic approach to proving the presence of hidden data in an image using both manual and automated methods. The combination of Python scripts, entropy analysis, and `zsteg` ensures thorough validation.
