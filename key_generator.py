from Crypto.PublicKey import RSA
from Crypto.Util import number
from Crypto import Random
import sys, os, shutil

def main():

    key_size = 1024
    random_gen = Random.new().read

    xpri = RSA.generate(key_size, random_gen)
    ypri = RSA.generate(key_size, random_gen)
    xpub = xpri.publickey()
    ypub = ypri.publickey()

    XPub = open("XPublic.key", "wb")
    XPub.write(xpub.exportKey())


    XPri = open("XPrivate.key", "wb")
    XPri.write(xpri.exportKey())


    YPub = open("YPublic.key","wb")
    YPub.write(ypub.exportKey())


    YPri = open("YPrivate.key", "wb")
    YPri.write(ypri.exportKey())

    XPub.close()
    XPri.close()
    YPub.close()
    YPri.close()

    print("--------------------------------------")
    kxy = input("Enter symmetric key Kxy (16 char - 128 bit): ")
    if(len(kxy) != 16):
        print("Symmetric key must be 16 digits. Modifying input to correct size.\n")

        if(len(kxy) < 16):
            kxy = '1234567890123456'
        else:
            kxy = kxy[0:16]

    Kxy = open("symmetric.key", "w")
    Kxy.write(kxy)
    Kxy.close()

    print("Copying symmetric.key to:", shutil.copy('symmetric.key', '../Sender/symmetric.key'))
    print("Copying symmetric.key to:", shutil.copy('symmetric.key', '../Receiver/symmetric.key'))
    print("Copying YPublic.key to:", shutil.copy('YPublic.key', '../Sender/YPublic.key'))
    print("Copying YPrivate.key to:", shutil.copy('YPrivate.key', '../Receiver/YPrivate.key'))
    print("\n...done")

if __name__ == "__main__":
    main()
