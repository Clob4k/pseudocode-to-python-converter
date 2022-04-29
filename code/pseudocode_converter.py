"""
pseudocode_converter.py
coding:utf-8

Developed by @Luke.Tang 2022
This program is for converting the pseudocode to the Python code.
For more information, please visit github.com/Clob4k/pseudocode-to-python-converter
"""

import regex as re

INDENTATION = "    "


def convert_file(textfile):
    converted_file = convert_key_words(textfile)
    return converted_file


def convert_key_words(textfile):
    global INDENTATION
    case_list, repeat_list, converted_file_list = [], [], []
    convert_flag, case_flag, repeat_flag = False, False, False
    convert_mod = ""

    for Index in range(len(textfile)):
        line = textfile[Index]
        nextline = True

        if line == "\n":
            nextline = False
        elif "//" in line:
            line = line.replace("//", "#")
            nextline = False
        elif convert_flag:
            if convert_mod == "CASE":
                if "ENDCASE" in line:
                    case_flag = False
                    case_list.append(line)
                    line, indent, nextline = direct_deletion_config()

                if case_flag:
                    case_list.append(line)
                    line, indent, nextline = direct_deletion_config()
                else:
                    converted_case_list = pseudo_case(case_list)
                    converted_file_list.extend(converted_case_list)
                    convert_flag = False
                    convert_mod = ""

            elif convert_mod == "REPEAT":
                if "UNTIL" in line:
                    repeat_flag = False
                    repeat_list.append(line)
                    line, indent, nextline = direct_deletion_config()

                if repeat_flag:
                    repeat_list.append(line)
                    line, indent, nextline = direct_deletion_config()
                else:
                    converted_repeat_list = pseudo_repeat(repeat_list)
                    converted_file_list.extend(converted_repeat_list)
                    convert_flag = False
                    convert_mod = ""
        else:

            if "CASE" in line and not ("ENDCASE" in line):
                convert_flag = True
                case_flag = True
                convert_mod = "CASE"
                case_list = [line]
                line, indent, nextline = direct_deletion_config()
            elif "REPEAT" in line:
                convert_flag = True
                repeat_flag = True
                convert_mod = "REPEAT"
                repeat_list = [line]
                line, indent, nextline = direct_deletion_config()
            else:
                indent = indentation_count(line)
                line = line.strip()
                line, indent, nextline = direct_deletion(line, indent, nextline)
                line = line_del(line)
                line = line_conversion(line)

            line = pseudo_replace(line)
            # indentation addition
            line = INDENTATION * indent + line

        if not convert_flag:
            converted_file_list.append(line)

        if nextline:
            converted_file_list.append("\n")

    return converted_file_list


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
    elif "IF" in line and not ("ENDIF" in line):
        if ("AND" in line) or ("OR" in line) or ("NOT" in line):
            line = pseudo_bool_if(line)
            line = pseudo_replace(line)
        else:
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
    indent = int(blanks / 4)
    return indent


def direct_deletion(line, indent, nextline):
    if "NEXT" in line:
        line, indent, nextline = direct_deletion_config()
    elif "THEN" in line:
        line, indent, nextline = direct_deletion_config()
    elif "ENDIF" in line:
        line, indent, nextline = direct_deletion_config()
    elif "ENDWHILE" in line:
        line, indent, nextline = direct_deletion_config()
    elif "ENDPROCEDURE" in line:
        line, indent, nextline = direct_deletion_config()
    elif "ENDFUNCTION" in line:
        line, indent, nextline = direct_deletion_config()
    return line, indent, nextline


def direct_deletion_config():
    line = ""
    indent = 0
    nextline = False
    return line, indent, nextline


def line_del(line):
    if "  ELSE" in line:
        line = line.replace("  ELSE", "else:")
    elif "LENGTH" in line:
        line = line.replace("LENGTH", "len")
    elif "WHILE" in line:
        line = line.replace("WHILE", "while")
        line = line + ":"
    elif "RETURN" in line and not ("RETURNS" in line):
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
    variable_name = ""
    variable_name = variable_name.join(re.findall(r"LCASE\((.*?)\)", line))
    variable_name = variable_name.strip()
    this_line = "{}.lower".format(variable_name)
    return this_line


def pseudo_ucase(line):
    variable_name = ""
    variable_name = variable_name.join(re.findall(r"UCASE\((.*?)\)", line))
    variable_name = variable_name.strip()
    this_line = "{}.upper".format(variable_name)
    return this_line


