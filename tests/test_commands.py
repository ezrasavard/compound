from .context import compoundfin
from compoundfin import core

import datetime
import unittest


class CommandTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.parser = core.parser

    def test_help(self):
        command = '-h'
        with self.assertRaises(SystemExit) as e:
            self.parser.parse_args(command.split())
        self.assertEquals(e.exception.code, 0)


class TestQueryCommand(CommandTest):

    def test_basic_usage(self):
        command = 'query --start 2016-01-31 --end 2017-01-31'
        self.parser.parse_args(command.split())

    def test_default_end_date(self):
        command = 'query --start 2016-01-31'
        args = self.parser.parse_args(command.split())
        self.assertEquals(args.end_date.date(), datetime.date.today())

    def test_multiple_categories(self):
        command = 'query --start 2016-01-31 --categories Groceries Healthcare'
        args = self.parser.parse_args(command.split())
        self.assertTrue("Groceries" in args.categories)
        self.assertTrue("Healthcare" in args.categories)

    def test_rejects_unknown_category(self):
        command = 'query --start 2016-01-31 --categories MysteryCategory'
        with self.assertRaises(SystemExit) as e:
            self.parser.parse_args(command.split())
        self.assertEquals(e.exception.code, 2)


class TestFetchCommand(CommandTest):

    def test_basic_usage(self):
        """
        This test will fail if "fetch" is implemented and the test cases
        are not updated
        """
        command = 'fetch -h'
        with self.assertRaises(SystemExit) as e:
            self.parser.parse_args(command.split())
        self.assertEquals(e.exception.code, 2)
