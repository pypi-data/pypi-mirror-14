# coding: utf8


def left(a, _):
    return a


def right(_, b):
    return b


def empty(_):
    return None


def clear_empty_line(string):
    if string.startswith("\n"):
        return clear_empty_line(string[1:])
    if string.lstrip(" ").startswith("\n"):
        return clear_empty_line(string.lstrip(" ")[1:])
    return string


def multi(string, cut, skip_empty_line=True):
    result = list()
    while string:
        enum, string = cut(string)
        result.append(enum)
        string = clear_empty_line(string) if skip_empty_line else string
    return result


def till(string, cut, condition, skip_empty_line=True):
    result = list()
    while string and condition(string):
        enum, string = cut(string)
        result.append(enum)
        string = clear_empty_line(string) if skip_empty_line else string
    return result, string


def choice(condition, a, b):
    return a if condition else b


def choice_one(string, *args):
    def _get_result(stream):
        result = args[0](stream)
        return result if result is not None else choice_one(stream, *args[1:])
    return choice(args, _get_result, empty)(string)


def surround(string, start, end):
    return string[0] == start and string[-1] == end and string[1:-1]


def separate(string, symbol, reverse=False, padding=True):
    result = [enum for enum in choice(reverse, string.rsplit, string.split)(symbol, 1)]
    return fill(result) if padding else result


def fill(enums):
    return enums[0], enums[1] if len(enums) > 1 else ""
