"""
main.py
coding:utf-8

Developed by @Luke.Tang 2022
This program is for converting the pseudocode to the Python code.
For more information, please visit github.com/Clob4k/pseudocode-to-python-converter
"""

import pseudocode_converter as conv
import file_operation as file


def main():
    textfile = file.get_file()
    print("Conversion in process.")
    convert_file = conv.convert_file(textfile)
    file.out_put_file(convert_file)


main()
