import hashlib
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

private_key = RSA.importKey(open("YPrivate.key").read())

Kxy = open("symmetric.key", "rb").read()

input_file = input("Input the name of the message file: ")
 
with open("message.rsacipher", "rb") as cipher_file:
    ciphertext = cipher_file.read()
print("Ciphertext: ", len(ciphertext))

# input_file = input("Input the name of the message file: ")

def rsa_decrypt(ciphertext, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    length = private_key.size_in_bytes() 
    print("Length: ", length)

    with open("decrypted.dd", "ab") as rsa_decrypt:

        for i in range(0, len(ciphertext), length):
            decrypted_block = cipher.decrypt(ciphertext[i: i + length])
            rsa_decrypt.write(decrypted_block)
 
rsa_decrypt(ciphertext, private_key)

with open("decrypted.dd", "rb") as hash_read:
    hash_block = hash_read.read(32)
    message = hash_read.read()
    print("Mes Len: ", len(message))

print("HB:     ", hash_block)
print("HB size:", len(hash_block))

cipher = AES.new(Kxy, AES.MODE_ECB)
decrypted = cipher.decrypt(hash_block)

print("SHA256: ", decrypted)

h = hashlib.sha256()
h.update(message)

if (h.digest() == decrypted):
    print("Digital Digest Authentication Passed")
else:
    print("Digital Digest Authentication Fails")

with open(input_file, "w") as file:
    file.write(message.decode('utf-8'))