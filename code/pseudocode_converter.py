"""
pseudocode_converter.py
coding:utf-8

Developed by @Luke.Tang 2022
This program is for converting the pseudocode to the Python code.
For more information, please visit github.com/Clob4k/pseudocode-to-python-converter
"""

import regex as re

INDENTATION = "    "

def convert_file(txtfile):
    convFile = convert_key_words(txtfile)
    return convFile


def convert_key_words(txtfile):
    global INDENTATION
    convFileList = []
    convFlag = False
    caseFlag, repeatFlag = False, False
    convMod = ""

    for Index in range(len(txtfile)):
        line = txtfile[Index]
        nextLine = True

        if line == "\n":
            nextLine = False
        elif "//" in line:
            line = line.replace("//", "#")
            nextLine = False
        elif convFlag:
            if convMod == "CASE":
                if "ENDCASE" in line:
                    caseFlag = False
                    caselist.append(line)
                    line, inden, nextLine = direct_deletion_config()

                if caseFlag:
                    caselist.append(line)
                    line, inden, nextLine = direct_deletion_config()
                else:
                    convcaselist = pseudo_case(caselist)
                    convFileList.extend(convcaselist)
                    convFlag = False
                    convMod = ""

            elif convMod == "REPEAT":
                if "UNTIL" in line:
                    repeatFlag = False
                    repeatlist.append(line)
                    line, inden, nextLine = direct_deletion_config()

                if repeatFlag:
                    repeatlist.append(line)
                    line, inden, nextLine = direct_deletion_config()
                else:
                    convrepeatlist = pseudo_repeat(repeatlist)
                    convFileList.extend(convrepeatlist)
                    convFlag = False
                    convMod = ""
        else:

            if "CASE" in line and not "ENDCASE" in line:
                convFlag = True
                caseFlag = True
                convMod = "CASE"
                caselist = []
                caselist.append(line)
                line, inden, nextLine = direct_deletion_config()
            elif "REPEAT" in line:
                convFlag = True
                repeatFlag = True
                convMod = "REPEAT"
                repeatlist = []
                repeatlist.append(line)
                line, inden, nextLine = direct_deletion_config()
            else:
                inden = indentation_count(line)
                line = line.strip()
                line, inden, nextLine = direct_deletion(line, inden, nextLine)
                line = line_delection(line)
                line = line_conversion(line)

            line = pseudo_replace(line)
            # indentation addition
            line = INDENTATION * inden + line

        if not convFlag:
            convFileList.append(line)

        if nextLine == True:
            convFileList.append("\n")

    return convFileList


def line_conversion(line):
    if "LCASE" in line:
        line = pseudo_lcase(line)
    elif "UCASE" in line:
        line = pseudo_ucase(line)
    elif "RIGHT" in line:
        line = pseudo_right(line)
    elif "MID" in line:
        line = pseudo_mid(line)
    elif "OUTPUT" in line:
        line = pseudo_output(line)
    elif "DECLARE" in line:
        line = pseudo_declare(line)
    elif "OPENFILE" in line:
        line = pseudo_openfile(line)
    elif "READFILE" in line:
        line = pseudo_readfile(line)
    elif "WRITEFILE" in line:
        line = pseudo_writefile(line)
    elif "CLOSEFILE" in line:
        line = pseudo_closefile(line)
    elif "FOR" in line:
        line = pseudo_for(line)
    elif "IF" in line and not "ENDIF" in line:
        line = pseudo_if(line)
    elif "CALL" in line:
        line = pseudo_call(line)
    elif "PROCEDURE" in line:
        line = pseudo_procedure(line)
    elif "FUNCTION" in line:
        line = pseudo_function(line)
    return line


def indentation_count(line):
    blanks = 0
    while line[blanks] == " ":
        blanks = blanks + 4
    inden = int(blanks / 4)
    return inden


def direct_deletion(line, inden, nextLine):
    if "NEXT" in line:
        line, inden, nextLine = direct_deletion_config()
    elif "THEN" in line:
        line, inden, nextLine = direct_deletion_config()
    elif "ENDIF" in line:
        line, inden, nextLine = direct_deletion_config()
    elif "ENDWHILE" in line:
        line, inden, nextLine = direct_deletion_config()
    elif "ENDPROCEDURE" in line:
        line, inden, nextLine = direct_deletion_config()
    elif "ENDFUNCTION" in line:
        line, inden, nextLine = direct_deletion_config()
    return line, inden, nextLine


