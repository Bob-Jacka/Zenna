input_symbols: str = '>> '
"""
Input symbols in int or string user input
"""


def int_user_input(min_int_constraint: int = 0, max_int_constraint: int = 10):
    """
    Input function for integer type
    :param min_int_constraint: minimum value constraint
    :param max_int_constraint: maximum value constraint
    :return: checked int value
    """
    try:
        user_choice = int(input(input_symbols))
        if max_int_constraint >= user_choice >= min_int_constraint:
            return user_choice
        else:
            raise Exception(f'Min / Max constraint is not satisfied, user input {user_choice} is less than {min_int_constraint} or more than {max_int_constraint}')
    except Exception as e:
        print(f'Error in int user input - {e}')


def str_user_input(null_safe: bool = False):
    """
    Input function for strings
    :param null_safe: boolean flag if it need to check for null string
    :return: String object
    """
    try:
        user_choice = input(input_symbols)
        if null_safe:
            if user_choice != '' and user_choice is not None:
                return user_choice
            else:
                raise Exception('Null safe constraint is not satisfied')
        else:
            return user_choice
    except Exception as e:
        pass


def to_real_string(string: str):
    """
    In real world we encapsulate strings in double quotes
    :param string: string to encapsulate
    :return: Encapsulated string
    """
    return f'"{string}"'
