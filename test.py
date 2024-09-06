import argparse
import unittest
import sys

# The following tests demonstrate three different ways to pass key-value arguments using argparse in Python.

# 1. Using the equal sign to assign a value to a key:
#    Example: --key=value
#    This method assigns the value directly to the key using an equal sign.

# 2. Using a space to separate the key and value:
#    Example: --key value
#    This method separates the key and value with a space.

# 3. Using a short option with a space to separate the key and value:
#    Example: -k value
#    This method uses a short option (single character) with a space to separate the key and value.


class TestArgparse(unittest.TestCase):
    def test_key_value_equal(self):
        test_args = ["test.py", "--key=value"]
        sys.argv = test_args
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--key", "-k", type=str, help="Example key-value argument"
        )
        args = parser.parse_args()
        self.assertEqual(args.key, "value")

    def test_key_value_space(self):
        test_args = ["test.py", "--key", "value"]
        sys.argv = test_args
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--key", "-k", type=str, help="Example key-value argument"
        )
        args = parser.parse_args()
        self.assertEqual(args.key, "value")

    def test_short_option(self):
        test_args = ["test.py", "-k", "value"]
        sys.argv = test_args
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--key", "-k", type=str, help="Example key-value argument"
        )
        args = parser.parse_args()
        self.assertEqual(args.key, "value")


if __name__ == "__main__":
    unittest.main()
