# Writeup-CTF-Infinity

  # CTF Write-up: Identifying and Extracting LSB Hidden Data

This write-up outlines the steps to test for, identify, and extract data hidden in the Least Significant Bit (LSB) of a PNG image. It also demonstrates how to reverse image search and use the extracted data to navigate the "Library of Babel" for further instructions.

---

## Step 1: Analyze the Image for Possible Steganography

### **Testing for Hidden Data**
When analyzing a file in a CTF scenario, suspect data may be hidden. Here’s how to begin testing:

1. **File Type Validation**
   - Use `file` (Linux/Mac) or `exiftool` to verify the file format.
     ```bash
     file challenge_infinity_image.png
     exiftool challenge_infinity_image.png
     ```

2. **Visual Inspection**
   - Open the image using a viewer to spot anomalies like artifacts, repetitive patterns, or seemingly unnecessary alpha transparency.

3. **Hex Inspection**
   - Examine the binary content using a hex editor like `hexedit` or `xxd`.
     ```bash
     xxd challenge_infinity_image.png | less
     ```
   - Look for unusual metadata, patterns, or chunks outside the PNG standard.

---

### **Identifying Hidden LSB Data**

If initial tests suggest no anomalies, assume the data is hidden in the image’s LSB. 

#### Tools to Test for LSB Steganography:
1. **`stegdetect`** (for automated detection)
   ```bash
   stegdetect challenge_infinity_image.png
   ```

2. **Stego Programs** (e.g., `zsteg` or `stegsolve`):
   - `zsteg` scans PNG images for steganographic content.
     ```bash
     zsteg challenge_infinity_image.png
     ```
   - `stegsolve` offers a GUI for analyzing different bit planes of the image.

3. **Extract Bit Planes for Analysis**
   Use Python and the `Pillow` library to isolate and analyze individual bits.
   ```python
   from PIL import Image
   img = Image.open("challenge_infinity_image.png")
   pixels = img.load()
   width, height = img.size
   lsb_image = Image.new("1", (width, height))
   lsb_pixels = lsb_image.load()

   for y in range(height):
       for x in range(width):
           r, g, b, a = pixels[x, y]
           lsb_pixels[x, y] = r & 1  # Extract the least significant bit
   lsb_image.show()
   ```

---

## Step 2: Extracting LSB Hidden Data

### Python Program for LSB Extraction
If data is confirmed in the LSB, extract it:

```python
from PIL import Image

def extract_lsb(image_path, target_channels="RGBA", num_lsb=1):
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

    # Group binary data into bytes
    data = ""
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if len(byte) == 8:
            data += chr(int(byte, 2))
    return data

hidden_data = extract_lsb("challenge_infinity_image.png", target_channels="RGB", num_lsb=2)
print("Hidden Data:", hidden_data)
```

### Example Output:
```plaintext
Hidden Data: Page 383 of Volume 22 on Shelf 1 of Wall 2 of Hexagon: 2kcw2ju6uxf3...
```

---

## Step 3: Reverse Image Search for Context

### Reverse Image Search
1. **Use Reverse Image Search Engines**:
   - **Google Reverse Image Search**: Drag and drop the image into [Google Images](https://images.google.com).
   - **Tineye**: [Tineye Reverse Image Search](https://www.tineye.com/).

2. **Identify References**:
   - Search results may reveal the image is tied to "The Library of Babel."

---

## Step 4: Use the Library of Babel

### Navigate the Library of Babel
The Library of Babel (https://libraryofbabel.info) is a fictional library containing all possible texts.

#### Steps:
1. Open the Library of Babel website.
2. Use the search functionality or direct hexagon navigation:
   - Enter `Page 383 of Volume 22 on Shelf 1 of Wall 2 of Hexagon` in the search field.
   - Input the hexagon code: `2kcw2ju6uxf3a4...`.

3. Read the instructions or clues within the page to proceed with the challenge.

---

## Common Pitfalls and Recommendations

1. **Image Analysis**:
   - If LSB tools fail, try other steganographic techniques (e.g., alternate bit planes, metadata).
2. **Extracting Data**:
   - Ensure the correct number of bits (`num_lsb`) matches the embedding method.
3. **Cross-referencing Context**:
   - If no clues are found, consider the context of the challenge for hints.

---

### Conclusion

By analyzing, testing, and extracting the hidden LSB data, we uncovered instructions leading to the Library of Babel. The extracted data was used to navigate the library and retrieve the instructions for the next stage. This process demonstrates a systematic approach to tackling steganographic challenges in CTFs.
