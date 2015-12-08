__author__ = 'willienuckols'

from Crypto.Cipher import ARC4
from Crypto.PublicKey import RSA
from Crypto import Random


#on creation of a new user, their username and public key is put into a public text file
random_generator = Random.new().read
key = RSA.generate(1024, random_generator)

#when the user uploads a file, encrypt_file is called and a password is asked
#if the user is sharing it, the other users names are looked up and the password is sent to them using their public key





def secret_string(str1, public_key):
    ss = public_key.encrypt(str.encode(str1),32)
    return ss

def encrypt_file(fname, key):
    try:
        data = open(fname, 'rb')
        dfile = open(fname + ".enc", 'wb')
        encr4 = ARC4.new(key)
        nstr = data.read()
        enfile = encr4.encrypt(nstr)
        dfile.write(enfile)
        return True
    except:
        return False


def decrypt_file(fname, key):
    try:

        data = open(fname, 'rb')
        nstr = data.read()
        encr4 = ARC4.new(key)
        ss= encr4.decrypt(nstr)
        dfile = open("DEC_" + fname[:-4], 'wb')
        dfile.write(ss)
        return True
    except:
        return False


def encrypt_body(body, key):
    encr4 = ARC4.new(key)
    return encr4.encrypt(body).decode("cp037")

def decrypt_body(encbody, key):
    encr4 = ARC4.new(key)
    return encr4.decrypt(str.encode(encbody,"cp037")).decode("utf-8")
