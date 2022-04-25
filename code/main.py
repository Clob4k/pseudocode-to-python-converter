"""
main.py
coding:utf-8

Developed by @Luke.Tang 2022
This program is for converting the pesudocode to the Python code.
For more information, please visit github.com/Clob4k/pesudocode-to-python-converter
"""

import pesudocode_converter as conv
# import user_interface as inf
import file_operation as file
import syntax_check as syn


#def interface_setup():
#    inf.window.mainloop()

def main():
    # interface_setup()
    txtfile = file.get_file()
    print("Convertion in process.")
    convfile = conv.convert_file(txtfile)
    file.out_put_file(convfile)


main()
