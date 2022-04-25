# under development

"""
user_interface.py
coding:utf-8

Developed by @Luke.Tang 2022
This program is for converting the pesudocode to the Python code.
For more information, please visit github.com/Clob4k/pesudocode-to-python-converter
"""

import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog


def input_file_path(FilePath):
    FilePath = FilePath.replace("\\", "/")
    FilePath = FilePath.strip()
    return FilePath


def read_file(FilePath):
    try:
        File = open(FilePath, "r", encoding="utf-8")
        Txtfile = File.read()
        return Txtfile
    except:
        return "NotFound"


def choose_file():
    filepath = filedialog.askopenfilename(title="Choose a file", filetypes=[("Pesudocode", "*.txt")])
    filepath = input_file_path(filepath)
    Txtfile = read_file(filepath)
    if Txtfile == "NotFound":
        tk.Message("Wrong file format, consider retry.")
    else:
        scoText.delete(1.0, tk.END)
        scoText.insert(tk.INSERT, Txtfile)


def syntax_check():
    print("connect to syntax check")


window = tk.Tk()
window.title("python-converter")
window.geometry("400x600")

# choose buttom 
filechoose = tk.Button(window, text="Choose a file", command=choose_file)
filechoose.place(x=10, y=100)
filechoose.pack()

# syntax check buttom
syntaxcheck = tk.Button(window, text="Syntax check", command=syntax_check)
syntaxcheck.place(x=50, y=100)
syntaxcheck.pack()

# scrolled text frame
scoText = scrolledtext.ScrolledText(window, width=100, height=200)
scoText.pack()

if __name__ == "__main__":
    window.mainloop()