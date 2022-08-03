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
    ValidationError if the title is not valid.
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
    ValidationError if the short description is too long or is not a string.
    """
    # check if short description is a string
    if type(shortDescription) != str: raise ValidationError("The short description must be a string.")

    # check if short description is too long
    count = len(shortDescription.split(" "))
    if count > 50: raise ValidationError("The short description must be less than or equal to 50 words.")

def validate_abstract(abstractText):
    """

    :param absract:
    :return:
    """
    return None

def validate_methods(methodText):

def validate_keywords(keywords):
"methodText": "string",
    "extraMetadata": {},
    "keywords": [
def validate_num_scoresets(numScoresets):
