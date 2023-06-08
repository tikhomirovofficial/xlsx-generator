import json
import os
import tempfile
from io import BytesIO

import pandas as pd
from fastapi import FastAPI, Query, Body
from fastapi.responses import FileResponse, JSONResponse
from openpyxl import Workbook

from starlette.background import BackgroundTask

from utils.dataframes import set_new_keys_df, correct_dataframe
from utils.dictionaries import resize_excel_columns

app = FastAPI()


# Основная функция генерации файла.
# Принимает данные и кастомные заголовки, возвращает набор байтов для записи в excel файл.
def generate_file(data, custom_headers=[]):
    is_dict = isinstance(data, dict)
    prepared_data = [data] if is_dict else data

    # Коррекция датафрейма, установка кастомных заголовков
    df = pd.DataFrame(prepared_data)
    correct_df = set_new_keys_df(correct_dataframe(df), custom_headers)

    workbook = Workbook()
    workbook.active = resize_excel_columns(correct_df, workbook.active)

    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    return output.read()


# Маршрут, принимает в качестве тела поля: имя файла, новые заголовки, данные (подразумевается JSON строка)
@app.get("/")
async def get_temp_file(filename: str = Query(...),
                        keys: str = Query(...),
                        data: str = Query(...)) -> FileResponse or JSONResponse:
    try:
        def cleanup():
            os.remove(temp_file.name)
        json_parsed = json.loads(data)
        keys_parsed = json.loads(keys)

        data_is_correct = isinstance(json_parsed, dict) or isinstance(json_parsed, list)

        if not data_is_correct:
            print(data_is_correct)
            return JSONResponse({"err": "data is incorrect"})

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            # Запись результата во временный файл
            temp_file.write(generate_file(data=json_parsed, custom_headers=keys_parsed))
            temp_file.flush()

            return FileResponse(temp_file.name, background=BackgroundTask(cleanup),
                                media_type="application/octet-stream",
                                filename=f"{filename}.xlsx")

    except BaseException as e:
        print(e)
        return JSONResponse({"err": "request is incorrect"})
