"""
Create a program that reads the text file "raw_text.txt", encrypts its contents using a
simple encryption method, and writes the encrypted text to a new file
"encrypted_text.txt". Then create a function to decrypt the content and a function to
verify the decryption was successful.

Requirements
The encryption should take two user inputs (shift1, shift2), and follow these rules:
 • For lowercase letters:
        o If the letter is in the first half of the alphabet (a-m): shift forward by shift1 * shift2 positions
        o If the letter is in the second half (n-z): shift backward by shift1 + shift2 positions
    • For uppercase letters:
        o If the letter is in the first half (A-M): shift backward by shift1 positions
        o If the letter is in the second half (N-Z): shift forward by shift2² positions (shift2 squared)
    • Other characters:
        o Spaces, tabs, newlines, special characters, and numbers remain unchanged

Main Functions to Implement
Encryption function: Reads from "raw_text.txt" and writes encrypted content to "encrypted_text.txt".
Decryption function: Reads from "encrypted_text.txt" and writes the decrypted content to "decrypted_text.txt".
Verification function: Compares "raw_text.txt" with "decrypted_text.txt" and prints whether the decryption was successful or not.

Program Behavior
When run, your program should automatically:
    1. Prompt the user for shift1 and shift2 values
    2. Encrypt the contents of "raw_text.txt"
    3. Decrypt the encrypted file
    4. Verify the decryption matches the original
"""


# Transforms a single character using a shift and starting alphabet
def transform_char(shift, char, start_char):
    new_ord = ord(char) - ord(start_char)
    new_char = chr((new_ord + shift) % 13 + ord(start_char))
    return new_char


# Encryots the contents of raw_text.txt and writes to encrypted_text.txt
# Apply shift transformations depending on the position of the letter
def encryption(shift1, shift2):
    try:
        with open("raw_text.txt", "r") as file:
            raw_text = file.read()
        encrypted_text = []
        for char in raw_text:
            if "a" <= char <= "m":
                new_char = transform_char(shift1 * shift2, char, "a")
            elif "n" <= char <= "z":
                new_char = transform_char(-(shift1 + shift2), char, "n")
            elif "A" <= char <= "M":
                new_char = transform_char(-shift1, char, "A")
            elif "N" <= char <= "Z":
                new_char = transform_char(shift2**2, char, "N")
            else:
                new_char = char
            encrypted_text.append(new_char)
        with open("encrypted_text.txt", "w") as file:
            file.write("".join(encrypted_text))
    except FileNotFoundError:
        print("File not found.")


# Decrypts the contents of encrypted_text.txt  and writes to decrypted_text.txt
# Applies the inverse shift transformations
def decryption(shift1, shift2):
    try:
        with open("encrypted_text.txt", "r") as file:
            encrypted_text = file.read()
        decrypted_text = []
        for char in encrypted_text:
            if "a" <= char <= "m":
                new_char = transform_char(-(shift1 * shift2), char, "a")
            elif "n" <= char <= "z":
                new_char = transform_char(shift1 + shift2, char, "n")
            elif "A" <= char <= "M":
                new_char = transform_char(shift1, char, "A")
            elif "N" <= char <= "Z":
                new_char = transform_char(-(shift2**2), char, "N")
            else:
                new_char = char
            decrypted_text.append(new_char)
        with open("decrypted_text.txt", "w") as file:
            file.write("".join(decrypted_text))
    except FileNotFoundError:
        print("File not found.")


# Verifies that the contents of decrypted_text.txt and raw_text.txt are the same
def verify_decryption():
    try:
        with open("decrypted_text.txt", "r") as file:
            decrypted_text = file.read()
        with open("raw_text.txt", "r") as file:
            raw_text = file.read()

        if raw_text == decrypted_text:
            print("\n\nDecryption successful: The decrypted text matches the original.")
        else:
            print(
                "\n\nDecryption failed: The decrypted text does not match the original."
            )
    except FileNotFoundError:
        print("File not found.")


# Get user inputs for shifts
shift1 = int(input("Enter shift1 value: "))
shift2 = int(input("Enter shift2 value: "))

# Encrypt the raw text
encryption(shift1, shift2)

# Decrypt the encrypted text
decryption(shift1, shift2)

# Verify the decryption
verify_decryption()
