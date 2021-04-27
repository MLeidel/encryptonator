'''
code file: encryptonator.py
date: Apr 2021
Auth: Michael Leidel
commants:
    Encrypt and Decrypt Files
    with this program

Shortcut Keys:
    <Escape>    quit program
    <Control-q> quit program
    <Control-w> switch "In" and "Out" filenames
    <Control-i> copy "In" filename to "Out"
    <Control-o> copy "Out" filename to "In"
'''

from tkinter import *
from tkinter.ttk import *  # defaults all widgets as ttk
import os
import sys
from tkinter import filedialog
from tkinter import messagebox
from simplecrypt import encrypt, decrypt
from ttkthemes import ThemedTk  # ttkthemes is applied to all widgets

class Application(Frame):
    ''' main class docstring '''
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=True, padx=4, pady=4)
        self.create_widgets()

    def create_widgets(self):
        ''' Set up the GUI '''
        btn_clr1 = Button(self, text='Clr', command=self.btn_clr1_clear)
        btn_clr1.grid(row=1, column=1, padx=2, pady=2)

        btn_clr2 = Button(self, text='Clr', command=self.btn_clr2_clear)
        btn_clr2.grid(row=2, column=1, padx=2, pady=2)

        btn_enc = Button(self, text='Encrypt', command=self.btn_encrypt)
        btn_enc.grid(row=3, column=1, padx=2, pady=2)

        btn_input = Button(self, text='In', command=self.btn_in)
        btn_input.grid(row=1, column=2, padx=2, pady=2)

        btn_output = Button(self, text='Out', command=self.btn_out)
        btn_output.grid(row=2, column=2, padx=2, pady=2)

        btn_dec = Button(self, text='Decrypt', command=self.btn_decrypt)
        btn_dec.grid(row=3, column=2, padx=2, pady=2)

        self.ven_file1 = StringVar()
        en_file1 = Entry(self, textvariable=self.ven_file1, width="30")
        en_file1.grid(row=1, column=3)

        self.ven_file2 = StringVar()
        en_file2 = Entry(self, textvariable=self.ven_file2, width="30")
        en_file2.grid(row=2, column=3)

        self.ven_passw = StringVar()
        # self.ven_passw.trace("w", self.eventHandler)
        en_passw = Entry(self, textvariable=self.ven_passw, width="30", show="*")
        en_passw.grid(row=3, column=3)

        root.bind("<Escape>", self.exit_program)
        root.bind("<Control-q>", self.exit_program)
        root.bind("<Control-w>", self.switch_input)
        root.bind("<Control-i>", self.copy_input)
        root.bind("<Control-o>", self.copy_output)

        root.configure(bg='#333')


    def btn_clr1_clear(self):
        ''' Clear 'In' file entry field '''
        self.ven_file1.set("")


    def btn_clr2_clear(self):
        ''' Clear 'Out' file entry field '''
        self.ven_file2.set("")


    def btn_in(self):
        ''' Prompt filedialog for Input file '''
        user = os.environ['USER']
        filename = filedialog.askopenfilename(initialdir="/home/" + user + "/",
                                              title="Locate file")
        self.ven_file1.set(filename)


    def btn_out(self):
        ''' Prompt filedialog for Output file '''
        user = os.environ['USER']
        filename = filedialog.askopenfilename(initialdir="/home/" + user + "/",
                                              title="Locate file")
        self.ven_file2.set(filename)


    def btn_encrypt(self):
        ''' Encrypt In file to Out file '''
        FILENAME = self.ven_file1.get()
        ENCRNAME = self.ven_file2.get()
        PASSWORD = self.ven_passw.get()

        if FILENAME == "" or ENCRNAME == "" or PASSWORD == "":
            messagebox.showwarning("Warning", "A required field is blank")
            return

        data = open(FILENAME, "rb").read()

        try:
            ciphertext = encrypt(PASSWORD, data)
        except Exception as e:
            messagebox.showerror("Encryption Error", e)
            return

        with open(ENCRNAME, "wb") as f:
            f.write(ciphertext)

        messagebox.showinfo("Encryption Completed", "File Encrypted and Saved")


    def btn_decrypt(self):
        ''' Decrypt In file to Out file '''
        ENCRNAME = self.ven_file1.get()
        FILENAME = self.ven_file2.get()
        PASSWORD = self.ven_passw.get()

        if FILENAME == "" or ENCRNAME == "" or PASSWORD == "":
            messagebox.showwarning("Warning", "A required field is blank")
            return

        data = open(ENCRNAME, "rb").read()

        try:
            plaindata = decrypt(PASSWORD, data)
        except Exception as e:
            messagebox.showerror("Decryption Error", e)
            return

        with open(FILENAME, "wb") as f:
            f.write(plaindata)

        messagebox.showinfo("Decryption Completed", "File Decrypted and Saved")


    def exit_program(self, e):
        ''' Exit Program '''
        root.destroy()


    def switch_input(self, e):
        ''' Switch the In and Out filenames '''
        IN = self.ven_file1.get()
        OUT = self.ven_file2.get()
        self.ven_file1.set(OUT)
        self.ven_file2.set(IN)


    def copy_input(self, e):
        ''' Copy the In file to Out '''
        IN = self.ven_file1.get()
        self.ven_file2.set(IN)


    def copy_output(self, e):
        ''' Copy the Out file to In '''
        OUT = self.ven_file2.get()
        self.ven_file1.set(OUT)

root = ThemedTk(theme="black")

root.title("Encryptonator")
root.resizable(0, 0) # no resize & removes maximize button
app = Application(root)
app.mainloop()
