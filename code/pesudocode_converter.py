# pesudocode_converter.py
# This program is developed by @Luke.Tang 2022

import regex as re
import os

def sepLine():
    print("-"*45)

def getFile():
    filePath = inputFilePath()
    txtfile = readFile(filePath)
    while txtfile == "notFound":
        filePath = inputFilePath()
        txtfile = readFile(filePath)
    return txtfile

def inputFilePath():
    sepLine()
    filePath = input("Key in the file path of the file to convert:\n")
    filePath = filePath.replace("\\", "/")
    filePath = filePath.strip()
    return filePath

def readFile(filePath):
    try:
        file = open(filePath, 'r', encoding='utf-8')
        txtfile = file.readlines()
        return txtfile
    except:
        print("Wrong file path or file name, consider retry.")
        return "notFound"

def convertFile(txtfile):
    convFile = convKeyWords(txtfile)
    syntaxCheck()
    return convFile

def convKeyWords(txtfile):
    sepLine()
    print("Convertion in process.")
    convFile = ""
    for line in txtfile:
        nextLine = True
        if line == "\n":
            nextLine = False
        else:
            # indentation count
            blanks = 0
            while line[blanks] == " ":
                blanks = blanks + 4
            inden = int(blanks/4)
            line = line.strip()

            # line deletion
            line,inden,nextLine = dirDel(line,inden,nextLine)
            line = delLine(line)

            # line convertion
            if "LCASE" in line:
                line = convLcase(line)
            elif "UCASE" in line:
                line = convUcase(line)
            elif "RIGHT" in line:
                line = convRight(line)
            elif "MID" in line:
                line = convMid(line)
            elif "OUTPUT" in line:
                line = convOutput(line)
            elif "DECLARE" in line:
                line = convDeclare(line)
            elif "OPENFILE" in line:
                line = convOpenFile(line)
            elif "READFILE" in line:
                line = convReadFile(line)
            elif "WRITEFILE" in line:
                line = convWriteFile(line)
            elif "CLOSEFILE" in line:
                line = convCloseFile(line)
            elif "FOR" in line:
                line = convFor(line)
            elif "IF" in line:
                line = convIF(line)

            line = convReplace(line)
            # indentation addition
            line = "    "*inden + line

        convFile = convFile + line
        if nextLine == True:
            convFile = convFile + "\n"
    return convFile

def dirDel(line,inden,nextLine):
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
    elif "ENDWHILE" in line:
        line = ""
        inden = 0
        nextLine = False
    return (line,inden,nextLine)

def delLine(line):
    if "ELSE" in line:
        line = line.replace("ELSE","else:")
    elif "LENGTH" in line:
        line = line.replace("LENGTH","len")
    elif "WHILE" in line:
        line = line.replace("WHILE","while")
        line = line + ":"
    return line

def convReplace(line):
    line = line.replace('//','#')
    line = line.replace("NOT","not")
    line = line.replace("OR","or")
    line = line.replace("AND","and")
    line = line.replace("TRUE","True")
    line = line.replace("FALSE","False")
    line = line.replace("←","=")
    line = line.replace("&","+")
    return line

def convLcase(line):
    # get variable name
    varNameList = re.findall(r'LCASE\((.*?)\)',line)
    varName = ""
    varName = varName.join(varNameList)
    varName = varName.strip()
    thisLine = "{}.lower".format(varName)
    return thisLine

def convUcase(line):
    varNameList = re.findall(r'UCASE\((.*?)\)',line)
    varName = ""
    varName = varName.join(varNameList)
    varName = varName.strip()
    thisLine = "{}.upper".format(varName)
    return thisLine

def convRight(line):
    varNameList = re.findall(r'RIGHT\((.*?),',line)
    varNumList = re.findall("\d+",line)
    integer = varNumList[-1]
    varName = ""
    varName = varName.join(varNameList)
    varName = varName.strip()
    thisLine = "{}[0:{}]".format(varName,integer)
    return thisLine

