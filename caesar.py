def encrypt(plainText, shift, mode):
    cipherText = '' 
    for ch in plainText:
        if ch.isalpha():
            stayInAlphabet = ord(ch) + int(shift) 
            if stayInAlphabet > ord('z'):
                stayInAlphabet -= 26
            finalLetter = chr(stayInAlphabet)
        cipherText += finalLetter
    return cipherText

def decrypt(text, shift, mode):
    return encrypt(text,int(shift)*(-1), mode)