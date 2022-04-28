"""
file_operation.py
coding:utf-8

Developed by @Luke.Tang 2022
This program is for converting the pseudocode to the Python code.
For more information, please visit github.com/Clob4k/pseudocode-to-python-converter
"""

import os


def get_file():
    FilePath = input_file_path()
    Txtfile = read_file(FilePath)

    while Txtfile == "NotFound":
        FilePath = input_file_path()
        Txtfile = read_file(FilePath)
    return Txtfile


def input_file_path():
    FilePath = input(
        "Key in the file path of the file to convert:\n"
        "example : C:/Users/luke/Desktop/test.txt\n"
        "\\ is also acceptable\n"
    )
    FilePath = FilePath.replace("\\", "/")
    FilePath = FilePath.strip()
    return FilePath


def read_file(FilePath):
    try:
        File = open(FilePath, "r", encoding="utf-8")
        Txtfile = File.readlines()
        return Txtfile
    except:
        print("Wrong file path or file name, consider retry.")
        return "NotFound"


def file_config():
    DelBlankLines = False
    DelComments = False
    print("Delete blank lines? key in 1 to confirm, enter to reject.")
    if input() == "1":
        DelBlankLines = True
    print("Delete comments(#)? key in 1 to confirm, enter to reject.")
    if input() == "1":
        DelComments = True
    return DelBlankLines, DelComments


def out_put_file(convFileList):
    DelBlankLines, DelComments = file_config()
    # fetch the operating path
    currentWorkPath = os.path.dirname(__file__)
    genFilePath = currentWorkPath + "/converted_file.txt"
    genTxtFile = open(genFilePath, "w", encoding="utf-8")
    for line in convFileList:
        if DelBlankLines == True:
            if line == "":
                continue
        if DelComments == True:
            if line[0:1] == "#":
                continue
        genTxtFile.write(line)
