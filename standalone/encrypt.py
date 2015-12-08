from Crypto.Cipher import ARC4
import os

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
        ss = encr4.decrypt(nstr)
        head,tail = os.path.split(fname)
        file_new = "DEC_" + tail[:-4]
        file2 = fname[:-(len(tail))]
        ffile = file2 + file_new
        dfile = open(ffile, 'wb')        
        dfile.write(ss)
        return True
    except:
        return False
