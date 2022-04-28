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
    txtfile = file.get_file()
    print("Convertion in process.")
    convfile = conv.convert_file(txtfile)
    file.out_put_file(convfile)


main()
