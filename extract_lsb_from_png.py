from PIL import Image
import os.path

def extract_lsb_data(image_path, target_channels, num_lsb):
    """
    Extracts data hidden using LSB steganography from the specified RGBA channels.

    Parameters:
        image_path (str): Path to the input image.
        target_channels (str): Target color channels (e.g., "RGBA").
        num_lsb (int): Number of least significant bits to extract.

    Returns:
        str: The extracted binary data as a string.
    """
    if num_lsb <= 0 or num_lsb > 8:
        raise ValueError("Number of least significant bits must be between 1 and 8.")

    # Open the image
    try:
        img = Image.open(image_path)
        img = img.convert("RGBA")
    except Exception as e:
        raise IOError(f"Error opening image: {e}")

    pixels = img.load()
    width, height = img.size

    # Accumulates the hidden binary data from all specified channels of all pixels
    binary_data = ""

    # Iterate over every pixel
    for y in range(height):
        for x in range(width):
            # Access the color values of the pixel at coordinates (x, y)
            r, g, b, a = pixels[x, y]
            # Create a dictionary to map channel names ("R", "G", "B", "A") to their corresponding pixel values (r, g, b, a)
            channels = {"R": r, "G": g, "B": b, "A": a}

            for channel in target_channels:
                if channel in channels:
                    # Check and process only the channels specified in target_channels
                    value = channels[channel]
                    # Convert the hex values to binary then extract the specified least significant bits
                    binary_data += f"{value:08b}"[-num_lsb:]

    return binary_data

def binary_to_text(binary_data):
    """
    Converts binary data to text by grouping bits into bytes and decoding.

    Parameters:
        binary_data (str): The binary data as a string.

    Returns:
        str: The decoded text.
    """
    chars = []
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if len(byte) == 8:
            chars.append(chr(int(byte, 2)))
    return "".join(chars)

if __name__ == "__main__":
    try:
        image_path = input("Enter the path to the image: ")
        target_channels = input("Enter the target color channels (e.g., RGBA): ").upper()
        num_lsb = int(input("Enter the number of least significant bits to extract: "))

        image_path = os.path.abspath(image_path)

        if not os.path.exists(image_path):
            print(f"Error: The file does not exist at the given path: {image_path}")
        else:
            print(f"Validated path: {image_path}")

        binary_data = extract_lsb_data(image_path, target_channels, num_lsb)
        extracted_text = binary_to_text(binary_data)

        print("\nExtracted Data:")
        print(extracted_text)
    except Exception as e:
        print(f"Error: {e}")
