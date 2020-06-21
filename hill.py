import string
import numpy as np
import math
from sympy import Matrix #inverse key

def letterToNumber(letter):
    return string.ascii_lowercase.index(letter)

def numberToLetter(number):
    return chr(int(number) + 97)

def keyGeneration(number,size=3):
    key = []
    for i in range(0,size):
        key_line = []
        for j in range(0,size):
            if i == j:
                key_line.append(pow(3,number))
            else:
                key_line.append(0)
        key.append(key_line)
    return np.array(key)
    
def encrypt(raw_message, k, mode):
    module = 26 #english alphabet
    message = []

    key = keyGeneration(int(k))

    key_rows = key.shape[0]
    key_columns = key.shape[1]

    if key_rows != key_columns:
        raise Exception('key must be square matrix!')

    #-------------------------
    for i in range(0, len(raw_message)):
        current_letter = raw_message[i:i+1].lower()
        if current_letter != ' ':
            letter_index = letterToNumber(current_letter)
            message.append(letter_index)
            
    if len(message) % key_rows != 0:
        for i in range(0, len(message)):
            message.append(message[i])
            if len(message) % key_rows == 0:
                break

    # transform message to numpy array
    message = np.array(message)
    message_length = message.shape[0]
    
    #transform message array to matrix
    message.resize(int(message_length/key_rows), key_rows)

    encryption = message @ key

    manualMat = []
    for set_of_int in encryption:
        line = []
        for integer in set_of_int:
            line.append(integer%module)
        manualMat.append(line)
    encryption = np.array(manualMat)

    encrypted_text = ''
    for set_of_int in encryption:
        for integer in set_of_int:
            encrypted_text += numberToLetter(integer)

    return encrypted_text

def decrypt(encrypted_text, k, mode):
    module = 26 #english alphabet

    message = []

    key = keyGeneration(int(k))

    key_rows = key.shape[0]

    for i in range(0, len(encrypted_text)):
        current_letter = encrypted_text[i:i+1].lower()
        if current_letter != ' ':
            letter_index = letterToNumber(current_letter)
            message.append(letter_index)
            
    #message must be multiplier of key line count.
    #if not append beginning of the message to the end

    if len(message) % key_rows != 0:
        for i in range(0, len(message)):
            message.append(message[i])
            if len(message) % key_rows == 0:
                break

    #------------------------
    #transform message to numpy array. we'll use numpy's matrix multiplication
    message = np.array(message)
    message_length = message.shape[0]

    #transform message array to matrix
    message.resize(int(message_length/key_rows), key_rows)

    # inverse key and multiplication

    inverse_key = []
    for set_of_int in key:
        line = []
        for integer in set_of_int:
            line.append(integer%module)
        inverse_key.append(line)
    inverse_key = np.array(inverse_key)

    inverse_key = key @ inverse_key

    decryption = message @ inverse_key

    manualMat = []
    for set_of_int in decryption:
        line = []
        for integer in set_of_int:
            line.append(integer%module)
        manualMat.append(line)
    manualMat = np.array(manualMat)

    decrypted_text = ''
    for set_of_int in manualMat:
        for integer in set_of_int:
            decrypted_text += numberToLetter(integer)

    return decrypted_text