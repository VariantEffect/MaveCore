from mavecore.models.data import Experiment, ScoreSet


def validate_experiment(experiment: dict):
    try:
        Experiment.parse_obj(experiment)
    except ValueError as e:
        print(e)


def validate_scoreset(scoreset: dict):
    try:
        ScoreSet.parse_obj(scoreset)
    except ValueError as e:
        print(e)
