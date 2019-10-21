import hashlib
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

private_key = RSA.importKey(open("YPrivate.key").read())

Kxy = open("symmetric.key", "rb").read()

print("--------------------------------------")

input_file = input("Input the name of the message file: ")

print("\nReading from message.rsacipher...")
with open("message.rsacipher", "rb") as cipher_file:
    ciphertext = cipher_file.read()

print("Length of Ciphertext:", len(ciphertext))

def rsa_decrypt(ciphertext, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    length = private_key.size_in_bytes()

    with open("message.add-msg", "ab") as rsa_decrypt:

        for i in range(0, len(ciphertext), length):
            decrypted_block = cipher.decrypt(ciphertext[i: i + length])
            rsa_decrypt.write(decrypted_block)

rsa_decrypt(ciphertext, private_key)
print("\nDecrypted message.rsacipher\n")

with open("message.add-msg", "rb") as hash_read:
    auth_dd = hash_read.read(32)
    message = hash_read.read()

#print("Authentic Digital Digest: ", auth_dd, "\n")
with open(input_file, "wb") as file:
    file.write(message)

cipher = AES.new(Kxy, AES.MODE_ECB)
digital_digest = cipher.decrypt(auth_dd)

with open("message.dd","wb") as dd_file:
    dd_file.write(digital_digest)

print("Digital Digest:")
hex_ddigest = digital_digest.hex()
for i in range(0, len(hex_ddigest), 16):
    print(hex_ddigest[i: i + 2], ' ', hex_ddigest[i + 2 : i + 4], ' ', hex_ddigest[i + 4 : i + 6], ' ', hex_ddigest[i + 6 : i + 8], ' ',
      hex_ddigest[i+8:i+10],' ', hex_ddigest[i+10:i+12],' ', hex_ddigest[i+12:i+14],' ', hex_ddigest[i+14:i+16])

print("Length of decrypted message:", len(message))

h = hashlib.sha256()
h.update(message)

if (h.digest() == digital_digest):
    print("\nDigital Digest Authentication Passed")
else:
    print("\nDigital Digest Authentication Fails")