def direct_deletion_config():
    line = ""
    inden = 0
    nextLine = False
    return line, inden, nextLine


def line_delection(line):
    if "  ELSE" in line:
        line = line.replace("  ELSE", "else:")
    elif "LENGTH" in line:
        line = line.replace("LENGTH", "len")
    elif "WHILE" in line:
        line = line.replace("WHILE", "while")
        line = line + ":"
    elif "RETURN" in line and not "RETURNS" in line:
        line = line.replace("RETURN", "return")
    return line


def pseudo_replace(line):
    line = line.replace("NOT", "not")
    line = line.replace("OR", "or")
    line = line.replace("AND", "and")
    line = line.replace("TRUE", "True")
    line = line.replace("FALSE", "False")
    line = line.replace("←", "=")
    line = line.replace("&", "+")
    line = line.replace("<>", "!=")
    return line


def pseudo_lcase(line):
    varName = ""
    varName = varName.join(re.findall(r"LCASE\((.*?)\)", line))
    varName = varName.strip()
    thisLine = "{}.lower".format(varName)
    return thisLine


def pseudo_ucase(line):
    varName = ""
    varName = varName.join(re.findall(r"UCASE\((.*?)\)", line))
    varName = varName.strip()
    thisLine = "{}.upper".format(varName)
    return thisLine


def pseudo_right(line):
    varNameList = re.findall(r"RIGHT\((.*?),", line)
    varNumList = re.findall("\d+", line)
    integer = varNumList[-1]
    varName = ""
    varName = varName.join(varNameList)
    varName = varName.strip()
    thisLine = "{}[0:{}]".format(varName, integer)
    return thisLine


def pseudo_mid(line):
    varNameList = re.findall(r"\((.*?),", line)
    varNumList = re.findall("\d+", line)
    startVal = varNumList[-2]
    lenVal = varNumList[-1]
    startVal = str(eval(startVal) - 1)
    lenVal = str(eval(lenVal) + 1)
    varName = ""
    varName = varName.join(varNameList)
    varName = varName.strip()
    thisLine = "{}[{}:{}]".format(varName, startVal, lenVal)
    return thisLine


def pseudo_output(line):
    thisLine = line
    varName = ""
    varName = varName.join(re.findall(r"OUTPUT(.*?)\Z", line))
    varName = varName.strip()
    varName = varName.replace("&", "+")
    thisLine = "print({})".format(varName)
    return thisLine


def pseudo_declare(line):
    thisLine = line
    if "ARRAY" in line:
        varName = ""
        varName = varName.join(re.findall(r"DECLARE(.*?):", line))
        varName = varName.strip()
        thisLine = varName + " = []"
    else:
        thisLine = line.replace("DECLARE", "# DECLARE")
    return thisLine


def pseudo_for(line):
    varName = ""
    varName = varName.join(re.findall(r"FOR(.*?)←", line))
    varName = varName.strip()
    varRangeList = re.findall("\d+", line)
    iniVal = varRangeList[-2]
    endVal = varRangeList[-1]
    thisLine = "for {} in range({},{}):".format(varName, iniVal, endVal)
    return thisLine


def pseudo_if(line):
    if ">=" in line:
        varNameList = re.findall(r"IF(.*?)>=", line)
        varValueList = re.findall(r">=(.*?)\Z", line)
        symbol = ">="
    elif "<=" in line:
        varNameList = re.findall(r"IF(.*?)<=", line)
        varValueList = re.findall(r"<=(.*?)\Z", line)
        symbol = "<="
    elif "<>" in line:
        varNameList = re.findall(r"IF(.*?)<>", line)
        varValueList = re.findall(r"<>(.*?)\Z", line)
        symbol = "!="
    else:
        if "=" in line:
            varNameList = re.findall(r"IF(.*?)=", line)
            varValueList = re.findall(r"=(.*?)\Z", line)
            symbol = "=="
        elif ">" in line:
            varNameList = re.findall(r"IF(.*?)>", line)
            varValueList = re.findall(r">(.*?)\Z", line)
            symbol = ">"
        elif "<" in line:
            varNameList = re.findall(r"IF(.*?)<", line)
            varValueList = re.findall(r"<(.*?)\Z", line)
            symbol = "<"
        else:
            print("Error: {}".format(line))
    varName = ""
    varName = varName.join(varNameList)
    varName = varName.strip()
    varValue = ""
    varValue = varValue.join(varValueList)
    varValue = varValue.strip()
    thisLine = "if {} {} {}:".format(varName, symbol, varValue)
    return thisLine


