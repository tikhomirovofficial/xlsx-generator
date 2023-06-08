from openpyxl.utils import get_column_letter
from openpyxl.utils.dataframe import dataframe_to_rows
from pandas import DataFrame

from utils.common import get_excel_date


# Изменение размеров столбцов на основе значения с максимальной длиной
def resize_excel_columns(dataframe: DataFrame, worksheet):
    # Инициализация таблицы на основе порядового прохода по датафрейму
    for row in dataframe_to_rows(dataframe, index=False, header=True):
        worksheet.append(row)

    # Поиск значения в столбце с максимальной длиной, установка ширины колонки
    for column_cells in worksheet.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        column_letter = get_column_letter(column_cells[0].column)
        worksheet.column_dimensions[column_letter].width = length + 2

    return worksheet


# Создание линейного словаря, избавление от вложенности
def dict_flat(data, parent_key='', sep='.'):
    result = {}

    for key, val in data.items():
        new_key = str(parent_key) + str(sep) + str(key) if parent_key else key

        if isinstance(val, dict):
            result.update(dict_flat(val, new_key))

        elif isinstance(val, list) and all(isinstance(item, dict) for item in val):
            result.update(dict_flat(transform_list_of_dicts(val), new_key))

        else:
            result[new_key] = val

    return result


# Изменение ключей словаря
def get_new_keys(prev_keys, new_keys):
    new_keys_dict = {}

    for i in range(len(prev_keys)):
        if i < len(prev_keys) and i < len(new_keys):
            new_keys_dict[prev_keys[i]] = new_keys[i]

    return new_keys_dict


# Поиск полей с датой, конвертация в удобный формат
def reformat_obj_dates_to_excel(data):
    for key, val in data.items():
        data[key] = get_excel_date(val) or data[key]
    return data


# Трансформация словаря
def transform_list_of_dicts(data):
    result = {}

    for item in data:
        for key, value in item.items():
            if key not in result:
                result[key] = []
            result[key].append(get_excel_date(value) or value)

    return result
