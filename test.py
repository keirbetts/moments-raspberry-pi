import unittest
from utils import getUsrPhotoUrls


class TestGetUrls (unittest.TestCase):
    def test_getUrls(self):
        result = getUsrPhotoUrls()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertIsInstance(result[1], str)


if __name__ == "__main__":
    unittest.main()
