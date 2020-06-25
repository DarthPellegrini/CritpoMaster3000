from Crypto.Cipher import DES
from Crypto.Util import Counter
import base64

BLOCK_SIZE = 16
iv = b'super_iv'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def encrypt(message,key,mode):
    message = pad(message)
    if(mode == 6):
        cipher = DES.new(key=key, mode=mode, counter=Counter.new(64)) 
    else:
        cipher = DES.new(key, mode, iv) 
    message = str(base64.b64encode(cipher.encrypt(message)))
    return message[2:len(message)-1] 
    
def decrypt(message,key,mode):
    message = base64.b64decode(message)
    if(mode == 6):
        cipher = DES.new(key=key, mode=mode, counter=Counter.new(64)) 
    else:
        cipher = DES.new(key, mode, iv) 
    message = str(unpad(cipher.decrypt(message)))
    return message[2:len(message)-1]