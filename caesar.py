def encrypt(plainText, shift, mode):
    cipher = ''
    for char in plainText: 
        if char == ' ':
            cipher = cipher + char
        elif  char.isupper():
            cipher = cipher + chr((ord(char) + int(shift) - 65) % 26 + 65)
        else:
            print(shift)
            cipher = cipher + chr((ord(char) + int(shift) - 97) % 26 + 97)
    return cipher

def decrypt(text, shift, mode):
    return encrypt(text,int(shift)*(-1), mode)