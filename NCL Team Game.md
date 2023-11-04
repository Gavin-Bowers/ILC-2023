## Crypto

### Salad

This is just a classic Vignere cypher. I can guess and check single letter keys. I can tell because the letters and numbers are preserved, but altered. Also it's too short for alphanumeric substitution

### Beep Beep

It's morse code. This one is easier than the first

### Someone Cooked

This one has binary which decodes to morse code, which decodes to decimal values
![[Pasted image 20231103142713.png]]

I found out this is octal because the 040 values are common at regular spacing and represent a space in octal. That gives us this hex:

53 63 6d 63 68 6d 63 63 63 53 69 48 68 47 67 54 26 44 23 46 56 14 27 14 56 46 06 43 c3 33 23 24 27 95 27 56 26 94 27 14 63 94 87 34 33 4f 41 47 44 57 37 62 41 47 47 4f 53 52 61 7d

Which I can't decode

There are apparently 7 encoding techniques, and I only have 3 of them. I'm stuck on figuring out what the hex decodes to. It creates invalid chars as ASCII, and I even tried running it through ciphers before decoding. It also isn't anything notewothy in decimal or valid as utf-8

### Roots

This one is a fun one. We must follow a set of move and draw instructions in order to draw the flag. This one could be done is Scratch, but I used the Python turtle library.

![[Pasted image 20231103153940.png]]
### Pretty Good Signature

This challenge requires going through a list of pgp signatures until you find the one which is valid. I installed GPT4win and used a python script to interface with it and go through the list. I encountered an issue with regex where the --BEGIN PGP SIGNATURE-- was being left out which caused it not to work at first.

My code:
```python
import subprocess
import re

# Replace this string with your actual public key
public_key = """-----BEGIN PGP PUBLIC KEY BLOCK-----
...
"""

# Import the public key
def import_key(key):
    process = subprocess.run(['gpg', '--import'], input=key, text=True, capture_output=True)
    if process.returncode != 0:
        raise Exception("Failed to import public key.")

# Verify the signature
def verify_signature(message, signature):
    # Write the message and signature to temporary files
    with open('message.txt', 'w') as f:
        f.write(message)
    with open('signature.asc', 'w') as f:
        f.write(signature)
    
    # Use GPG to verify the signature
    process = subprocess.run(['gpg', '--verify', 'signature.asc', 'message.txt'], capture_output=True)
    return process.returncode == 0  # Return True if the signature is valid

# Function to parse messages and signatures from a file
def parse_messages(file_path):
    with open(file_path, 'r') as file:
        raw_data = file.read()

    pattern = re.compile(
        r"-----BEGIN PGP SIGNED MESSAGE-----\n"
        r"Hash: SHA512\n\n"
        r"(.*?)\n"
        r"(-----BEGIN PGP SIGNATURE-----\n"
        r".*?-----END PGP SIGNATURE-----)",
        re.DOTALL
    )
    return pattern.findall(raw_data)

# Parse the input data
parsed_messages = parse_messages("messages.txt")

# Import the public key
import_key(public_key)

# Check each message and signature
for message, signature in parsed_messages:
    if verify_signature(message, signature):
        print("Valid signature found for the message:")
        print(message)
        break
    else:
        print("Invalid signature for the message.")
```

And the results:

![[Pasted image 20231103170218.png]]
### Boomer

First, we must solve a sudoku puzzle. This is easy with an online sudoky solver. The solved puzzle is:

658123479743589162291746538586472913324951687179638254437265891815394726962817345

![[Pasted image 20231103162642.png]]
The cyphertext is:

66v5 h8f1rq234 g7b974358 916229u1vx7465r385 68sv647i291332495r 16z87167vy963r8f2 65h443c7uv2y6y5 89ob18153gu 694jnl7 v2669628a1 gur73 f4a54295b63j 781gb trg gb 6f6pubby45

But I have no idea how to decrypt it using the sudoku result. ciphers typically don't take large numbers as keys and numbers usually aren't so common in ciphertext

## Cracking

### International

The format I identified as md5crypt. The hashcat mode for this is 500. I need a list of all country names as the dictionary plus a rule for appending and substituting special chars.