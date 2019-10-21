import hashlib
import shutil
from Crypto.Util import number
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP


with open("symmetric.key") as kxy:
    Kxy = kxy.read().encode('utf-8')

with open("YPublic.key", "r") as ypu:
    rsa_key = RSA.importKey(ypu.read())

with open("message.rsacipher", "wb") as file:
    pass

print("--------------------------------------")

# reading M in chunks


def bytes_in_file(filename):
    with open(filename, "rb") as file:
        while True:
            chunk = file.read(1024)
            if not chunk:
                break
            else:
                yield chunk


# build M (message) from chunks of file
filename = input("Input the name of the message file: ")
b = bytes_in_file(filename)
message = b''.join(m for m in b)
print("Length of message before decryption:", len(message))

# SHA256(M)
h = hashlib.sha256()
h.update(message)

print("\nCreating Digital Digest of:", filename)
print("\nDigital Digest:")
dig_display = h.hexdigest()
for i in range(0, len(dig_display), 16):
    print(dig_display[i:i+2], ' ', dig_display[i+2:i+4], ' ', dig_display[i+4:i+6], ' ', dig_display[i+6:i+8], ' ',
          dig_display[i+8:i+10], ' ', dig_display[i+10:i+12], ' ', dig_display[i+12:i+14], ' ', dig_display[i+14:i+16])


# save SHA256[M] (digital digest) to "message.dd"
with open("message.dd", "wb") as dd:
    dd.write(h.digest())


# AES-En:Kxy(SHA256(M))
cipher = AES.new(Kxy, AES.MODE_ECB)
encrypted = cipher.encrypt(h.digest())
print("\nAES Encrypted")

# save AES-En:Kxy(SHA256(M)) as "message.add-msg"
with open("message.add-msg", "wb") as aes_hash:
    aes_hash.write(encrypted)

with open("message.add-msg", "rb") as file:
    msg = file.read()

with open("message.add-msg", "ab") as file_message:
    file_message.write(message)

# append M to AES-En:Kxy(SHA256(M)) "message.add-msg" -> AES-En:Kxy(SHA256(M))||(M)
with open("message.add-msg", "rb") as file:
    final_message = file.read()

# RSA-En:Ky+(AES-En:Kxy(SHA256(M))||(M)) -> "message.rsacipher"


def encrypt():
    length = rsa_key.size_in_bytes() - 42

    with open("message.rsacipher", "ab") as rsa_file:
        for i in range(0, len(final_message), length):
            cipher = PKCS1_OAEP.new(rsa_key)
            ciphertext = cipher.encrypt(final_message[i: i + length])
            rsa_file.write(ciphertext)


encrypt()

with open("message.rsacipher", "rb") as enc_file:
    encrypted_message = enc_file.read()
print("Length of message:", len(encrypted_message))

# move file to Receiver/
recv_path = shutil.copy('message.rsacipher', '../Receiver/message.rsacipher')
print("\nmessage.rsacipher copied to:", recv_path)
print()

kxy.close()
ypu.close()
dd.close()
aes_hash.close()
