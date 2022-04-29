"""
file_operation.py
coding:utf-8

Developed by @Luke.Tang 2022
This program is for converting the pseudocode to the Python code.
For more information, please visit github.com/Clob4k/pseudocode-to-python-converter
"""

import os

def sep_line():
    print("-" * 50)

def get_file():
    FilePath = input_file_path()
    textfile = read_file(FilePath)

    while textfile == "NotFound":
        FilePath = input_file_path()
        textfile = read_file(FilePath)

    filename = os.path.basename(FilePath)
    return textfile, filename


def input_file_path():
    FilePath = input(
        "Key in the file path of the file to convert:\n"
        "example : C:/Users/luke/Desktop/test.txt\n"
    )
    FilePath = FilePath.strip()
    FilePath = os.path.normpath(FilePath)
    return FilePath


def read_file(filepath):
    try:
        File = open(filepath, "r", encoding="utf-8")
        textfile = File.readlines()
        return textfile
    except FileNotFoundError:
        sep_line()
        print("Wrong file path or file name, consider retry.")
        return "NotFound"


def file_config():
    DelBlankLines = False
    DelComments = False
    sep_line()
    print("Delete blank lines? key in 1 to confirm, press enter to reserve.")
    if input() == "1":
        DelBlankLines = True
    sep_line()
    print("Delete comments? key in 1 to confirm, press enter to reserve.")
    if input() == "1":
        DelComments = True
    return DelBlankLines, DelComments


def out_put_file(filelist, filename):
    DelBlankLines, DelComments = file_config()
    # fetch the operating path
    currentWorkPath = os.path.dirname(__file__)
    genFilePath = os.path.join(currentWorkPath, filename)
    if os.path.exists(genFilePath):
        sep_line()
        print("The file already exists, consider rename the file.")
        print("press enter to overwrite the original file.")
        print("press 0 to cancel the operation.")
        sep_line()
        option = input()
        if option == "0":
            print("Operation cancelled.")
            exit()
        elif option == "":
            pass
        else:
            print("invalid input.")

    genTxtFile = open(genFilePath, "w", encoding="utf-8")
    for line in filelist:
        if DelBlankLines:
            if line == "":
                continue
        if DelComments:
            if line[0:1] == "#":
                continue
        genTxtFile.write(line)
