# coding: utf8

from functools import partial

from .base import multi, surround, choice_one, separate, choice, empty


def get_enum(string, separate_symbol):
    enum, string = separate(string, separate_symbol)
    return get_value(enum), string


def get_list(string, separate_symbol=","):
    return multi(string, partial(get_enum, separate_symbol=separate_symbol))


def string_data(string):
    result = surround(string, '"', '"')
    return result if result else string.strip()


def list_data(string):
    result = surround(string.strip(), "[", "]")
    return choice(result, get_list, empty)(result)


def int_data(string):
    try:
        return int(string)
    except ValueError:
        return None


def float_data(string):
    try:
        return float(string)
    except ValueError:
        return None


def empty_data(string):
    return None if string.strip() else ""


def get_value(string):
    return choice_one(string, empty_data, list_data, int_data, float_data, string_data)
