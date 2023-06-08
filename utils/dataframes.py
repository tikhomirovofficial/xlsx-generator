import pandas as pd
from pandas import DataFrame

from utils.dictionaries import dict_flat, reformat_obj_dates_to_excel, get_new_keys

# Создание линейного датафрейма без вложенности, конвертация полей с датой в удобный формат
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


# Переименование колонок датафрейма
def set_new_keys_df(df: DataFrame, new_keys=[]) -> DataFrame:
    df_keys = df.columns.array
    new_df = df.rename(columns=get_new_keys(df_keys, new_keys))
    return new_df