def pseudo_right(line):
    variable_nameList = re.findall(r"RIGHT\((.*?),", line)
    varNumList = re.findall("\\d+", line)
    integer = varNumList[-1]
    variable_name = ""
    variable_name = variable_name.join(variable_nameList)
    variable_name = variable_name.strip()
    this_line = "{}[0:{}]".format(variable_name, integer)
    return this_line


def pseudo_mid(line):
    variable_nameList = re.findall(r"\((.*?),", line)
    varNumList = re.findall("\\d+", line)
    startVal = varNumList[-2]
    lenVal = varNumList[-1]
    startVal = str(eval(startVal) - 1)
    lenVal = str(eval(lenVal) + 1)
    variable_name = ""
    variable_name = variable_name.join(variable_nameList)
    variable_name = variable_name.strip()
    this_line = "{}[{}:{}]".format(variable_name, startVal, lenVal)
    return this_line


def pseudo_output(line):
    variable_name = ""
    variable_name = variable_name.join(re.findall(r"OUTPUT(.*?)\Z", line))
    variable_name = variable_name.strip()
    variable_name = variable_name.replace("&", "+")
    this_line = "print({})".format(variable_name)
    return this_line


def pseudo_declare(line):
    if "ARRAY" in line:
        variable_name = ""
        variable_name = variable_name.join(re.findall(r"DECLARE(.*?):", line))
        variable_name = variable_name.strip()
        this_line = variable_name + " = []"
    else:
        this_line = line.replace("DECLARE", "# DECLARE")
    return this_line


def pseudo_for(line):
    variable_name = ""
    variable_name = variable_name.join(re.findall(r"FOR(.*?)←", line))
    variable_name = variable_name.strip()
    varRangeList = re.findall("\\d+", line)
    iniVal = varRangeList[-2]
    endVal = varRangeList[-1]
    this_line = "for {} in range({},{}):".format(variable_name, iniVal, endVal)
    return this_line


def pseudo_if(line):
    variable_nameList = []
    varValueList = []
    symbol = ""
    if ">=" in line:
        variable_nameList = re.findall(r"IF(.*?)>=", line)
        varValueList = re.findall(r">=(.*?)\Z", line)
        symbol = ">="
    elif "<=" in line:
        variable_nameList = re.findall(r"IF(.*?)<=", line)
        varValueList = re.findall(r"<=(.*?)\Z", line)
        symbol = "<="
    elif "<>" in line:
        variable_nameList = re.findall(r"IF(.*?)<>", line)
        varValueList = re.findall(r"<>(.*?)\Z", line)
        symbol = "!="
    else:
        if "=" in line:
            variable_nameList = re.findall(r"IF(.*?)=", line)
            varValueList = re.findall(r"=(.*?)\Z", line)
            symbol = "=="
        elif ">" in line:
            variable_nameList = re.findall(r"IF(.*?)>", line)
            varValueList = re.findall(r">(.*?)\Z", line)
            symbol = ">"
        elif "<" in line:
            variable_nameList = re.findall(r"IF(.*?)<", line)
            varValueList = re.findall(r"<(.*?)\Z", line)
            symbol = "<"
        else:
            print("Error: {}".format(line))
            print("Unknown operator in if statement")
    variable_name = ""
    variable_name = variable_name.join(variable_nameList)
    variable_name = variable_name.strip()
    varValue = ""
    varValue = varValue.join(varValueList)
    varValue = varValue.strip()
    this_line = "if {} {} {}:".format(variable_name, symbol, varValue)
    return this_line
    

def pseudo_bool_if(line):
    bool_location = find_bool_location(line)
    bool_type = find_bool_type(line, bool_location)
    right_side = ""
    left_side = ""
    if bool_type == "NOT":
        line = line.replace("NOT", "not")
    elif bool_type == "OR":
        left_side = line[:bool_location]
        right_side = line[:bool_location + 1]
    elif bool_type == "AND":
        left_side = line[:bool_location]
        right_side = line[:bool_location + 2]

    if ("AND" in right_side) or ("OR" in right_side):
        right_side = find_bool_right(right_side)

    if bool_type == "NOT":
        line = pseudo_if(line)
    elif bool_type == "OR":
        line = pseudo_if(left_side) + "or" + right_side
    elif bool_type == "AND":
        line = pseudo_if(left_side) + "and" + right_side
    return line


def find_bool_location(line):
    location_list = [line.find("AND"), line.find("OR"), line.find("NOT")]
    location_list.sort()
    for i in location_list:
        if i != -1:
            return i
    return -1


