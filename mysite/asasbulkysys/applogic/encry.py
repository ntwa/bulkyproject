import os
import hashlib

# Example generation
salt = os.urandom(32)
key = hashlib.pbkdf2_hmac('sha256', 'mypassword'.encode('utf-8'), salt, 100000)

# Store them as:
storage = salt + key 

# Getting the values back out
salt_from_storage = storage[:32] # 32 is the length of the salt
key_from_storage = storage[32:]
