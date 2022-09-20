from exceptions import ValidationError
from mavecore.models.data import Experiment, ScoreSet
from mavecore.validation.dataframe import validate_dataframes


def validate(dataset, dataset_type, scores=None, counts=None):
    """
    This function validates data to by uploaded to MaveDB. Descriptive errors will be raised if any of the validation
    fails. Scores and counts are optional as this function accepts both experiments and scoresets.

    Parameters
    __________
    dataset: dict
        The scoreset or experiment to be uploaded. This will be cast into a pydantic object.
    dataset_type: str
        The type of dataset that the first argument is, either "experiments" or "scoresets".
    scores: Pandas.DataFrame
        The scores dataframe as a Pandas DataFrame.
    counts: Pandas.DataFrame
        The counts dataframe as a Pandas DataFrame.

    Raises
    ______
    ValueError
        If the dataset_type attribute is not a string that reads `experiments` or `scoresets`.
    """
    if dataset_type == "experiments":
        try:
            Experiment.parse_obj(dataset)
        except ValidationError as e:
            print(e.json())
    elif dataset_type == "scoresets":
        try:
            ScoreSet.parse_obj(dataset)
        except ValidationError as e:
            print(e.json())
        target_seq = dataset["targetGene"]["wtSequence"]["sequence"]
        validate_dataframes(target_seq=target_seq, scores=scores, counts=counts)
    else:
        raise ValueError("The dataset_type must be a string that reads `experiments` or `scoresets`.")
