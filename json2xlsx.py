import json
import os
from typing import Optional
from dashreq import get_dash_data

from xlsxwriter import Workbook
from xlsxwriter.worksheet import (Worksheet, cell_number_tuple,
                                  cell_string_tuple)


def get_column_width(worksheet: Worksheet, column: int) -> Optional[int]:
    """Get the max column width in a `Worksheet` column."""
    strings = getattr(worksheet, '_ts_all_strings', None)
    if strings is None:
        strings = worksheet._ts_all_strings = sorted(
            worksheet.str_table.string_table,
            key=worksheet.str_table.string_table.__getitem__)
    lengths = set()
    for row_id, colums_dict in worksheet.table.items():  # type: int, dict
        data = colums_dict.get(column)
        if not data:
            continue
        if type(data) is cell_string_tuple:
            iter_length = len(strings[data.string])
            if not iter_length:
                continue
            lengths.add(iter_length)
            continue
        if type(data) is cell_number_tuple:
            iter_length = len(str(data.number))
            if not iter_length:
                continue
            lengths.add(iter_length)
    if not lengths:
        return None
    return max(lengths)


def set_column_autowidth(worksheet: Worksheet, column: int):
    """
    Set the width automatically on a column in the `Worksheet`.
    !!! Make sure you run this function AFTER having all cells filled in
    the worksheet!
    """
    maxwidth = get_column_width(worksheet=worksheet, column=column)
    if maxwidth is None:
        return
    worksheet.set_column(first_col=column, last_col=column, width=maxwidth)

dashjson, dashrequest = get_dash_data()

os.makedirs('out', exist_ok=True)
with Workbook('out/covid.xlsx') as workbook:
    datas = map(lambda x: x['data'], dashjson)
    sheets = map(lambda x: x["queryName"], dashrequest["requests"])
    shnames = []
    for shname, data in zip(sheets, datas):

        if shname in shnames:
            shname = shname + str(len(list(map(lambda n: shname in n, shnames))))
        shnames.append(shname)

        if not isinstance(data, list):
            data = [data]
        data = list(data)
        fields = list(data[0].keys())
        print(shname, fields)

        worksheet = workbook.add_worksheet(shname)
        worksheet.write_row(row=0, col=0, data=fields)
        for index, item in enumerate(data):
            row = map(lambda field_id: item.get(field_id, ''), fields)
            worksheet.write_row(row=index + 1, col=0, data=row)

        for ifield, _ in enumerate(fields):
            set_column_autowidth(worksheet, ifield)
