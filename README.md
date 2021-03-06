# pseudocode-to-python-converter

* Individual project by _Luke.Tang_

* Started on _Jan 16th 2022_

* The program is designed to convert pseudocode in text file into python code.

* Develop environment: _python 3.10.2_

# Limitations

You may still obtain output files when operating the program without encountering any errors in following situations. However, there is no guarantee to generate accurate python format files.

* pseudocode to be converted should not have **any keywords** in variable names.

* Multiline command without pre-definition is not accepted.

* Unexpected brackets ``()`` may lead to serious errors.

* Unexpected blanks preceded, or implemented in commands e.g. ``LENGTH (ThisString)`` will not be accepted, as if it is grammatically correct.

* This program is **not** capable of handling pseudocode with :

1. any command words that are not mentioned in **Accepted pseudocode format** section.

2. logical operations ``AND, OR, NOT`` within ``IF, WHILE, CASE, REPEAT UNTIL`` operation.

3. ``BYREF, EOF`` operations.

4. **user-defined data types**

# Accepted pseudocode format

* All Syntax follow the Cambridge International AS & A Level Computer Science 9618 - pseudocode Guide for Teachers.

* Command words implemented should be in **UPPER** case.

* Variable identifiers are recommended to be in **CamelCaps** while under-scores are also acceptable.

* **Indentations** should be made where necessary and appropriate.

* **Comments** are preceded by ``//``.

## Data types

* The program accepts ``INTEGER, REAL, CHAR, STRING, BOOLEAN`` as data types.

* The converted file follows original identifiers.

* Variable declaration will be converted into comments since it does not exist in python.

* Constants will be regarded as variables even if it may not be altered.

## Assignment

* Pay attention that symbol for assignment is ``←`` instead of ``<-`` .

```
<variableA> ← <variableB> 
```

## Arrays

* one-dimensional : 
```
DECLARE <identifier> : ARRAY[<lower>,<upper>] OF <data type>
```

* two-dimensional : 
```
DECLARE <identifier> : ARRAY[<lower1>:<upper1>,<lower2>:<upper2>] OF <data type>
```

* fetch values :    
```
<identifier>[index]
```

## Common operations

* Symbols and operations :

| symbol | operation                |
|:------:|--------------------------|
|   \+   | Addition                 |
|   \-   | Subtraction              |
|   \*   | Multiplication           |
|   /    | Division                 |
|   \>   | Greater than             |
|   <    | Less than                |
|  \>=   | Greater than or equal to |
|   <=   | Less than or equal to    |
|   =    | Equal to                 |
|   <>   | Not equal to             |
|   &    | Concatenate two strings  |

* Commands :

```
INPUT<identifier>
```

```
OUTPUT<value(s)>
```

```
<statement> AND <statement>
```

```
<statement> OR <statement>
```

```
NOT <statement>
```

```
RIGHT(ThisString: STRING, x:INTEGER)
```

```
LENGTH(ThisString: STRING)
```

```
MID(ThisString: STRING, x:INTEGER, y:INTEGER)
```

```
LCASE(ThisChar: CHAR)
```

```
UCASE(ThisChar: CHAR)
```

## Selection

Noted that ``THEN`` only has two spaces of indentation, while the statement has four spaces (a tab) indentation.

And ``ELSE`` lines up with ``THEN`` . Wrong format may lead to serious errors. 

Do check the "ENDCASE" for ``CASE`` statement since it is crucial for conversion.

```
IF <condition>
  THEN
    <statement(s)>
ENDIF
```

```
IF <condition>
  THEN
    <statement(s)>
  ELSE
    <statement(s)>
ENDIF
```

```
CASE OF <identifier>
    <value1> : <statement1>
               <statement2>
    <value2> : <statement1>
               <statement2>
    OTHERWISE: <statement1>
               <statement2>
ENDCASE
```

## Iteration

```
FOR <indentifer> ← <value1> TO <value2>
    <statements>
NEXT <identifier>
```

```
REPEAT
    <statement(s)>
UNTIL <condition>
```

```
WHILE <condition>
    <statement(s)>
ENDWHILE
```

## Procedure and functions

```
PROCEDURE <identifier>
    <statement(s)>
ENDPROCEDURE
```

```
PROCEDURE <identifier>(<para1>:<datatype>, <para2>:<datatype>)
    <statement(s)>
ENDPROCEDURE
```

```
CALL <identifier>
```

```
CALL <identifier>(Value1, Value2)
```

```
FUNCTION <identifier> RETURNS <data type>
    <statement(s)>
ENDFUNCTION
```

```
FUNCTION <identifier>(<para1>:<datatype>, <para2>:<datatype>) RETURNS <data type>
    <statement(s)>
ENDFUNCTION
```

```
PROCEDURE <identifier>(BYREF <para1>:<datatype>, <para2>:<datatype>)
    <statement(s)>
ENDPROCEDURE
```
Noted that ``BYREF`` applies to all the parameters in the procedure.

In other words, in a particular procedure, parameters can only be passed by reference or by values.

## File handling

```
OPENFILE <File identifier> FOR <File mode>

<File mode> : READ / WRITE / APPEND
```

```
READFILE <File identifier>, <variable: STRING>
```

```
EOF(<File identifier>)
```

```
WRITEFILE <File identifier>, <data>
```

```
CLOSEFILE <File identifier>
```

## User-defined data types

```
TYPE <identifier> = (value1, value2, value3, ...)
```

```
TYPE <pointer> = ^<Typename>
```

```
Type <identifier1>
    DECLARE <identifier2> : <data type>
    DECLARE <identifier3> : <data type>
    ...
ENDTYPE
```