import json
import os
import tempfile
from io import BytesIO

from fastapi import FastAPI, Query, Body
from fastapi.responses import FileResponse, JSONResponse
from openpyxl import Workbook
from openpyxl.styles import numbers
from openpyxl.utils import get_column_letter
from openpyxl.utils.dataframe import dataframe_to_rows
from datetime import datetime

from starlette.background import BackgroundTask

from utils import *

app = FastAPI()


def resize_excel_cells(dataframe: DataFrame, worksheet):
    # Инициализация таблицы на оснвове порядового прохода по датафрейму
    for row in dataframe_to_rows(dataframe, index=False, header=True):
        worksheet.append(row)

    # Поиск значения в столбце с максимальной длиной, установка ширины колонки
    for column_cells in worksheet.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        # for cell in column_cells:
        #     if len(str(cell.value).split("-")) == 3:
        #         cell_name = f"{cell.column_letter}{cell.row}"
        #         worksheet[cell_name].value = datetime.strptime(cell.value, "%Y-%m-%d").date()
        column_letter = get_column_letter(column_cells[0].column)
        worksheet.column_dimensions[column_letter].width = length + 2

    return worksheet


def generate_file(data, custom_headers=[]):
    is_dict = isinstance(data, dict)
    prepared_data = [data] if is_dict else data

    # Коррекция датафрейма, установка кастомных заголовков
    df = pd.DataFrame(prepared_data)
    correct_df = correct_dataframe(set_new_keys_df(df, custom_headers))

    workbook = Workbook()
    workbook.active = resize_excel_cells(correct_df, workbook.active)

    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    return output.read()


@app.get("/")
async def get_temp_file(filename: str = Query(...),
                        keys: str = Query(...),
                        data: str = Query(...)) -> FileResponse or JSONResponse:
    # try:
    def cleanup():
        os.remove(temp_file.name)

    json_parsed = json.loads(data)
    keys_parsed = json.loads(keys)

    data_is_correct = isinstance(json_parsed, dict) or isinstance(json_parsed, list)

    if not data_is_correct:
        return JSONResponse({"err": "request is incorrect"})

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        # Запись результата во временный файл
        temp_file.write(generate_file(data=json_parsed, custom_headers=keys_parsed))
        temp_file.flush()

        return FileResponse(temp_file.name, background=BackgroundTask(cleanup),
                            media_type="application/octet-stream",
                            filename=f"{filename}.xlsx")
#
# except BaseException as e:
#     print(e)
#     return JSONResponse({"err": "request is incorrect"})