def find_bool_type(line, bool_location):
    bool_char = ""
    if bool_location == -1:
        print("Error: {}".format(line))
        print("Unknown bool operator")
    else:
        bool_char = line[bool_location]
        if bool_char == "A":
            bool_char = "and"
        elif bool_char == "O":
            bool_char = "or"
        elif bool_char == "N":
            bool_char = "not"
        else:
            print("Error: {}".format(line))
            print("Unknown bool operator")
    return bool_char


def find_bool_right(line):
    bool_location = find_bool_location(line)
    bool_type = find_bool_type(line, bool_location)
    if bool_type == "OR":
        left_side = line[:bool_location]
        right_side = line[:bool_location + 1]
        if ("AND" in right_side) or ("OR" in right_side):
            right_side = find_bool_right(right_side)
        line = left_side + " or " + right_side
    elif bool_type == "AND":
        left_side = line[:bool_location]
        right_side = line[:bool_location + 2]
        if ("AND" in right_side) or ("OR" in right_side):
            right_side = find_bool_right(right_side)
        line = left_side + " and " + right_side
    return line


def pseudo_case(case_list):
    identifier = ""
    global INDENTATION
    convert_case_list = []
    count = 0
    indent = indentation_count(case_list[0])
    for case_line in case_list:
        case_line = case_line.strip()
        if "CASE" in case_line and not ("ENDCASE" in case_line):
            identifier = pseudo_case_header(case_line)
        elif "OTHERWISE" in case_line:
            statement = pseudo_case_statement(case_line)
            statement = line_conversion(statement)
            statement = pseudo_replace(statement)
            convert_case_list.append(indent * INDENTATION + "else:")
            convert_case_list.append("\n")
            statement = (indent + 1) * INDENTATION + statement
            convert_case_list.append(statement)
            convert_case_list.append("\n")
        elif ":" in case_line and not ("OTHERWISE" in case_line):
            statement = pseudo_case_statement(case_line)
            statement = line_conversion(statement)
            value = pseudo_case_value(case_line)
            statement = pseudo_replace(statement)
            if count == 0:
                convert_case_list.append(indent * INDENTATION + "if {} == {}:".format(identifier, value))
                count += 1
            else:
                convert_case_list.append(indent * INDENTATION + "elif {} == {}:".format(identifier, value))
            convert_case_list.append("\n")
            statement = (indent + 1) * INDENTATION + statement
            convert_case_list.append(statement)
            convert_case_list.append("\n")
        elif "ENDCASE" in case_line:
            continue
        else:
            statement = line_conversion(case_line)
            statement = pseudo_replace(statement)
            statement = (indent + 1) * INDENTATION + statement
            convert_case_list.append(statement)
            convert_case_list.append("\n")
    return convert_case_list


def pseudo_case_header(case_line):
    identifier = ""
    identifier = identifier.join(re.findall(r"OF(.*?)\Z", case_line))
    identifier = identifier.strip()
    return identifier


def pseudo_case_statement(case_line):
    statement = ""
    statement = statement.join(re.findall(r":(.*?)\Z", case_line))
    statement = statement.strip()
    return statement


def pseudo_case_value(case_line):
    value = ""
    value = value.join(re.findall(r"\A(.*?):", case_line))
    value = value.strip()
    return value


def pseudo_repeat(repeat_list):
    global INDENTATION
    converted_repeat_list, iterative_part = [], []
    indent = indentation_count(repeat_list[0])
    for repeat_line in repeat_list:
        repeat_line = repeat_line.strip()
        if "REPEAT" in repeat_line:
            continue
        elif "UNTIL" in repeat_line:
            converted_repeat_list.extend(iterative_part)
            condition = pseudo_repeat_condition(repeat_line)
            condition = line_conversion(condition)
            condition = pseudo_replace(condition)
            converted_repeat_list.append(indent * INDENTATION + "while {}:".format(condition))
            converted_repeat_list.append("\n")
            for elements in iterative_part:
                elements = (indent + 1) * INDENTATION + elements
                converted_repeat_list.append(elements)
        else:
            statement = line_conversion(repeat_line)
            statement = pseudo_replace(statement)
            statement = indent * INDENTATION + statement
            iterative_part.append(statement)
            iterative_part.append("\n")
    return converted_repeat_list


def pseudo_repeat_condition(repeat_line):
    condition = ""
    condition = condition.join(re.findall(r"UNTIL(.*?)\Z", repeat_line))
    condition = condition.strip()
    return condition


def pseudo_openfile(line):
    open_mod = ""
    if "READ" in line:
        open_mod = "r"
    elif "WRITE" in line:
        open_mod = "w"
    elif "APPEND" in line:
        open_mod = "a"
    variable_name = ""
    variable_name = variable_name.join(re.findall(r"OPENFILE(.*?)FOR", line))
    variable_name = variable_name.strip()
    fileName = variable_name[1:]
    fileName = fileName[:-5]
    this_line = "{} = open({},'{}')".format(fileName, variable_name, open_mod)
    return this_line


