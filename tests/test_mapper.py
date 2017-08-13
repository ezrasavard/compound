from .context import compoundfin
from compoundfin import core
from compoundfin import mapper

import datetime
import mongoengine as mdb
import unittest
import uuid


class TestMapper(unittest.TestCase):

    ACCOUNT1 = mapper.Account(bank="CapitalOne",
            card_type="MASTERCARD",
            last_four="1234",
            description="foobarz card",
            native_currency="CAD")
    ACCOUNT2 = mapper.Account(bank="Tangerine",
            card_type="DEBIT",
            last_four="9999",
            description="my debit card",
            native_currency="CAD")
    ACCOUNT3 = mapper.Account(bank="RBC",
            card_type="DEBIT",
            last_four="1111",
            description="rbc debit card",
            native_currency="CAD")

    CATEGORY_GROCERIES = mapper.CategoryMap(description="Groceries",
            code=1)

    CATEGORY_HEALTHCARE = mapper.CategoryMap(description="Healthcare",
            code=2)

    CATEGORY_DINING = mapper.CategoryMap(description="Dining",
            code=3)

    DATE1 = core.timestamp("1970-01-01")
    DATE2 = core.timestamp("1970-01-02")
    DATE3 = core.timestamp("1970-01-03")
    DATE4 = core.timestamp("1970-01-04")

    TRANSACTION1 = mapper.Transaction(amount=-10,
            currency="CAD",
            account=ACCOUNT1,
            date=DATE1,
            category=CATEGORY_GROCERIES,
            description="transaction 1")

    TRANSACTION2 = mapper.Transaction(amount=-20,
            currency="CAD",
            account=ACCOUNT2,
            date=DATE2,
            category=CATEGORY_HEALTHCARE,
            description="transaction 2")

    TRANSACTION3 = mapper.Transaction(amount=-30,
            currency="USD",
            account=ACCOUNT3,
            date=DATE3,
            category=CATEGORY_DINING,
            description="transaction 3")

    @classmethod
    def setUpClass(cls):
        """Create a temporary database"""
        cls.db_name = str(uuid.uuid4())
        print("Creating temporary DB: {}".format(cls.db_name))
        cls.client = mdb.connect(cls.db_name)

        cls.ACCOUNT1.save()
        cls.ACCOUNT2.save()
        cls.ACCOUNT3.save()
        cls.CATEGORY_GROCERIES.save()
        cls.CATEGORY_HEALTHCARE.save()
        cls.CATEGORY_DINING.save()
        cls.TRANSACTION1.save()
        cls.TRANSACTION2.save()
        cls.TRANSACTION3.save()

    @classmethod
    def tearDownClass(cls):
        """Destroy the temporary database"""
        print("Removing temporary DB: {}".format(cls.db_name))
        cls.client.fsync()
        cls.client.drop_database(cls.db_name)

    def test_category_insertion_and_retrieval(self):
        row = mapper.CategoryMap()
        row.description = "Groceries"
        row.code = 9999
        row.no_cache = True
        row.save()

        # test persistence
        self.client.close()
        self.client = mdb.connect(self.db_name)
        self.assertTrue(row in mapper.CategoryMap.objects())

    def test_category_invalid(self):
        row = mapper.CategoryMap()
        row.description = "foobar"
        self.assertRaises(mdb.ValidationError, row.save)

    def test_transaction_insertion_and_retrieval(self):
        row = mapper.CategoryMap()
        row.description = "Costco"
        row.code = 1234
        row.save()
        row.no_cache = True
        self.assertTrue(row in mapper.CategoryMap.objects())

        account = mapper.Account()
        account.bank = "CapitalOne"
        account.card_type = "MASTERCARD"
        account.last_four = "1234"
        account.description = "foobarz card"
        account.native_currency = "CAD"
        account.no_cache = True
        account.save()
        self.assertTrue(account in mapper.Account.objects())

        trans = mapper.Transaction()
        trans.amount = -13.37
        trans.currency = "CAD"
        trans.account = account
        trans.date = datetime.datetime.now
        trans.description = "stuff"
        trans.category = row
        trans.no_cache = True
        trans.save()

        # test persistence
        self.client.close()
        self.client = mdb.connect(self.db_name)
        self.assertTrue(trans in mapper.Transaction.objects())

    def test_transaction_query_date_boundaries(self):
        """Queries have inclusive start dates and exclusive end dates"""
        results = mapper.Transaction.query(start_date=self.DATE1,
                end_date=self.DATE2)
        self.assertEquals(len(results), 1)
        self.assertEquals(results[0].description,
                self.TRANSACTION1.description)

        results = mapper.Transaction.query(start_date=self.DATE2,
                end_date=self.DATE3)
        self.assertEquals(len(results), 1)
        self.assertEquals(results[0].description,
                self.TRANSACTION2.description)

    def test_transaction_query_category_filtering(self):
        results = mapper.Transaction.query(start_date=self.DATE1,
                end_date=self.DATE4,
                category_filters=[self.CATEGORY_GROCERIES.description])
        self.assertEquals(len(results), 1)

    def test_transaction_query_multi_category_filtering(self):
        results = mapper.Transaction.query(start_date=self.DATE1,
                end_date=self.DATE4,
                category_filters=[self.CATEGORY_GROCERIES.description,
                    self.CATEGORY_HEALTHCARE.description])
        self.assertEquals(len(results), 2)
