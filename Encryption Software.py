def check_length(mk):
    return len(mk) >= 10

def check_uppercase(mk):
    for c in mk:
        if c.isupper():
            return True
    return False

def check_lowercase(mk):
    for c in mk:
        if c.islower():
            return True
    return False

def check_digit(mk):
    for c in mk:
        if c.isdigit():
            return True
    return False

def check_special(mk):
    for c in mk:
        if not c.isalnum() and c != " ":
            return True
    return False

def check_space(mk):
    for c in mk:
        if c == " ":
            return False
    return True

def validate_masterkey():
    while True:
        mk = input("Enter master key (Must remember!): ")
        errors = []

        if not check_length(mk):
            errors.append("At least 10 characters needed")

        if not check_uppercase(mk):
            errors.append("At least 1 uppercase character needed")

        if not check_lowercase(mk):
            errors.append("At least 1 lowercase character needed")

        if not check_digit(mk):
            errors.append("At least 1 digit needed")

        if not check_special(mk):
            errors.append("At least 1 special character needed")

        if not check_space(mk):
            errors.append("No spaces allowed")

        if not errors:
            return mk

        print("\nYour password must meet the following requirements:")
        for e in errors:
            print(e)

def vault_save():
    data = json.dumps(vault).encode()
    encrypted = f.encrypt(data)
    with open("vault.enc", "wb") as v:
        v.write(encrypted)
        

def vault_view():
    if not vault:
        print("Vault is empty.")
    else:
        for service, password in vault.items():
            print(f"{service:^20} = {password:^20}")

def vault_add():
    addservice = input("Enter service name: ")
    addpassword = input("Enter service password: ")
    vault[addservice] = addpassword

def vault_delete():
    service = input("Enter service name you want deleted: ")
    if service in vault:
        del vault[service]
        print("Deleted.")
    else:
        print("Service not found.")
        
def menu():
    while True:
        print()
        print("1. View all entries")
        print("2. Add an entry")
        print("3. Delete an entry")
        print("4. Save and Exit")
        print()
        action = input("Enter your option: ")

        if action == "1":
            vault_view()
        elif action == "2":
            vault_add()
        elif action == "3":
            vault_delete()
        elif action == "4":
            vault_save()
            break
        else:
            print("Error. Invalid choice.")

import os
import random
vault_file = "vault.enc"
characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
salt = []
vault = {}
import base64
from cryptography.fernet import Fernet
import json
from hashlib import pbkdf2_hmac


if os.path.exists(vault_file):
    print("Vault found!")
    userpass = input("Enter master key to unlock: ")
    
    with open("saltbytes.txt", "rb") as f:
        salt_bytes = f.read()
    with open("vault_key", "rb") as f:
        vaultpass = f.read()
    iterations = 10000
    hash = pbkdf2_hmac('SHA512', userpass.encode(), salt_bytes, iterations, dklen=64)
    if hash == vaultpass:
        fernet_key = base64.urlsafe_b64encode(hash[:32])
        f = Fernet(fernet_key)
        with open("vault.enc", "rb") as v:
            encrypted = v.read()
        try:
            decrypted = f.decrypt(encrypted)
            vault = json.loads(decrypted.decode())
        except:
            print("Vault corrupted or wrong key.")
            vault = {}
        menu()
    else:
        print("Incorrect password.")
        print("Restart to re-enter.")
   
else:
    print("No vault exists.")
    print("Creating vault...")
    print("Welcome To An Encryption Service.")
    
    masterkey = validate_masterkey()
    print("Master key accepted!")
    
    for i in range(12):
        salt.append(random.choice(characters))
    saltjoined = "".join(salt)
    
    saltbytes = bytes(saltjoined, encoding="utf-8")
    
    with open("saltbytes.txt", "wb") as f:
        f.write(saltbytes)

    from hashlib import pbkdf2_hmac
    iterations = 10000
    passwordtohash = masterkey
    
    hash = pbkdf2_hmac('SHA512', bytes(passwordtohash,'utf-8'), saltbytes, iterations, dklen=64)
    with open("vault_key", "wb") as f:
        f.write(hash)
    vault = {}
    fernet_key = base64.urlsafe_b64encode(hash[:32])
    f = Fernet(fernet_key)
    menu()
