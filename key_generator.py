from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util import number
from Crypto import Random

def main():

    key_size = 1024
    random_gen = Random.new().read

    # xkey = RSA.generate(1024)
    # ykey = RSA.generate(1024)

    # xpub = xkey.publickey().exportKey()
    # xpri = xkey.exportKey()
    # file_out = open("XPrivate.key", "wb")
    # file_out.write(xpri)
    # pub_out = open("XPublic.key", "wb")
    # pub_out.write(xpub)

    # ypub = ykey.publickey().exportKey()
    # ypri = ykey.exportKey()
    # file_outer = open("YPrivate.key", "wb")
    # file_outer.write(ypri)
    # ypub_out = open("YPublic.key","wb")
    # ypub_out.write(ypub)

    
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

    with open("YPrivate.key", "rb") as key:
        print(key.read())
        
    kxy = input("Enter symmetric key Kxy (16 char - 128 bit): ")
    print(repr(kxy))
    Kxy = open("symmetric.key", "w")
    Kxy.write(kxy)

    Kxy.close()


if __name__ == "__main__":
    main()