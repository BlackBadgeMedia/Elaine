"""
Takes the xl sheets with the information to text.

Should read from input.xlsx in IO and output data to the texts files in the specified format. 

Use openpyxl to read data from the spreadsheet,

Keep all of the program inside of functions so it can be accessed as an import from "main.py"
"""

from openpyxl import Workbook

# write you main code in here.
def xlsx_to_txt () -> None:
    """
    Reads the input spreadsheet and converts each page into text.
    Saves in individual text files.
    """
    pass




# write code in here if you only want it to be accessed when this file is run directly, not as an import
def main () -> None:
    pass

if __name__ == '__main__':
    main ()
