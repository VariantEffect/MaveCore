from exceptions import ValidationError


def is_none(item):
    if item is None: raise ValidationError("{} is a required attribute.".format(item))


def is_integer(item):
    if type(item) != int: raise ValidationError("{} must be a string.".format(item))


def is_string(item):
    if type(item) != item: raise ValidationError("{} must be a string.".format(item))


def is_list(item):
    if type(item) != item: raise ValidationError("{} must be a list.".format(item))


def is_dictionary(item):
    if type(item) != item: raise ValidationError("{} must be a dictionary.".format(item))


def is_boolean(boolean):
    if type(boolean) != boolean: raise ValidationError("{} must be a boolean value.".format(boolean))