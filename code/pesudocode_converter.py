# pesudocode_converter.py
# This program is developed by @Luke.Tang 2022

import regex as re
import os

def getFile():
    filePath = inputFilePath()
    txtfile = readFile(filePath)
    while txtfile == "notFound":
        filePath = inputFilePath()
        txtfile = readFile(filePath)
    return txtfile

def inputFilePath():
    filePath = input("Key in the file path of the file to convert:\n")
    filePath = filePath.replace("\\", "/")
    return filePath

def readFile(filePath):
    try:
        file = open(filePath, 'r', encoding='utf-8')
        txtfile = file.readlines()
        return txtfile
    except FileNotFoundError:
        print("Wrong file path or file name, consider retry.")
        return "notFound"

def convertFile(txtfile):
    convFile = convKeyWords(txtfile)
    syntaxCheck()
    return convFile

def convKeyWords(txtfile):
    print("Convertion in process.")
    convFile = ""
    for line in txtfile:
        nextLine = True
        if line == "\n":
            nextLine = False
        else:
            #indentation
            blanks = 0
            while line[blanks] == " ":
                blanks = blanks + 4
            inden = int(blanks/4)
            line = line.strip()
            #convert comments
            line = line.replace('//','#')
            if "NEXT" in line:
                line = ""
                inden = 0
                nextLine = False
            elif "THEN" in line:
                line = ""
                inden = 0
                nextLine = False
            elif "ENDIF" in line:
                line = ""
                inden = 0
                nextLine = False
            elif "ELSE" in line:
                line = line.replace("ELSE","else:")
            elif "OUTPUT" in line:
                line = convOutput(line)
            elif "DECLARE" in line:
                line = convDeclare(line)
            elif "FOR" in line:
                line = convFor(line)
            elif "IF" in line:
                line = convIF(line)
            line = line.replace("NOT","not")
            line = line.replace("OR","or")
            line = line.replace("AND","and")
            line = line.replace("TRUE","True")
            line = line.replace("FALSE","False")
            line = line.replace("←","=")
            line = "    "*inden + line
        convFile = convFile + line
        if nextLine == True:
            convFile = convFile + "\n"
    return convFile

def convOutput(line):
    thisLine = line
    varNameList = re.findall(r'OUTPUT(.*?)\Z',line)
    varName = ""
    varName = varName.join(varNameList)
    varName = varName.strip()
    varName = varName.replace("&","+")
    thisLine = "print({})".format(varName)
    return thisLine

def convDeclare(line):
    thisLine = line
    if "ARRAY" in line:
        #get variable name
        varNameList = re.findall(r'DECLARE(.*?):',line)
        varName = ""
        varName = varName.join(varNameList)
        varName = varName.strip()
        thisLine = varName + " = []"
    else:
        thisLine = line.replace("DECLARE","#DECLARE")
    return thisLine

def convFor(line):
    varNameList = re.findall(r'FOR(.*?)←',line)
    varName = ""
    varName = varName.join(varNameList)
    varName = varName.strip()
    varRangeList = re.findall("\d+",line)
    ini = varRangeList[0]
    end = varRangeList[1]
    thisLine = "for {} in range({},{}):".format(varName, ini, end)
    return thisLine

def convIF(line):
    if ">=" in line:
        varNameList = re.findall(r'IF(.*?)>=',line)
        varValueList = re.findall(r'>=(.*?)\Z',line)
        symbol = ">="
    elif "<=" in line:
        varNameList = re.findall(r'IF(.*?)<=',line)
        varValueList = re.findall(r'<=(.*?)\Z',line)
        symbol = "<="
    elif "<>" in line:
        varNameList = re.findall(r'IF(.*?)<>',line)
        varValueList = re.findall(r'<>(.*?)\Z',line)
        symbol = "!="
    else:
        varNameList = re.findall(r'IF(.*?)=',line)
        varValueList = re.findall(r'=(.*?)\Z',line)
        symbol = "=="
    varName = ""
    varName = varName.join(varNameList)
    varName = varName.strip()
    varValue = ""
    varValue = varValue.join(varValueList)
    varValue = varValue.strip()  
    thisLine = "if {} {} {}:".format(varName, symbol, varValue)
    return thisLine


def syntaxCheck():
    print('progressing')

def outputFile(convFile):
    fileConfig()
    currentWorkPath = os.path.dirname(__file__)
    genFilePath = currentWorkPath + "/convertedFile.txt"
    genTxtFile = open(genFilePath, 'w', encoding='utf-8')
    lineList = convFile.split("\n")
    for line in lineList:
        genTxtFile.write(line)
        genTxtFile.write("\n")

def fileConfig():
    print('progressing')

def executeFile():
    print('progressing')

def main():
    txtfile = getFile()
    convFile = convertFile(txtfile)
    outputFile(convFile)
    executeFile()

main()