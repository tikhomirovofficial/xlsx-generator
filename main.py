import os
import tempfile
from io import BytesIO

import pandas
from fastapi import FastAPI
from fastapi.responses import FileResponse
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.utils.dataframe import dataframe_to_rows

import pandas as pd
from pandas import DataFrame
from starlette.background import BackgroundTask

from utils import *

app = FastAPI()


def correct_dataframe(df: DataFrame) -> DataFrame:
    list_from_df = []

    for _, row in df.iterrows():
        flatted_row_dict = dict_flat(dict(row))
        for key, val in flatted_row_dict.items():
            if isinstance(val, list):
                sep = ", "

                flatted_row_dict[key] = sep.join([str(item) for item in val])

        list_from_df.append(reformat_obj_dates_to_excel(flatted_row_dict))

    return pd.DataFrame(list_from_df)


def set_new_keys_df(df: DataFrame, new_keys=[]) -> DataFrame:
    df_keys = df.columns.array
    new_df = df.rename(columns=get_new_keys(df_keys, new_keys))
    return new_df


def generate_file(params, custom_headers=["Имя"], filename="result"):
    is_dict = isinstance(params, dict)
    prepared_data = [params] if is_dict else params

    df = pd.DataFrame(prepared_data)
    correct_df = correct_dataframe(set_new_keys_df(df, custom_headers))
    workbook = Workbook()

    worksheet = workbook.active

    for row in dataframe_to_rows(correct_df, index=False, header=True):
        worksheet.append(row)

    for column_cells in worksheet.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        column_letter = get_column_letter(column_cells[0].column)
        worksheet.column_dimensions[column_letter].width = length + 2

    output = BytesIO();
    workbook.save(output)
    output.seek(0)
    return output.read()

    # file_res = FileResponse()
    # return file_res


generate_file([
    {
        "name": "Artemfdsfdsfsdfsdfsfdfsdfsdfsdfs",
        "age": 19
    },
    {
        "name": "Artem",
        "age": 191
    }
])


@app.get("/")
async def get_temp_file() -> FileResponse:
    filename = "sas"

    def cleanup():
        os.remove(temp_file.name)

    # Создаем временный файл с помощью tempfile.NamedTemporaryFile
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        # Записываем данные во временный файл
        # Все параметры, что потребуются для генерации файла передаем в функцию generate_file()
        temp_file.write(generate_file([
            {
                "name": "Artem",
                "age": 18,
                "birthday": "1623500000"
            },
            {
                "name": "Artemdsfdsfdfsfdfsfsdffsfd",
                "age": 18,
                "birthday": "22-03-04"
            }
        ]))
        temp_file.flush()

        return FileResponse(temp_file.name, background=BackgroundTask(cleanup), media_type="application/octet-stream",
                            filename=f"{filename}.xlsx")