def pseudo_readfile(line):
    variable_file = ""
    variable_file = variable_file.join(re.findall(r"READFILE(.*?),", line))
    variable_file = variable_file.strip()
    variable_name = ""
    variable_name = variable_name.join(re.findall(r",(.*?)\Z", line))
    variable_name = variable_name.strip()
    fileName = variable_file[1:]
    fileName = fileName[:-5]
    this_line = "{} = {}.readline()".format(variable_name, fileName)
    return this_line


def pseudo_call(line):
    if ("(" or ")") in line:
        variable_name = ""
        variable_name = variable_name.join(re.findall(r"\((.*?)\)", line))
        variable_name = variable_name.strip()
        function_name = ""
        function_name = function_name.join(re.findall(r"CALL(.*?)\(", line))
        function_name = function_name.strip()
        this_line = "{}({})".format(function_name, variable_name)
    else:
        function_name = ""
        function_name = function_name.join(re.findall(r"CALL(.*?)\Z", line))
        function_name = function_name.strip()
        this_line = function_name + "()"
    return this_line


def pseudo_procedure(line):
    this_line = line
    parameter_number = line.count(":")
    if parameter_number == 1:
        variable_name = ""
        variable_name = variable_name.join(re.findall(r"\((.*?):", line))
        variable_name = variable_name.strip()
        function_name = ""
        function_name = function_name.join(re.findall(r"PROCEDURE(.*?)\(", line))
        function_name = function_name.strip()
        this_line = "def {}({}):".format(function_name, variable_name)
    elif parameter_number == 0:
        function_name = ""
        function_name = function_name.join(re.findall(r"PROCEDURE(.*?)\Z", line))
        function_name = function_name.strip()
        this_line = "def {}():".format(function_name)
    elif parameter_number > 1:
        function_name = ""
        function_name = function_name.join(re.findall(r"PROCEDURE(.*?)\(", line))
        function_name = function_name.strip()
        variable_name = ""
        variable_name = variable_name.join(re.findall(r"\((.*?):", line))
        variable_name = variable_name.strip()
        parameter_name = ",".join(re.findall(r",(.*?):", line))
        parameter_name = parameter_name.strip()
        parameter = variable_name + "," + parameter_name
        parameter = parameter.replace(" ", "")
        this_line = "def {}({}):".format(function_name, parameter)
    return this_line


def pseudo_function(line):
    this_line = line
    parameter_number = line.count(":")
    if parameter_number == 1:
        variable_name = ""
        variable_name = variable_name.join(re.findall(r"\((.*?):", line))
        variable_name = variable_name.strip()
        function_name = ""
        function_name = function_name.join(re.findall(r"FUNCTION(.*?)\(", line))
        function_name = function_name.strip()
        this_line = "def {}({}):".format(function_name, variable_name)
    elif parameter_number == 0:
        function_name = ""
        function_name = function_name.join(re.findall(r"FUNCTION(.*?)RETURNS", line))
        function_name = function_name.strip()
        this_line = "def {}():".format(function_name)
    elif parameter_number > 1:
        function_name = ""
        function_name = function_name.join(re.findall(r"FUNCTION(.*?)\(", line))
        function_name = function_name.strip()
        variable_name = ""
        variable_name = variable_name.join(re.findall(r"\((.*?):", line))
        variable_name = variable_name.strip()
        parameter_name = ",".join(re.findall(r",(.*?):", line))
        parameter_name = parameter_name.strip()
        parameter = variable_name + "," + parameter_name
        parameter = parameter.replace(" ", "")
        this_line = "def {}({}):".format(function_name, parameter)
    return this_line


def pseudo_writefile(line):
    variable_file = ""
    variable_file = variable_file.join(re.findall(r"WRITEFILE(.*?),", line))
    variable_file = variable_file.strip()
    variable_name = ""
    variable_name = variable_name.join(re.findall(r",(.*?)\Z", line))
    variable_name = variable_name.strip()
    fileName = variable_file[1:]
    fileName = fileName[:-5]
    this_line = "{}.write({})".format(fileName, variable_name)
    return this_line


def pseudo_closefile(line):
    variable_file = ""
    variable_file = variable_file.join(re.findall(r"CLOSEFILE(.*?)\Z", line))
    variable_file = variable_file.strip()
    fileName = variable_file[1:]
    fileName = fileName[:-5]
    this_line = "{}.close()".format(fileName)
    return this_line
