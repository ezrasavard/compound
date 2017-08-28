from .context import compoundfin
from . import util
from compoundfin import config
from compoundfin import core
from compoundfin import mapper

import tempfile


class TestOutput(util.DBTest):
    """
    Tests in this class cover both unittesting some output methods
    and functional testing of the entire query-to-output sequence
    """

    TMP_DIR = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.TMP_DIR = tempfile.TemporaryDirectory(dir='.')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.TMP_DIR.cleanup()

    def test_transaction_csv(self):
        tmp = tempfile.NamedTemporaryFile(suffix='.csv',
                dir=self.TMP_DIR.name, delete=False)
        # query to get transactions 1 through 3
        command = 'query --start {} --end {} --raw-csv {}'.format(
                self.DATE1.strftime(config.time_format),
                self.DATE4.strftime(config.time_format), tmp.name)
        args = core.parser.parse_args(command.split())
        args.func(args)
        csv_written = tmp.readlines()
        print('csv content: {}'.format(csv_written))
        # header row and three data rows
        self.assertEquals(len(csv_written), 4)

    def test_transaction_by_category_csv(self):
        tmp = tempfile.NamedTemporaryFile(suffix='.csv',
                dir=self.TMP_DIR.name, delete=False)
        # query to get transactions 1 and 2
        command = 'query --start {} --end {} --csv {}'.format(
                self.DATE1.strftime(config.time_format),
                self.DATE3.strftime(config.time_format), tmp.name)
        args = core.parser.parse_args(command.split())
        args.func(args)
        csv_written = tmp.readlines()
        print('csv content: {}'.format(csv_written))
        # header row and two category rows
        self.assertEquals(len(csv_written),
                len(mapper.Category.CATEGORIES) + 1)

    def test_transaction_by_category_pie_chart(self):
        pass

    def test_image_formats(self):
        pass

    def test_validate_single_currency(self):
        pass

    def test_currency_conversion(self):
        pass

    def test_aggregate_transactions_by_category(self):
        pass
