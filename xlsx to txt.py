"""
Takes the xl sheets with the information to text.

Should read from input.xlsx in IO and output data to the texts files in the specified format. 

Use openpyxl to read data from the spreadsheet,

Keep all of the program inside of functions so it can be accessed as an import from "main.py"
"""

from openpyxl import load_workbook


# write you main code in here.
def xlsx_to_txt () -> None:
    """
    Reads the input spreadsheet and converts each page into text.
    Saves in individual text files.
    """
    
files = ['students.txt', 'teachers.txt', 'subjects.txt', 'rooms.txt'] #file name to output to

for i in range(4):
    wb = load_workbook("IO\input.xlsx") #opens input.xlsx
    wb.active=wb.worksheets[i]
    sheet = wb.active
    maxRow = sheet.max_row
    maxColumn=sheet.max_column
    for x in range(1, maxRow + 1):
        for y in range(1, maxColumn +1):
            cell_obj = sheet.cell(row=x, column=y)
            print(cell_obj.value, end=' | ', file=open(files[i], 'a'))
        print('', file=open(files[i], 'a'))

# write code in here if you only want it to be accessed when this file is run directly, not as an import
def main () -> None:
    pass

if __name__ == '__main__':
    main ()

xlsx_to_txt()
