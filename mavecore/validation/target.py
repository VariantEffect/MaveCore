from mavecore.validation.exceptions import ValidationError
from mavecore.validation.constants.target import valid_categories, valid_sequence_types


def validate_target_category(category):
    if category not in valid_categories:
        raise ValidationError("{}'s is not a valid target category. Valid categories are "
                              "Protein coding, Regulatory, and Other noncoding".format(category))


def validate_sequence_category(sequence_type):
    if sequence_type not in valid_sequence_types:
        raise ValidationError("{}'s is not a valid sequence type. Valid sequence types are "
                              "Infer, DNA, and Protein".format(sequence_type))
