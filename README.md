# Encrypted-Storage
Master key (encrypted) needed to access passwords and information added.

A simple command-line password vault that securely stores service passwords using encryption.
This project features master-key validation, password hashing, salt generation, and Fernet symmetric encryption.

Features

Create and validate a secure master key
Generate a random salt for password hashing
Derive encryption keys using PBKDF2-HMAC (SHA-512)
Encrypt and decrypt stored passwords using Fernet
Add, view, and delete vault entries
Persistent encrypted storage (vault.enc)
Automatic detection of first-time setup vs existing vault

How It Works:

1. Master Key Creation
On first launch, the program asks you to create a master key that must meet these rules:
At least 10 characters
At least 1 uppercase, 1 lowercase, 1 digit, 1 special character
No spaces
The master key is never stored. Instead, a PBKDF2-HMAC hash is generated and saved.

2. Encryption Setup

The program:

Generates a 12-character random salt
Stores it in saltbytes.txt
Hashes the master key with PBKDF2-HMAC (SHA-512 × 10,000 iterations)
Saves the hash in vault_key
Uses the first 32 bytes of the hash as the Fernet encryption key

3. Encrypted Vault

The vault itself is a Python dictionary, encrypted with Fernet
Only the correct master key can decrypt it.

4. Usage
   
First Run:

No vault exists.
Creating vault...
Welcome To An Encryption Service.
You will be prompted to create a master key.
Unlocking the Vault

On later runs:

Vault found!
Enter master key to unlock:
If the hash matches, the vault decrypts and loads.

Menu Options

Once unlocked, you can:

1. View all entries
2. Add an entry
3. Delete an entry
4. Save and Exit

Your vault updates ONLY when choosing Save and Exit.

5. Why I Built This

This secure encrypted vault helped me learn about:
Hashing
Salts
Encryption
Secure storage
User input validation
Python file handling
