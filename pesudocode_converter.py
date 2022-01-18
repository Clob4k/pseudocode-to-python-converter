# pesudocode_converter.py
# This file is owned by @Luke.Tang 2022

def transDECLARE(ReadLine):
    # preceded by transARRAY
    # ReadLine, TransLine: STRING
    TransLine = ReadLine.replace("DECLARE", "#DECLARE")

def transCOMMENT(ReadLine):
    # ReadLine, TransLine: STRING
    TransLine = ReadLine.replace("//", "#")

def transASSIGN(ReadLine):
    # proceded by transFOR
    # ReadLine, TransLine: STRING
    TransLine = ReadLine.replace("←", "=")

def transARRAY(ReadLine):
    # ReadLine, TransLine: STRING