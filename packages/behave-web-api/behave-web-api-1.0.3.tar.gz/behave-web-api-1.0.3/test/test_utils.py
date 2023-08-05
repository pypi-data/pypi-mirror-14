import unittest
from behave_web_api import utils


class UtilsTest(unittest.TestCase):
    def test_is_comparing_values_with_matched_regex(self):
        error = None

        try:
            utils.compare_values(
                {
                    'hi': '%.+%'
                },
                {
                    'hi': 'Hello'
                }
            )
        except AssertionError, e:
            error = e

        self.assertIsNone(error)

    def test_is_comparing_values_with_non_matched_regex(self):
        error = None

        try:
            utils.compare_values(
                {
                    'hi': 'dsa'
                },
                {
                    'hi': 'Hello'
                }
            )
        except AssertionError, e:
            error = e

        self.assertEqual(
            'Expected \'Hello\' to equal \'dsa\' at path hi',
            error.message
        )

    def test_is_comparing_dicts(self):
        error = None

        try:
            utils.compare_values(
                {
                    'a': {
                        'b': {
                            'c': [3]
                        }
                    }
                },
                {
                    'a': {
                        'b': {
                            'c': [4]
                        }
                    }
                }
            )
        except AssertionError, e:
            error = e

        self.assertEqual(
            'Expected 4 to equal 3 at path a.b.c.0',
            error.message
        )
