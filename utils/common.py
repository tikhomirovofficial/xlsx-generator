import datetime as dt

import dateutil.parser


def try_parse_int(param_str) -> bool or int:
    try:
        return int(param_str)

    except BaseException:
        return False


# Конвертация даты в удобный формат для excel
def get_excel_date(date_str):
    try:
        if not try_parse_int(date_str):
            res = dateutil.parser.parse(date_str).date()
            return res

        len_timestamp = 10
        str_is_equal_max_len = len(date_str) == len_timestamp

        if str_is_equal_max_len:
            dt_timestamp = dt.datetime.fromtimestamp(int(date_str))

            return dt_timestamp.date()

    except BaseException as e:
        return False
