import hashlib
from Crypto.Util import number
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP


with open("symmetric.key") as kxy:
    Kxy = kxy.read().encode('utf-8')

with open("YPublic.key", "r") as ypu:
    rsa_key = RSA.importKey(ypu.read())

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

# SHA256(M)
h = hashlib.sha256()
h.update(message)
print("digest length: ", len(h.digest()))
print("digest: ", h.digest())

# save SHA256[M] (digital digest) to "message.dd"
with open("message.dd", "wb") as dd:
    dd.write(h.digest())


# AES-En:Kxy(SHA256(M))
cipher = AES.new(Kxy, AES.MODE_ECB)
encrypted = cipher.encrypt(h.digest())
print("AES:    ", encrypted)
print("AES len: ", len(encrypted))

# save AES-En:Kxy(SHA256(M)) as "message.add-msg"
with open("message.add-msg", "wb") as aes_hash:
    aes_hash.write(encrypted)

# print("Message: ", message)

with open("message.add-msg", "rb") as file:
    # print("Before appending", file.read())
    msg = file.read()
with open("message.add-msg", "ab") as file_message:
    file_message.write(message)

# append M to AES-En:Kxy(SHA256(M)) "message.add-msg" -> AES-En:Kxy(SHA256(M))||(M)
with open("message.add-msg", "rb") as file:
    final_message = file.read()
    print("add-msg length: ", len(final_message))

# RSA-En:Ky+(AES-En:Kxy(SHA256(M))||(M)) -> "message.rsacipher"
def encrypt():
    length = rsa_key.size_in_bytes() - 42
    print("Length of pub key: ", length)
    print("Length of message: ", len(final_message))

    with open("message.rsacipher", "ab") as rsa_file:

        for i in range(0, len(final_message), length):
            cipher = PKCS1_OAEP.new(rsa_key)
            ciphertext = cipher.encrypt(final_message[i: i + length])
            rsa_file.write(ciphertext)

encrypt()

kxy.close()
ypu.close()
dd.close()
aes_hash.close()
