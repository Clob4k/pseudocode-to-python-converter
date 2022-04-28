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
    textfile = read_file(FilePath)

    while textfile == "NotFound":
        FilePath = input_file_path()
        textfile = read_file(FilePath)
    return textfile


def input_file_path():
    FilePath = input(
        "Key in the file path of the file to convert:\n"
        "example : C:/Users/luke/Desktop/test.txt\n"
        "\\ is also acceptable\n"
    )
    FilePath = FilePath.replace("\\", "/")
    FilePath = FilePath.strip()
    return FilePath


def read_file(filepath):
    try:
        File = open(filepath, "r", encoding="utf-8")
        textfile = File.readlines()
        return textfile
    except FileNotFoundError:
        print("Wrong file path or file name, consider retry.")
        return "NotFound"


def file_config():
    DelBlankLines = False
    DelComments = False
    print("Delete blank lines? key in 1 to confirm, press enter to reserve.")
    if input() == "1":
        DelBlankLines = True
    print("Delete comments? key in 1 to confirm, press enter to reserve.")
    if input() == "1":
        DelComments = True
    return DelBlankLines, DelComments


def out_put_file(filelist):
    DelBlankLines, DelComments = file_config()
    # fetch the operating path
    currentWorkPath = os.path.dirname(__file__)
    genFilePath = currentWorkPath + "/converted_file.txt"
    genTxtFile = open(genFilePath, "w", encoding="utf-8")
    for line in filelist:
        if DelBlankLines:
            if line == "":
                continue
        if DelComments:
            if line[0:1] == "#":
                continue
        genTxtFile.write(line)
