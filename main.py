import os
import tempfile

from dateutil import parser
from fastapi import FastAPI
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
import pandas as pd
from utils import *

app = FastAPI()


# **kwargs заменить на получаемые параметры
def generate_file(params, custom_headers=[]):
    is_dict = isinstance(params, dict)
    prepared_data = [params] if is_dict else params
    # flatted_data = [dict_flat(item if isinstance(item, dict) else dict(item)) for item in prepared_data ]

    # print(flatted_data)
    # reformatted_dates = reformat_obj_dates_to_excel(flatted_data)

    df = pd.DataFrame(prepared_data)
    list_from_df = []
    for index, val in df.iterrows():
        list_from_df.append(reformat_obj_dates_to_excel(dict_flat(dict(val))))

    new_df = pd.DataFrame(list_from_df)
    df_keys = new_df.columns.array
    new_df = new_df.rename(columns=get_new_keys(df_keys, custom_headers))

    for index, val in new_df.iterrows():
        for key, item in val.items():
            print(key, item)

    # print(get_excel_date("20/02/2004"))

    # result = "output.xlsx"
    # df.to_excel(result, index=False)
    # return b'123'


generate_file([
    {
        "name": "John Doe",
        "age": 30,
        "email": "johndoe@example.com",
        "address": {
            "street": "123 Main St",
            "city": "New York",
            "state": "NY",
            "country": "USA"
        },
        "phoneNumbers": [
            {
                "type": "home",
                "number": "555-1234"
            },
            {
                "type": "work",
                "number": "555-5678"
            }
        ],
        "friends": [
            {
                "name": "Jane Smith",
                "age": 28,
                "birthday": "1659800000"
            },
            {
                "name": "Mike Johnson",
                "age": 32,
                "birthday": "18/02/2002"
            }
        ]
    }

])
# в get_temp_file(сюда) можно передавать аргументы с их типами, что потребуется, то и передаем
# @app.get("/")
# async def get_temp_file() -> FileResponse:
#     def cleanup():
#         os.remove(temp_file.name)
#
#     # Создаем временный файл с помощью tempfile.NamedTemporaryFile
#     with tempfile.NamedTemporaryFile(delete=False) as temp_file:
#         # Записываем данные во временный файл
#         # Все параметры, что потребуются для генерации файла передаем в функцию generate_file()
#         temp_file.write(generate_file())
#         temp_file.flush()
#
#         # Возвращаем временный файл в ответе
#         return FileResponse(temp_file.name, background=BackgroundTask(cleanup), media_type="application/octet-stream",
#                             filename="temp_file.txt")
