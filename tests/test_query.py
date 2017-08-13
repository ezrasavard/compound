from .context import compoundfin
from compoundfin import core
from compoundfin import mapper
from compoundfin import query

import datetime
import mongoengine as mdb
import unittest
import uuid


class TestQuery(unittest.TestCase):

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
        """Create a temporary database and populate it"""
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

    def test_query_date_boundaries(self):
        """Queries have inclusive start dates and exclusive end dates"""
        transaction_query = query.Transactions()
        transaction_query.start_date = self.DATE1
        transaction_query.end_date = self.DATE2
        results = transaction_query.execute()
        self.assertEquals(len(results), 1)
        self.assertEquals(results[0].description,
                self.TRANSACTION1.description)

        transaction_query = query.Transactions()
        transaction_query.start_date = self.DATE2
        transaction_query.end_date = self.DATE3
        results = transaction_query.execute()
        self.assertEquals(len(results), 1)
        self.assertEquals(results[0].description,
                self.TRANSACTION2.description)

    def test_category_filtering(self):
        transaction_query = query.Transactions()
        transaction_query.start_date = self.DATE1
        transaction_query.end_date = self.DATE4
        transaction_query.category_filters = [
                self.CATEGORY_GROCERIES.description,
                ]
        results = transaction_query.execute()
        self.assertEquals(len(results), 1)

    def test_multi_category_filtering(self):
        transaction_query = query.Transactions()
        transaction_query.start_date = self.DATE1
        transaction_query.end_date = self.DATE4
        transaction_query.category_filters = [
                self.CATEGORY_GROCERIES.description,
                self.CATEGORY_HEALTHCARE.description,
                ]
        results = transaction_query.execute()
        self.assertEquals(len(results), 2)
