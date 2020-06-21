def encrypt(txt, key, mode):
    k_len = len(key)
    k_ints = [ord(i) for i in key]
    txt_ints = [ord(i) for i in txt]
    ret_txt = ''
    for i in range(len(txt_ints)):
        adder = k_ints[i % k_len]
        v = (txt_ints[i] - 32 + adder) % 95
        ret_txt += chr(v + 32)
    return ret_txt

def decrypt(txt, key, mode):
    k_len = len(key)
    k_ints = [ord(i) for i in key]
    txt_ints = [ord(i) for i in txt]
    ret_txt = ''
    for i in range(len(txt_ints)):
        adder = k_ints[i % k_len]
        adder *= -1
        v = (txt_ints[i] - 32 + adder) % 95
        ret_txt += chr(v + 32)
    return ret_txt