from unittest import TestCase
from pydantic import ValidationError
from mavecore.models.user import User


class TestUser(TestCase):
    def test_valid_all_fields(self):
        user = {
          "orcid_id": "idididid",
          "firstName": "first",
          "lastName": "last",
          "email": "firstlast@email.edu",
        }
        User.parse_obj(user)

    def test_invalid_email(self):
        user = {
            "orcid_id": "idididid",
            "firstName": "first",
            "lastName": "last",
            "email": "firstlastemail.edu",
        }
        with self.assertRaises(ValueError):
            User.parse_obj(user)
