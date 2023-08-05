# -*- coding: utf-8 -*-
from xlrd import open_workbook

wb = open_workbook("excel/data/Reference Data entry/data entry.xlsx")

for s in wb.sheets():
    print "sheet:", s.name
    for row in range(s.nrows):
        values = []
        for col in range(s.ncols):
            values.append(s.cell(row,col).value.decode('utf'))
        print ",".join(values)

