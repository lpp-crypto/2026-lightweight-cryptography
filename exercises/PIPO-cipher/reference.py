#!/usr/bin/env python

from random import randint

class PIPO:
    def __init__(self, key_bitlength: int):
        """Initializes a PIPO based on the key length.

        Args:
            key_bitlength(int): The key length (in bits). Must be either 128, 192 or 256.
        
        """
        assert key_bitlength in [128, 192, 256]
        if key_bitlength == 128:
            self.key_length = 16
            self.n_rounds = 9
        elif key_bitlength == 192:
            self.key_length = 24
            self.n_rounds = 11
        elif key_bitlength == 256:
            self.key_length = 32
            self.n_rounds = 13
        self.sbox = [
            234,73,225,28,64,68,134,174,242,239,211,221,183,37,232,203,
            42,105,1,44,192,4,150,126,162,111,163,253,151,149,184,75,
            10,137,177,12,144,244,230,190,130,255,19,189,71,69,56,139,
            26,249,209,124,48,52,70,62,146,127,227,93,39,133,104,11,
            138,233,113,204,160,36,22,78,50,191,179,205,119,229,168,219,
            122,9,97,108,224,164,6,94,2,31,195,109,135,181,248,27,
            250,121,17,172,80,100,166,254,178,175,99,125,247,85,216,187,
            202,185,81,220,32,196,102,222,210,63,51,45,215,165,200,235,
            106,153,193,140,96,84,182,14,66,207,131,13,7,101,136,107,
            170,169,161,60,128,132,86,142,34,95,35,61,231,197,24,43,
            186,57,145,92,112,228,214,30,18,15,67,157,87,53,88,171,
            90,25,65,156,240,212,246,110,82,143,3,77,199,245,72,155,
            58,201,49,188,16,180,38,158,114,159,115,141,23,213,40,251,
            74,89,129,76,208,116,54,46,226,223,147,237,55,5,152,59,
            218,217,241,236,176,20,198,206,98,47,83,173,103,117,120,91,
            154,41,33,252,0,148,118,238,194,79,243,29,167,21,8,123
        ]
        self.sbox_inv = []
        for x in range(0, 256):
            self.sbox_inv.append(self.sbox.index(x))
            

    def keySchedule(self, K: list[int]) -> None:
        """Sets the self.subkeys attribute using the given master key.

        It must be of length self.key_length.

        """
        assert len(K) == self.key_length
        self.subkeys = [
            [K[(13*i + 7*j) % self.key_length] for j in range(0, 16)]
            for i in range(0, self.n_rounds+1)
        ]

        
    def subBytes(self, state: list[list[int]]) -> list[list[int]]:
        return [[self.sbox[state[i][j]] for j in range(0, 4)]
                for i in range(0, 4)]

    
    def subBytes_inv(self, state: list[list[int]]) -> list[list[int]]:
        return [[self.sbox_inv[state[i][j]] for j in range(0, 4)]
                for i in range(0, 4)]

    
    def mixColumns(self, state: list[list[int]]) -> list[list[int]]:
        cols = [[state[j][i] for j in range(0, 4)]
                for i in range(0, 4)]
        for i in range(0, 4):
            cols[i] = [
                cols[i][1] ^ cols[i][2] ^ cols[i][3],
                cols[i][0] ^ cols[i][2] ^ cols[i][3],
                cols[i][0] ^ cols[i][1] ^ cols[i][3],
                cols[i][0] ^ cols[i][1] ^ cols[i][2],
            ]
        return [[cols[j][i] for j in range(0, 4)]
                for i in range(0, 4)]

    
    def shiftRows(self, state: list[list[int]]) -> list[list[int]]:
        return [[state[i][(j+i) % 4] for j in range(0, 4)]
                for i in range(0, 4)]

    
    def shiftRows_inv(self, state: list[list[int]]) -> list[list[int]]:
        return [[state[i][(j-i) % 4] for j in range(0, 4)]
                for i in range(0, 4)]

    
    def addSubKey(self, state: list[list[int]], r: int) -> list[list[int]]:
        return [
                [state[i][j] ^ self.subkeys[r][4*i+j] ^ (4*i+j) for j in range(0, 4)]
                for i in range(0, 4)
            ]

    
    def encrypt(self, x: list[int], K: list[int]) -> list[int]:
        assert len(x) == 16
        self.keySchedule(K)
        state = [[x[4*i + j] for j in range(0, 4)]
                 for i in range(0, 4)]
        # "normal" rounds
        for r in range(0, self.n_rounds-1):
            state = self.addSubKey(state, r)
            state = self.subBytes(state)
            state = self.shiftRows(state)
            state = self.mixColumns(state)
        # last round (without linear part)
        state = self.addSubKey(state, self.n_rounds-1)
        state = self.subBytes(state)
        # final whitening
        state = self.addSubKey(state, self.n_rounds)
        return state[0] + state[1] + state[2] + state[3]

    
    def decrypt(self, x: list[int], K: list[int]) -> list[int]:
        assert len(x) == 16
        self.keySchedule(K)
        state = [[x[4*i + j] for j in range(0, 4)]
                 for i in range(0, 4)]
        # final whitening
        state = self.addSubKey(state, self.n_rounds)
        # last round (without linear part)
        state = self.subBytes_inv(state)
        state = self.addSubKey(state, self.n_rounds-1)
        # "normal" rounds
        for r in reversed(range(0, self.n_rounds-1)):
            state = self.mixColumns(state)
            state = self.shiftRows_inv(state)
            state = self.subBytes_inv(state)
            state = self.addSubKey(state, r)
        return state[0] + state[1] + state[2] + state[3]


def hex_vec(x):
    result = ""
    for x_i in x:
        result += "{:02x} ".format(x_i)
    return result


if __name__ == "__main__":
    x = [randint(0, 255) for i in range(0, 16)]
    K = [randint(0, 255) for i in range(0, 16)]
    E = PIPO(128)
    print("x =         ", hex_vec(x))
    print("K =         ", hex_vec(K))
    y = E.encrypt(x, K)
    print("PIPO_K(x) = ", hex_vec(y))

