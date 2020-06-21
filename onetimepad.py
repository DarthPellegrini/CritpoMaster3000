import binascii, itertools

def convert_to_bits(s):
    return "".join(format(ord(x), 'b') for x in s)

def xor(m, k):
    r = []
    for i, j in zip(m, k):
        r.append(str(int(i) ^ int(j)))  # xor between bits i and j
    return "".join(r)

def to_str(string):
    res = ''
    for idx in range(len(string)/8):
        tmp = chr(int(string[idx*8:(idx+1)*8], 2))
        res += tmp
    return res

def encryptOneTimePad(text,key):
    return xor(convert_to_bits(text),key) 

def decryptOneTimePad(cipher, key):
    return xor(key, convert_to_bits(cipher))


### BETTER IMPLEMENTATION (?) ###
def encrypt(msg, key, mode):
    '''Return cipher text'''
    cipher = xor_str(msg, key)
    # ascii armor the cipher text
    cipher = (binascii.hexlify(cipher.encode())).decode()
    return cipher

def decrypt(cipher, key, mode):
    '''Return plain text message'''
    # get back the string from ascii armored cipher
    cipher = (binascii.unhexlify(cipher.encode())).decode()
    msg = xor_str(cipher, key)
    return msg

def xor_str(a, b):
    '''Return the xor of the two strings a and b
    The length of the output string is the same as that of first string,
    which means that if second string is shorter than first, it'll be repeated
    over.'''
    xorred = ''.join([chr(ord(x)^ord(y)) for x, y in zip(a, itertools.cycle(b))])
    return xorred