import os
from Crypto.Cipher import ARC4
import encrypt
import json
import talk
import tkinter as tk
import tkinter.filedialog as fdialog
from PIL import Image, ImageTk
from functools import partial
import shutil
import urllib.request

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        root.withdraw()
        self.key = '01234567'
        self.createWidgets()

    def createWidgets(self):
        self.main = tk.Toplevel(self)
        self.hi_there = tk.Label(self.main)
        self.hi_there["text"] = "Welcome to SecureShare!!\n Please Log In!"
        self.hi_there.pack()
        L1 = tk.Label(self.main, text="User Name")
        L1.pack()
        self.username = tk.Entry(self.main)
        self.username.pack()
        L2 = tk.Label(self.main, text="Password")
        L2.pack()
        self.password = tk.Entry(self.main, show='*')
        self.password.pack()
        self.submit = tk.Button(self.main)
        self.submit["text"] = "Log In"
        self.submit["command"] = self.login
        self.submit.pack()
        self.L3 = tk.Label(self.main)
        self.L3.pack()
        self.QUIT = tk.Button(self.main, text="QUIT", fg="red",
                                            command=root.destroy)
        self.QUIT.pack(side = "bottom")

    def login(self):
        self.u = self.username.get()
        self.p = self.password.get()
        auth = talk.comm(self.u, self.p)
        if auth:
            self.open_file_win()
        else:
            self.L3["text"] = "Wrong Username or Password"

    def open_file_win(self):
        self.view = tk.Toplevel(self)
        self.main.destroy()
        self.new_text = tk.Label(self.view)
        self.new_text["text"] = "Welcome " + self.u + "!\n" + "What would you like to do?"
        self.new_text.pack()
        self.reports = tk.Button(self.view)
        self.reports["text"] = "View Reports"
        self.reports["command"] = self.report
        self.reports.pack()
        self.enc = tk.Button(self.view)
        self.enc["text"] = "Encrypt a File"
        self.enc["command"] = self.encrypt
        self.enc.pack()
        self.decry = tk.Button(self.view)
        self.decry["text"] = "Decrypt a File"
        self.decry["command"] = self.decrypt
        self.decry.pack()
        self.log_out = tk.Button(self.view)
        self.log_out["text"] = "Log Out"
        self.log_out["command"] = self.back_to_main
        self.log_out.pack()
        self.log = tk.Label(self.view)
        self.log.pack()

    def back_to_main(self):
        self.view.destroy()
        self.u = ""
        self.p = ""
        self.createWidgets()

    def encrypt(self):
        self.t = tk.Toplevel(self)
        L2 = tk.Label(self.t, text="Create a Password")
        L2.pack()
        self.create_key = tk.Entry(self.t, show='*')
        self.create_key.pack()
        submit = tk.Button(self.t)
        submit["text"] = "Submit"
        submit["command"] = self.encrypt_file
        submit.pack()

    def encrypt_file(self):
        filename = fdialog.askopenfilename()
        key = self.create_key.get()
        self.t.destroy()
        result = encrypt.encrypt_file(filename, key)
        if result:
            self.log["text"]= "Encryption was Successful"
        else:
            self.log["text"]= "An error has occured"

    def decrypt(self):
        self.t2 = tk.Toplevel(self)
        L2 = tk.Label(self.t2, text="Password")
        L2.pack()
        self.enter_key = tk.Entry(self.t2, show='*')
        self.enter_key.pack()
        submit = tk.Button(self.t2)
        submit["text"] = "Submit"
        submit["command"] = self.decrypt_file
        submit.pack()

    def decrypt_file(self):
        filename = fdialog.askopenfilename()
        key = self.enter_key.get()
        self.t2.destroy()
        result = encrypt.decrypt_file(filename, key)
        if result:
            self.log["text"]= "Decryption was Successful"
        else:
            self.log["text"]= "An error has occured"

    def report(self):
        self.rep = tk.Toplevel(self)
        scrollbar = tk.Scrollbar(self.rep)
        scrollbar.pack( side = "right", fill="y")
        self.rep.maxsize(width=600, height=600)
        self.view.destroy()
        canvas = tk.Canvas(self.rep)
        self.back = tk.Button(self.rep)
        self.back["text"] = "Back"        
        self.back["command"] = self.open_file_win2
        self.back.pack()
        self.list_rep = talk.comm_reports(self.u, self.p)
        image = Image.open('contract11.png').convert("RGBA")
        image = image.resize((50, 50))
        photo = ImageTk.PhotoImage(image) 
        for reps in self.list_rep:
            label2 = tk.Label(self.rep,text = reps['report_title'])
            label2.pack()
            label = tk.Button(self.rep, image= photo)
            func =  partial(self.down_fil, reps['id'])
            label["command"] = func
            label.image = photo
            label.pack()
            

    def open_file_win2(self):
        self.rep.destroy()
        self.open_file_win()
        
    def down_fil(self,id_num):
        self.dl = tk.Toplevel(self)
        self.dl.maxsize(width=300, height=600)
        self.list_files = talk.comm_dl(id_num)
        label2 = tk.Label(self.dl,text = "Here are the files to be downloaded!")
        label2.pack()
        for fl in self.list_files:
            head,tail = os.path.split(fl['single_file'])
            label2 = tk.Label(self.dl,text = tail)
            label2.pack()
        submit = tk.Button(self.dl)
        submit["text"] = "Confirm"
        submit["command"] = self.download
        submit.pack()

    def download(self):
        self.dl.destroy()
        filename = fdialog.askdirectory()
        for fl in self.list_files:
            head,tail = os.path.split(fl['single_file'])
            path = "https://sleepy-hamlet-6170.herokuapp.com/media/" + fl['single_file']
            #path = "http://127.0.0.1:8000/media/" + fl['single_file']
            newpath = filename + "/" + tail
            urllib.request.urlretrieve(path, newpath)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
