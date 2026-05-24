input_symbols: str = '>> '
"""
Input symbols in int or string user input
"""


def int_user_input(min_int_constraint: int = 0, max_int_constraint: int = 10):
    """
    Input function for integer type
    :param min_int_constraint: minimum value constraint to input
    :param max_int_constraint: maximum value constraint to input
    :return: checked int value
    """
    try:
        user_choice = int(input(input_symbols))
        if max_int_constraint >= user_choice >= min_int_constraint:
            return user_choice
        else:
            raise Exception(
                f'Min / Max constraint is not satisfied, user input {user_choice} is less than {min_int_constraint} or more than {max_int_constraint}')
    except Exception as e:
        print(f'Error in int user input - {e}')


def str_user_input(null_safe_check: bool = False):
    """
    Input function for strings
    :param null_safe_check: boolean flag if it need to check for null string
    :return: String object
    """
    try:
        user_choice = input(input_symbols)
        if null_safe_check:
            while True:
                if user_choice != '' and user_choice is not None:
                    return user_choice
                else:
                    print('Null safe constraint is not satisfied')
                    continue
        else:
            return user_choice
    except Exception as e:
        pass


def to_real_world_string(string: str):
    """
    In real world we encapsulate strings in double quotes
    :param string: string to encapsulate
    :return: Encapsulated string
    """
    return f'"{string}"'


def clear_str(to_clear: str) -> str:
    for cha in to_clear:
        if cha == '\'':
            to_clear.replace(cha, '')
        elif cha == '[' or cha == ']':
            to_clear.replace(cha, '')
    return to_clear  # return cleared string


def print_list_elems(list_to_print: list[str], is_print_console: bool, action=None):
    """
    Helper function for printing list elements in console or in file
    """
    str_to_return: str = ''
    for list_elem in list_to_print:
        if is_print_console:
            print(action(list_elem) if action is not None else list_elem)
            print(', ')
        else:
            str_to_return += action(list_elem) if action is not None else list_elem
            str_to_return += ', '
    str_to_return = str_to_return.removesuffix(', ')
    return str_to_return


def to_map(to_conver: list[str]) -> dict[str, str]:
    """
    Conversion into string dictionary
    """
    to_return: dict[str, str] = dict()
    for elem in to_conver:
        elem_name: str
        elem_ver: str
        split_elem_list = elem.split('\\')  # split by slash
        elem_name = clear_str(split_elem_list[0].strip())
        if len(split_elem_list) != 1:
            elem_ver = split_elem_list[1].strip()
        else:
            elem_ver = ''
        to_return[elem_name] = elem_ver
    return to_return


def to_list(to_conver: list[str]) -> list[str]:
    """
    Conversion into string list
    """
    to_return: list[str] = list()
    if len(to_conver) > 0:
        for elem in to_conver:
            if elem != '[]' and ('[' not in elem or '' not in elem):
                to_return.append(elem)
        return to_return
    else:
        return to_return
