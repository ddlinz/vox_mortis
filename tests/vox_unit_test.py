import unittest


class TestVoxUnitTests(unittest.TestCase):
    def test_access_basic(self):
        self.assertEqual(0 + 1, 1)

    def test_access_basic_alt(self):
        self.assertEqual(0 + 1, 1)


if __name__ == "__main__":
    unittest.main()
