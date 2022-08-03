from exceptions import ValidationError


def validate_title(title):
    """
    Validates a title of an experiment set, an experiment, or a scoreset.

    Parameters:
    __________
    title: str
        The title to be validated.

    Raises:
    ______
    ValidationError
        If the title is not valid.
    """
    # check if title is a string
    if type(title) != str: raise ValidationError("The title must be a string.")

    # check that title is not too long


def validate_short_description(shortDescription):
    """
    Validates the short description of an experiment set, an experiment, or a scoreset.

    Parameters:
    __________
    shortDescription: str
        The short description to be validated.

    Raises:
    ______
    ValidationError
        If the short description is too long or is not a string.
    """
    # check if short description is a string
    if type(shortDescription) != str: raise ValidationError("The short description must be a string.")

    # check if short description is too long
    count = len(shortDescription.split(" "))
    if count > 50: raise ValidationError("The short description must be less than or equal to 50 words.")


def validate_abstract(abstractText):
    """
    Validates the abstract of an experiment set, an experiment, or a scoreset.

    Parameters:
    __________
    abstractText: str
        The abstract to be validated.

    Raises:
    ______
    ValidationError
        If the abstract is too long or is not a string.
    """
    # check if short description is a string
    if type(abstractText) != str: raise ValidationError("The abstract must be a string.")

    # check if short description is too long
    count = len(abstractText.split(" "))
    if count > 200: raise ValidationError("The abstract must be less than or equal to 200 words.")


def validate_methods(methodText):
    """
    Validates the methods of an experiment set, an experiment, or a scoreset.

    Parameters:
    __________
    methodText: str
        The methods to be validated.

    Raises:
    ______
    ValidationError
        If the methods are too long or is not a string.
    """
    # check if short description is a string
    if type(methodText) != str: raise ValidationError("The methods must be a string.")

    # check if short description is too long
    count = len(methodText.split(" "))
    if count > 200: raise ValidationError("The methods must be less than or equal to 200 words.")


def validate_keywords(keywords):
    """
    Validates the methods of an experiment set, an experiment, or a scoreset.

    Parameters:
    __________
    methodText: str
        The methods to be validated.

    Raises:
    ______
    ValidationError
        If the keywords object is not a list of strings.
    """
    # check keywords type
    if type(keywords) != list[str]: raise ValidationError("The keywords must be a list of strings.")


def validate_num_scoresets(numScoresets):
    return


def validate_num_variants(numVariants):
    return


def validate_dataset_columns(datasetColumns):
    return
