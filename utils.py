from dateutil import parser
import datetime as dt


def try_parse_int(param_str) -> bool or int:
    try:
        return int(param_str)
    except BaseException:
        return False



def get_excel_date(date_str):
    try:
        excel_format = "%d.%m.%Y"

        if not try_parse_int(date_str):
            return parser.parse(date_str).strftime(excel_format)

        if len(date_str) == 10:
            dt_timestamp = dt.datetime.fromtimestamp(int(date_str))
            return dt_timestamp.strftime(excel_format)

    except BaseException as e:
        return False


def transform_list_of_dicts(data):
    result = {}
    for item in data:
        for key, value in item.items():
            if key not in result:
                result[key] = []
            result[key].append(get_excel_date(value) or value)
    return result


def reformat_obj_dates_to_excel(data):
    for key, val in data.items():
        data[key] = get_excel_date(val) or data[key]
    return data


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


def get_new_keys(prev_keys, new_keys):
    new_keys_dict = {}

    for i in range(len(prev_keys)):
        if i < len(prev_keys) and i < len(new_keys):
            new_keys_dict[prev_keys[i]] = new_keys[i]

    return new_keys_dict
