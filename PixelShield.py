import os
import numpy as np
from PIL import Image
import hashlib

# Clear the terminal
def clear_screen():
    """Clear the terminal screen."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
clear_screen()

# Check if the file exists
def file_exists(filepath):
    """Check if a file exists."""
    return os.path.isfile(filepath)

def key_generator(encryption_key):
    """Generate a list of keys derived from the encryption key."""
    l = []
    divisor = 2  # Default divisor is 2 if no other divisor is found

    # Find a divisor in the range 2 to 9
    for i in range(2, 10):
        if encryption_key % i == 0:
            divisor = i
            break  # Stop at the first divisor found

    key = encryption_key / divisor
    while key > 1:
        l.append(int(key))  # Ensure the key is an integer
        key = key / divisor
    return l

# Function for encryption
def image_encrypter(image_path, output_path, encryption_key):
    """Encrypt the image by shuffling its pixels based on a generated key list."""
    try:
        with Image.open(image_path) as image:
            image_array = np.array(image)
    except Exception as e:
        print(f"Error opening image: {e}")
        return
    # Get image dimensions
    height, width, channels = image_array.shape
    # Flatten the image array for shuffling
    flat_pixels = image_array.reshape(-1, channels)
    # Generate keys using the encryption key
    keys = key_generator(encryption_key)
    # Shuffle pixels using each key
    for key in keys:
        np.random.seed(key)  # Seed with integer part of the key
        np.random.shuffle(flat_pixels)
    # Reshape the shuffled pixels back into the original image dimensions
    encrypted_image = flat_pixels.reshape(height, width, channels)
    # Save the encrypted image
    encrypted_img = Image.fromarray(encrypted_image.astype(np.uint8))  # Ensure correct data type
    encrypted_img.save(output_path)
    print(f"Encrypted image saved as {output_path}")

# Hashing function for image
def hashage_calculator(image_path):
    """Calculate the hash of an image to generate a key."""
    try:
        with Image.open(image_path) as image:
            image_array = np.array(image)
            image_bytes = image_array.tobytes()
    except Exception as e:
        return f"Error opening image: {e}"

    # Calculate SHA-512 hash
    image_hash = hashlib.sha512(image_bytes).hexdigest()
    return image_hash

# Convert hash to integer key
def convert_hash(image_hash):
    """Convert the first 8 characters of the hash into an integer."""
    return int(image_hash[:8], 16)

# Function for decryption
def image_decrypter(image_path, output_path, encryption_key):
    """Decrypt the image by reversing the pixel shuffling process."""
    try:
        with Image.open(image_path) as encrypted_image:
            encrypted_image_array = np.array(encrypted_image)
    except Exception as e:
        print(f"Error opening encrypted image: {e}")
        return

    # Get image dimensions
    height, width, channels = encrypted_image_array.shape

    # Flatten the image array for reordering
    flat_pixels = encrypted_image_array.reshape(-1, channels)

    # Generate keys using the encryption key, and reverse the order for decryption
    keys = key_generator(encryption_key)[::-1]

    # Reverse shuffle pixels using each key
    for key in keys:
        np.random.seed(key)
        original_indices = np.random.permutation(len(flat_pixels))

        # Initialize an array to hold the decrypted pixels
        decrypted_pixels = np.zeros_like(flat_pixels)

        # Reverse the shuffle by placing pixels back in their original positions
        decrypted_pixels[original_indices] = flat_pixels

        # Update flat_pixels with decrypted_pixels for the next iteration
        flat_pixels = decrypted_pixels

    # Reshape the decrypted pixels back into the original image dimensions
    decrypted_image = flat_pixels.reshape(height, width, channels)

    # Save the decrypted image
    decrypted_img = Image.fromarray(decrypted_image.astype(np.uint8))  # Ensure correct data type
    decrypted_img.save(output_path)

    print(f"Decrypted image saved as {output_path}")

# Main function
def main():
    print("Welcome, this program is a simple tool to encrypt and decrypt images.\n")
    while True:
        choice = input("Insert (1) to encrypt, or (2) to decrypt: ")
        print("\n")
        if choice in ['1', '2']:
            break
        else:
            print("Please enter a valid option (1 or 2).\n")

    if choice == '1':
        while True:
            image_path = input("Please enter your image's path: ")
            if file_exists(image_path):
                break
            else:
                print("File not found. Please enter a valid path.\n")

        # Generate encryption key from hash
        image_hash = hashage_calculator(image_path)
        encryption_key = convert_hash(image_hash)
        
        output_path = input("Please enter the path where your encrypted image will be saved: ")
    
        image_encrypter(image_path, output_path, encryption_key)

        print("Encryption completed successfully!")
        print(f"Encryption Key (copy this): {encryption_key}\n")

    elif choice == '2':
        while True:
            image_path = input("Please enter your encrypted image's path: ")
            if file_exists(image_path):
                break
            else:
                print("File not found. Please enter a valid path.\n")

        output_path = input("Please enter the path where your decrypted image will be saved: ")
        encryption_key_str = input("Please enter the encryption key: ")
        
        image_decrypter(image_path, output_path, int(encryption_key_str))

        print("Decryption completed successfully!")

if __name__ == "__main__":
    main()
