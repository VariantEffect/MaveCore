from unittest import TestCase
from mavecore.models.user import User
from mavecore.models.genome import Genome


class TestGenome(TestCase):
    def test_valid(self):
        genome = {
            "shortName": "name",
            "organismName": "organism",
            "genomeId": 0,
            "id": 0,
        }
        Genome.parse_obj(genome)

