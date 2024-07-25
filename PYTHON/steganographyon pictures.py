import cv2
import os

DELIMITER = '1111111111111110'

def text_to_binary(text):
    """Convert text to a binary string."""
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary):
    """Convert binary string to text."""
    binary_chunks = [binary[i:i+8] for i in range(0, len(binary), 8)]
    text = ''.join(chr(int(chunk, 2)) for chunk in binary_chunks)
    return text

def hide_text_in_image(image_path, text, output_image_path):
    """Hide text inside an image."""
    try:
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to load image at {image_path}. The file may not be a valid image.")
            return False

        binary_text = text_to_binary(text) + DELIMITER  # Delimiter to indicate end of text
        data_index = 0
        
        for row in image:
            for pixel in row:
                for channel in range(3):  # Iterate over R, G, B channels
                    if data_index < len(binary_text):
                        pixel[channel] = int(format(pixel[channel], '08b')[:-1] + binary_text[data_index], 2)
                        data_index += 1

        if data_index < len(binary_text):
            print("Warning: The text is too long to be hidden in the image.")
            return False

        cv2.imwrite(output_image_path, image)
        if os.name == 'nt':  # Check if the OS is Windows
            os.startfile(output_image_path)
        else:
            print(f"Image saved at {output_image_path}")
        print(f"Data hiding in image completed successfully and saved as {output_image_path}")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def extract_text_from_image(image_path):
    """Extract hidden text from an image."""
    try:
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to load image at {image_path}. The file may not be a valid image.")
            return None

        binary_text = ""
        for row in image:
            for pixel in row:
                for channel in range(3):  # Iterate over R, G, B channels
                    binary_text += format(pixel[channel], '08b')[-1]

        if DELIMITER in binary_text:
            binary_text = binary_text[:binary_text.index(DELIMITER)]
            text = binary_to_text(binary_text)
            print("Hidden text extracted: ", text)
            return text
        else:
            print("No hidden text found.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    """Main function to choose hide or extract mode."""
    mode = input("Enter 'h' to hide text or 'e' to extract text: ").lower().strip()
    if mode == 'h':
        image_path = input("Enter the path to the image: ").strip()
        if not os.path.isfile(image_path):
            print("Invalid file path. Please try again.")
            return
        text = input("Enter the text to hide: ").strip()
        output_image_path = input("Enter the output image file name (with extension, e.g., output.png): ").strip()
        success = hide_text_in_image(image_path, text, output_image_path)
        if success:
            print("Text successfully hidden in the image.")
        else:
            print("Failed to hide text in the image.")
    elif mode == 'e':
        image_path = input("Enter the path to the image: ").strip()
        if not os.path.isfile(image_path):
            print("Invalid file path. Please try again.")
            return
        text = extract_text_from_image(image_path)
        if text is not None:
            print("Text successfully extracted from the image.")
        else:
            print("Failed to extract text from the image.")
    else:
        print("Invalid mode. Please enter 'h' or 'e'.")

# Run the main function
if __name__ == "__main__":
    main()
