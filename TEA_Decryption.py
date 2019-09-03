"""
Tiny Encryption Algorithm (TEA): (decryption)
Takes user inputs K0, K1, K2, K3, L2, R2 as strings, 
converts to hexadecimal. Dencryptts using two rounds
of blocks, resulting in L1 and R1, and L0 and R0. 
With L0 and R0 representing the final results. 

Author: Matt McMahon
Date: 9/1/19
"""


from ctypes import c_uint32 as u32

DELTAONE = 0x11111111
DELTATWO = 0x22222222

def main():

    K = [""] * 4
    L = [""] * 3
    R = [""] * 3

    # inputs
    for i in range(4):

        K[i] = input("Please input K[%s] in Hex String (without " "0x" ")/: " % i)

    for i in range(4):
        K[i] = u32(int(K[i],16)).value

    L[2] = input("Please input L[2] in Hex String (without " "0x" ")/: ")
        
    R[2] = input("Please input R[2] in Hex String (without ""0x"")/: ")

    L[0] = '00000000'

    L[0] = u32(int(L[0], 16)).value
    L[2] = u32(int(L[2], 16)).value
    R[2] = u32(int(R[2], 16)).value

    L[1] = R[0] = R[1] = L[0]    


    ## decrypt
    D = []

    D.append(DELTAONE)
    D.append(DELTATWO)
    
    R[1] = L[2]

    lshift = u32(L[2] << 4).value
    add1 = u32(lshift).value + K[2]
    add2 = u32(L[2]).value + u32(D[1]).value
    rshift = u32(L[2] >> 5).value
    add3 = u32(rshift).value + K[3]
    xor1 = u32(add1).value ^ u32(add2).value
    xor = u32(xor1).value ^ u32(add3).value
    L[1] = u32(R[2]).value - u32(xor).value

    R[0] = L[1]

    lshift = u32(R[0] << 4).value
    add1 = u32(lshift).value + K[0]
    add2 = u32(R[0]).value + u32(D[0]).value
    rshift = u32(R[0] >> 5).value
    add3 = u32(rshift).value + K[1]
    xor1 = u32(add1).value ^ u32(add2).value
    xor = u32(xor1).value ^ u32(add3).value
    L[0] = u32(L[2]).value - u32(xor).value


    # print
    k = 2
    while k > -1:
        L[k] = int(L[k])
        L[k] = hex(L[k]).replace('0x', '').upper()
        R[k] = int(R[k])
        R[k] = hex(R[k]).replace('0x','').upper()
        print("L[{}] = {}        R[{}] = {}".format(k,L[k],k,R[k]))
        k -= 1 
    

if __name__ == "__main__":
    main()
