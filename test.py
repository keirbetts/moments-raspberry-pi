import unittest
from connection import dbConnection


class TestGetUrls (unittest.TestCase):
    def test_getUrls(self):
        self.table = dbConnection()
        self.response = table.get_item(
            Key={"usr": "crookydan"}
        )
        self.pictureUrls = response["Item"]["picURL"]

        self.assertIsInstance(self.pictureUls, list)


if __name__ == "__main__":
    unittest.main()
