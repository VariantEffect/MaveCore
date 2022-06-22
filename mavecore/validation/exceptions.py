# note: ValidationError2 code in this file is from Django
import operator

NON_FIELD_ERRORS = "__all__"

class ValidationError(ValueError):
    None