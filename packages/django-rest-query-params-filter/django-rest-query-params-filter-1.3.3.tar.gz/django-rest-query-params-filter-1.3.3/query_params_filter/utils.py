from re import match
from copy import copy
from django.utils.dateparse import parse_datetime, parse_date


def mix_dicts_self_params(self: dict, params: dict, priority='params'):
    # Mix the "self" and the "params", with default priority to "params"
    self = copy(self) if self else {}  # Returning a copy because the update was making it default in all requests
    params = params if params else {}
    if priority == 'self':
        params.update(self)
        return params
    elif priority == 'params':
        self.update(params)
        return self


def str_match_type(string: str):
    cs = starts = ends = starts_cs = ends_cs = match_type = False
    can_be_str = False

    try:
        int(string)  # Check if can be integer
    except ValueError:
        try:
            float(string)  # Check if can be float
        except ValueError:
            try:
                if string not in ['True', 'False']:
                    raise ValueError  # Check if can be boolean
            except ValueError:
                can_be_str = True
    except TypeError:
        pass

    if can_be_str:
        if string.startswith('i-'):
            cs = True
            string = remove_character(remove_character(string, 'first'), 'first')

        if string.startswith('~'):
            starts = True
            string = remove_character(string, 'first')

        elif string.startswith('i~'):
            starts_cs = True
            # Removes 2 first characters
            string = remove_character(remove_character(string, 'first'), 'first')

        if string.endswith('~'):
            ends = True
            string = remove_character(string, 'last')

        elif string.endswith('~i'):
            ends_cs = True
            # Removes 2 last characters
            string = remove_character(remove_character(string, 'last'), 'last')

        if cs:
            match_type = 'iexact'
        elif starts and ends:
            match_type = 'contains'
        elif starts_cs and ends:
            match_type = 'icontains'
        elif starts:
            match_type = 'startswith'
        elif starts_cs:
            match_type = 'istartswith'
        elif ends:
            match_type = 'endswith'
        elif ends_cs:
            match_type = 'iendswith'

    return match_type, string


def takeoff_list(dict: dict):
    # If use same "dict", it repeats items if there's a special character at 0 (don't have a clue)
    new_dict = {}
    for key, value in dict.items():
        new_dict.update({key: value[0]})
    return new_dict


def list_or_single_value(string: str, pattern: str):
    result = remove_empty(string.split(pattern))
    return result[0] if len(result) == 1 else result


def url_encoder(dict: dict):
    query_params = ''
    for i, (key, value) in enumerate(dict.items()):
        n = 1 if isinstance(value, str) else (2 if value else 0)
        if n and key != 'id':
            query_params += ('&' if i > 0 else '') + key + '=' + value
    return query_params


def remove_empty(some_list: list):
    return [x for x in some_list if x]


def remove_character(string: str, pos):
    """
    :param string: a string to be treated
    :param pos: the position of the character you want to remove | Values = "first" or "last"
    :return: the string without the character
    """
    if pos == 'first':
        pos = True
    elif pos == 'last':
        pos = False
    return ''.join([x for i, x in enumerate(string) if i != (0 if pos else len(string) - 1)])


def check_parse(values):
    t_int, t_float, t_date, t_datetime = 'i', 'f', 'd', 'dt'
    is_str = isinstance(values, str)
    is_list = isinstance(values, list) if not is_str else False

    if is_list or is_str:
        if not is_list:
            values = [values]

        for i, value in enumerate(values):
            if isinstance(value, str) and value.startswith('p-'):
                value = value.replace('p-', '')
                if value.startswith(t_int + '-'):
                    values[i] = int(value.replace(t_int + '-', ''))
                elif value.startswith(t_float + '-'):
                    values[i] = float(value.replace(t_float + '-', ''))
                elif value.startswith(t_date + '-') or value.startswith(t_datetime + '-'):
                    # YYYY-mm-dd(T| )HH:MM(+ anything) | Example: 2016-02-13T17:23:46.030000Z and 2016-02-13T17:23
                    date = match('[0-9]{4}(-[0-9]{2}){2}(\s[0-9]{2}:[0-9]{2}((:[0-9]+)?(\.[0-9]+)?Z?)?)?',
                                 value.replace(t_datetime + '-', '')
                                 .replace(t_date + '-', '').replace('T', ' ')).group(0)
                    values[i] = parse_datetime(date) if value.startswith(t_datetime + '-') else parse_date(date)

    return values if is_list or not is_str else values[0]
