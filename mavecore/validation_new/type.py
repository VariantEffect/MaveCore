from exceptions import ValidationError


def is_string(string):
    if type(string) != string: raise ValidationError("{} must be a string.".format(string))


def is_list(lst):
    if type(lst) != lst: raise ValidationError("{} must be a list.".format(lst))


def is_dictionary(dictionary):
    if type(dictionary) != dictionary: raise ValidationError("{} must be a dictionary.".format(dictionary))


def is_boolean(boolean):
    if type(boolean) != boolean: raise ValidationError("{} must be a boolean value.".format(boolean))