def pseudo_case(caselist):
    global INDENTATION
    convcaselist = []
    forcount = 0
    inden = indentation_count(caselist[0])
    for caseline in caselist:
        caseline = caseline.strip()
        if "CASE" in caseline and not "ENDCASE" in caseline:
            identifer = pseudo_case_header(caseline)           
        elif "OTHERWISE" in caseline:
            statement = pseudo_case_statement(caseline)
            statement = line_conversion(statement)
            statement = pseudo_replace(statement)
            convcaselist.append(inden*INDENTATION + "else:")
            convcaselist.append("\n")
            statement = (inden+1)*INDENTATION + statement
            convcaselist.append(statement)
            convcaselist.append("\n")
        elif ":" in caseline and not "OTHERWISE" in caseline:
            statement = pseudo_case_statement(caseline)
            statement = line_conversion(statement)
            value = pesodo_case_value(caseline)
            statement = pseudo_replace(statement)
            if forcount == 0:
                convcaselist.append(inden*INDENTATION + "if {} == {}:".format(identifer, value))
                forcount += 1
            else:
                convcaselist.append(inden*INDENTATION + "elif {} == {}:".format(identifer, value))
            convcaselist.append("\n")
            statement = (inden+1)*INDENTATION + statement
            convcaselist.append(statement)
            convcaselist.append("\n")
        elif "ENDCASE" in caseline:
            continue
        else:
            statement = line_conversion(caseline)
            statement = pseudo_replace(statement)
            statement = (inden+1)*INDENTATION + statement
            convcaselist.append(statement)
            convcaselist.append("\n")
    return convcaselist


def pseudo_case_header(caseline):
    identifer = ""
    identifer = identifer.join(re.findall(r"OF(.*?)\Z", caseline))
    identifer = identifer.strip()
    return identifer


def pseudo_case_statement(caseline):
    statement = ""
    statement = statement.join(re.findall(r":(.*?)\Z", caseline))
    statement = statement.strip()
    return statement


def pesodo_case_value(caseline):
    value = ""
    value = value.join(re.findall(r"\A(.*?):", caseline))
    value = value.strip()
    return value


def pseudo_repeat(repeatlist):
    global INDENTATION
    convrepeatlist, iterativepart = [], []
    inden = indentation_count(repeatlist[0])
    for repeatline in repeatlist:
        repeatline = repeatline.strip()
        if "REPEAT" in repeatline:
            continue
        elif "UNTIL" in repeatline:
            convrepeatlist.extend(iterativepart)
            condition = pseudo_repeat_condition(repeatline)
            condition = line_conversion(condition)
            condition = pseudo_replace(condition)
            convrepeatlist.append(inden*INDENTATION + "while {}:".format(condition))
            convrepeatlist.append("\n")
            for elements in iterativepart:
                elements = (inden+1)*INDENTATION + elements
                convrepeatlist.append(elements)
        else:
            statement = line_conversion(repeatline)
            statement = pseudo_replace(statement)
            statement = inden*INDENTATION + statement
            iterativepart.append(statement)
            iterativepart.append("\n")
    return convrepeatlist


def pseudo_repeat_condition(repeatline):
    condition = ""
    condition = condition.join(re.findall(r"UNTIL(.*?)\Z", repeatline))
    condition = condition.strip()
    return condition

def pseudo_openfile(line):
    if "READ" in line:
        openMod = "r"
    elif "WRITE" in line:
        openMod = "w"
    elif "APPEND" in line:
        openMod = "a"
    varName = ""
    varName = varName.join(re.findall(r"OPENFILE(.*?)FOR", line))
    varName = varName.strip()
    fileName = varName[1:]
    fileName = fileName[:-5]
    thisLine = "{} = open({},'{}')".format(fileName, varName, openMod)
    return thisLine


