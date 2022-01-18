# pesudocode-to-python-converter
Individual project by Luke.Tang

Started on Jan 16th 2022

The program is designed to convert pesudocode in text file into python code.

version: python 3.9.6

# accepted pesudocode format
All Syntax follows the Cambridge International AS & A Level Computer Science 9618 - Pesudocode Guide for Teachers

Command words implemented should be in UPPER case.

Indentations should be made where necessary.

Comments are preceded by //.

**data types**

The program accepts INTEGER, REAL, CHAR, STRING, BOOLEAN as data types.

The converted file follows original identifiers.

Variable declaration will not be converted since it does not exists in python.

Constant will be regarded as a variable.

**assignment:** 

{variableA} ← {variableB} 

**arrays:**

one-dimensional: DECLARE {identifer} : ARRAY[{lower},{upper}] OF {data type}

two-dimensional: DECLARE {identifer} : ARRAY[{lower1}:{upper1},{lower2}:{upper2}] OF {data type}

fetch values:    {identifer}[index]

**common operations**

INPUT{identifer}

OUTPUT{value(s)}

"+"   Addition

"-"   Subtraction

"*"   Multiplication

"/"   Division

">"   Greater than

"<"   Less than

">="  Greater than or equal to

"<="  Less than or equal to

"="   equal to

"<>"  not equal to

{statement} AND {statement}

{statement} OR {statement}

NOT {statement}

RIGHT(ThisString: STRING, x:INTEGER)

LENGTH(ThisString: STRING)

MID(ThisString: STRING, x:INTEGER, y:INTEGER)

LCASE(ThisChar: CHAR)

UCASE(ThisChar: CHAR)

&   concatenate two strings

**selection**

IF {condition}
    THEN
        {statement(s)}
ENDIF

IF {condition}
    THEN
        {statement(s)}
    ELSE
        {statement(s)}
ENDIF

CASE OF {identifer}
    {value1} : {statement1}
               {statement2}
    {value2} : {statement1}
               {statement2}
    OTHERWISE: {statement1}
               {statement2}
ENDCASE

**iteration**

`
FOR {indentifer} ← {value1} TO {value2}
    {statements}
NEXT {identifer}
`

REPEAT
    {statement(s)}
UNTIL {condition}

WHILE {condition}
    {statement(s)}
ENDWHILE

**procedure and functions**

PROCEDURE {identifer}
    {statement(s)}
ENDPROCEDURE

PROCEDURE {identifer}({para1}:{datatype}, {para2}:{datatype})
    {statement(s)}
ENDPROCEDURE

CALL {identifer}

CALL {identifer}(Value1, Value2)

FUNCTION {identifer} RETURNS {data type}
    {statement(s)}
ENDFUNCTION

FUNCTION {identifer}({para1}:{datatype}, {para2}:{datatype}) RETURNS {data type}
    {statement(s)}
ENDFUNCTION

PROCEDURE {identifier}(BYREF {para1}:{datatype}, {para2}:{datatype})
    {statement(s)}
ENDPROCEDURE

**file handling**

OPENFILE {File identifier} FOR {File mode}

{File mode} : READ / WRITE / APPEND

READFILE {File identifier}, {variable: STRING}

EOF({File identifier})

WRITEFILE {File identifier}, {data}

CLOSEFILE {File identifier}

**user-defined data types**

to be include 