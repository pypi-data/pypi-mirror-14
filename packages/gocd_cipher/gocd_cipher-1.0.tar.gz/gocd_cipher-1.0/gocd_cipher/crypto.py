import base64

from Crypto.Cipher import DES

from gocd_cipher.util import bouncy_hex_decode


def pkcs5(value):
    pad = 8 - (len(value) % 8)
    return value + (chr(pad) * pad)


def gocd_encrypt(key, plaintext):
    cipher = DES.new(bouncy_hex_decode(key), mode=DES.MODE_CBC, IV=chr(0) * 8)
    return base64.b64encode(cipher.encrypt(pkcs5(plaintext)))


def gocd_decrypt(key, ciphertext):
    cipher = DES.new(bouncy_hex_decode(key), mode=DES.MODE_CBC, IV=chr(0) * 8)
    padded_plaintext = cipher.decrypt(base64.b64decode(ciphertext))
    pad_length = ord(padded_plaintext[-1])
    return padded_plaintext[:-pad_length]


def gocd_reencrypt(old_key, new_key, ciphertext):
    return gocd_encrypt(new_key, gocd_decrypt(old_key, ciphertext))