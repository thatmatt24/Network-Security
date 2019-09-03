"""
Tiny Encryption Algorithm (TEA):
Takes user inputs K0, K1, K2, K3, L0, R0 as strings, 
converts to hexadecimal. Encrypts using two rounds
of blocks, resulting in L1 and R1, and L2 and R2. 
With L2 and R2 representing the final results. 

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

    for i in range(4):

        K[i] = input("Please input K[%s] in Hex String (without " "0x" ")/: " % i)

    for i in range(4):
        K[i] = u32(int(K[i],16)).value


    L[0] = input("Please input L[0] in Hex String (without " "0x" ")/: ")
        
    R[0] = input("Please input R[0] in Hex String (without ""0x"")/: ")

    L[1] = '00000000'

    L[0] = u32(int(L[0], 16)).value
    L[1] = u32(int(L[1], 16)).value
    R[0] = u32(int(R[0], 16)).value

    L[2] = R[1] = R[2] = L[1]    

    ## encrypt
    #  Li= Ri-1     Ri= Li-1田F(Ri-1, K0, K1, δi)               i=1
    #  Li+1= Ri     Ri+1= Li田F(Ri, K2, K3, δi+1)

    D = []

    D.append(DELTAONE)
    D.append(DELTATWO)

    i = j = 1
    
    while i < 3:

        if i == 2:
            j = 3
        
        # L1 = R0, L2 = R1
        L[i] = u32(R[i - 1]).value

        # R[1] = L[0] + ((( R[0] << 4 ) + K[0] ) ^ (( R[0] >> 5 ) + K[1] ) ^ ( R[0] + DELTAONE ))
        lshift = u32(R[i - 1] << 4).value
        add1 = u32(lshift).value + K[j - 1]
        rshift = u32(R[i - 1] >> 5).value
        add2 = rshift + u32(K[j]).value
        add3 = u32(R[i - 1]).value + D[i - 1]
        xor1 = u32(add1).value ^ u32(add2).value
        xor = u32(xor1).value ^ u32(add3).value
        R[i] = u32(L[i - 1] + xor).value
        i += 1


    for i in range(len(L)):
        L[i] = int(L[i])
        L[i] = hex(L[i]).replace('0x', '').upper()
        R[i] = int(R[i])
        R[i] = hex(R[i]).replace('0x', '').upper()
        print("L[{}] = {}        R[{}] = {}".format(i,L[i],i,R[i]))

if __name__ == "__main__":
    main()