def convMid(line):
    varNameList = re.findall(r'\((.*?),',line)
    varNumList = re.findall("\d+",line)
    startVal = varNumList[-2]
    lenVal = varNumList[-1]
    startVal = str(eval(startVal)-1)
    lenVal = str(eval(lenVal)+1)
    varName = ""
    varName = varName.join(varNameList)
    varName = varName.strip()
    thisLine = "{}[{}:{}]".format(varName,startVal,lenVal)
    return thisLine

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
    ini = varRangeList[-2]
    end = varRangeList[-1]
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
        if "=" in line:
            varNameList = re.findall(r'IF(.*?)=',line)
            varValueList = re.findall(r'=(.*?)\Z',line)
            symbol = "=="
        elif ">" in line:
            varNameList = re.findall(r'IF(.*?)>',line)
            varValueList = re.findall(r'>(.*?)\Z',line)
            symbol = ">"
        elif "<" in line:
            varNameList = re.findall(r'IF(.*?)<',line)
            varValueList = re.findall(r'<(.*?)\Z',line)
            symbol = "<"
    varName = ""
    varName = varName.join(varNameList)
    varName = varName.strip()
    varValue = ""
    varValue = varValue.join(varValueList)
    varValue = varValue.strip()  
    thisLine = "if {} {} {}:".format(varName, symbol, varValue)
    return thisLine

def convOpenFile(line):
    if "READ" in line:
        openMod = "r"
    elif "WRITE" in line:
        openMod = "w"
    elif "APPEND" in line:
        openMod = "a"
    varNameList = re.findall(r'OPENFILE(.*?)FOR',line)
    varName = ""
    varName = varName.join(varNameList)
    varName = varName.strip()
    fileName = varName[1:]
    fileName = fileName[:-5]
    thisLine = "{} = open({},'{}')".format(fileName,varName,openMod)
    return thisLine

def convReadFile(line):
    varFileList = re.findall(r'READFILE(.*?),',line)
    varFile = ""
    varFile = varFile.join(varFileList)
    varFile = varFile.strip()
    varNameList = re.findall(r',(.*?)\Z',line)
    varName = ""
    varName = varName.join(varNameList)
    varName = varName.strip()
    fileName = varFile[1:]
    fileName = fileName[:-5]
    thisLine = "{} = {}.readline()".format(varName,fileName)
    return thisLine

def convWriteFile(line):
    varFileList = re.findall(r'WRITEFILE(.*?),',line)
    varFile = ""
    varFile = varFile.join(varFileList)
    varFile = varFile.strip()
    varNameList = re.findall(r',(.*?)\Z',line)
    varName = ""
    varName = varName.join(varNameList)
    varName = varName.strip()
    fileName = varFile[1:]
    fileName = fileName[:-5]
    thisLine = "{}.write({})".format(fileName,varName)
    return thisLine

def convCloseFile(line):
    varFileList = re.findall(r'CLOSEFILE(.*?)\Z',line)
    varFile = ""
    varFile = varFile.join(varFileList)
    varFile = varFile.strip()
    fileName = varFile[1:]
    fileName = fileName[:-5]
    thisLine = "{}.close()".format(fileName)
    return thisLine

def syntaxCheck():
    print('syntaxCheck() under-developing')

def outputFile(convFile):
    delBlankLines, delComments = fileConfig()
    currentWorkPath = os.path.dirname(__file__)
    genFilePath = currentWorkPath + "/convertedFile.txt"
    genTxtFile = open(genFilePath, 'w', encoding='utf-8')
    lineList = convFile.split("\n")
    for line in lineList:
        if delBlankLines == True:
            if line == "":
                continue
        if delComments == True:
            if line[0:1] == "#":
                continue       
        genTxtFile.write(line)
        genTxtFile.write("\n")

def fileConfig():
    delBlankLines = False
    delComments = False
    sepLine()
    print('Delete blank lines? key in 1 to confirm, enter to reject.')
    if input() == "1":
        delBlankLines = True
    print('Delete comments(#)? key in 1 to confirm, enter to reject.')
    if input() == "1":
        delComments = True
    return delBlankLines, delComments

def executeFile():
    print('executeFile() under-developing')

def main():
    txtfile = getFile()
    convFile = convertFile(txtfile)
    outputFile(convFile)
    executeFile()

main()