def pseudo_readfile(line):
    varFile = ""
    varFile = varFile.join(re.findall(r"READFILE(.*?),", line))
    varFile = varFile.strip()
    varName = ""
    varName = varName.join(re.findall(r",(.*?)\Z", line))
    varName = varName.strip()
    fileName = varFile[1:]
    fileName = fileName[:-5]
    thisLine = "{} = {}.readline()".format(varName, fileName)
    return thisLine


def pseudo_call(line):
    thisLine = line
    if ("(" or ")") in line:
        varName = ""
        varName = varName.join(re.findall(r"\((.*?)\)", line))
        varName = varName.strip()
        funName = ""
        funName = funName.join(re.findall(r"CALL(.*?)\(", line))
        funName = funName.strip()
        thisLine = "{}({})".format(funName, varName)
    else:
        funName = ""
        funName = funName.join(re.findall(r"CALL(.*?)\Z", line))
        funName = funName.strip()
        thisLine = funName + "()"
    return thisLine


def pseudo_procedure(line):
    thisLine = line
    paraNum = line.count(":")
    if paraNum == 1:
        varName = ""
        varName = varName.join(re.findall(r"\((.*?):", line))
        varName = varName.strip()
        funName = ""
        funName = funName.join(re.findall(r"PROCEDURE(.*?)\(", line))
        funName = funName.strip()
        thisLine = "def {}({}):".format(funName, varName)
    elif paraNum == 0:
        funName = ""
        funName = funName.join(re.findall(r"PROCEDURE(.*?)\Z", line))
        funName = funName.strip()
        thisLine = "def {}():".format(funName)
    elif paraNum > 1:
        funName = ""
        funName = funName.join(re.findall(r"PROCEDURE(.*?)\(", line))
        funName = funName.strip()
        thisLine = "def {}()".format(funName)
        varName = ""
        varName = varName.join(re.findall(r"\((.*?):", line))
        varName = varName.strip()
        paraName = ""
        paraName = ",".join(re.findall(r",(.*?):", line))
        paraName = paraName.strip()
        parameter = varName + "," + paraName
        parameter = parameter.replace(" ", "")
        thisLine = "def {}({}):".format(funName, parameter)
    return thisLine


def pseudo_function(line):
    thisLine = line
    paraNum = line.count(":")
    if paraNum == 1:
        varName = ""
        varName = varName.join(re.findall(r"\((.*?):", line))
        varName = varName.strip()
        funName = ""
        funName = funName.join(re.findall(r"FUNCTION(.*?)\(", line))
        funName = funName.strip()
        thisLine = "def {}({}):".format(funName, varName)
    elif paraNum == 0:
        funName = ""
        funName = funName.join(re.findall(r"FUNCTION(.*?)RETURNS", line))
        funName = funName.strip()
        thisLine = "def {}():".format(funName)
    elif paraNum > 1:
        funName = ""
        funName = funName.join(re.findall(r"FUNCTION(.*?)\(", line))
        funName = funName.strip()
        thisLine = "def {}()".format(funName)
        varName = ""
        varName = varName.join(re.findall(r"\((.*?):", line))
        varName = varName.strip()
        paraName = ""
        paraName = ",".join(re.findall(r",(.*?):", line))
        paraName = paraName.strip()
        parameter = varName + "," + paraName
        parameter = parameter.replace(" ", "")
        thisLine = "def {}({}):".format(funName, parameter)
    return thisLine


def pseudo_writefile(line):
    varFile = ""
    varFile = varFile.join(re.findall(r"WRITEFILE(.*?),", line))
    varFile = varFile.strip()
    varName = ""
    varName = varName.join(re.findall(r",(.*?)\Z", line))
    varName = varName.strip()
    fileName = varFile[1:]
    fileName = fileName[:-5]
    thisLine = "{}.write({})".format(fileName, varName)
    return thisLine


def pseudo_closefile(line):
    varFile = ""
    varFile = varFile.join(re.findall(r"CLOSEFILE(.*?)\Z", line))
    varFile = varFile.strip()
    fileName = varFile[1:]
    fileName = fileName[:-5]
    thisLine = "{}.close()".format(fileName)
    return thisLine
