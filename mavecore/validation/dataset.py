import json

from mavecore.models.data import Experiment, ScoreSet


def validate_experiment(experiment: dict):
    """
    Validates an experiment represented as a dictionary. Validation is handled via pydantic. A valid dictionary is
    returned upon validation. If extra or duplicate keys are included, those fields are excluded from the returned
    dictionary. If required keys are missing or any keys contain incorrect values, an error is raised.

    Parameters
    __________
    experiment : dict
        The experiment dictionary that will be validated.

    Raises
    ______
    ValueError
        If required keys are missing or any keys contain incorrect values.
    """
    try:
        return json.loads(Experiment.parse_obj(experiment).json())
    except ValueError as e:
        print(e)


def validate_scoreset(scoreset: dict):
    """
    Validates a scoreset represented as a dictionary (Note: this does not validate dataframes, look to dataframe.py
    for that validation code). Validation is handled via pydantic. A valid dictionary is returned upon validation.
    If extra or duplicate keys are included, those fields are excluded from the returned dictionary. If required keys
    are missing or any keys contain incorrect values, an error is raised.

    Parameters
    __________
    experiment : dict
        The scoreset dictionary that will be validated.

    Raises
    ______
    ValueError
        If required keys are missing or any keys contain incorrect values.
    """
    try:
        return json.loads(ScoreSet.parse_obj(scoreset).json())
    except ValueError as e:
        print(e)
