from .context import compoundfin
from compoundfin import core
from compoundfin import mapper

import datetime
import mongoengine as mdb
import unittest


class DBTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_name = 'compound-unittest'
        app = core.Application(cls.db_name)
        cls.client = app.client
        print("Creating temporary DB: {}".format(cls.db_name))

        cls.ACCOUNT1 = mapper.Account(bank="CapitalOne",
                card_type="MASTERCARD",
                last_four="1234",
                description="foobarz card",
                native_currency="CAD")
        cls.ACCOUNT2 = mapper.Account(bank="Tangerine",
                card_type="DEBIT",
                last_four="9999",
                description="my debit card",
                native_currency="CAD")
        cls.ACCOUNT3 = mapper.Account(bank="RBC",
                card_type="DEBIT",
                last_four="1111",
                description="rbc debit card",
                native_currency="CAD")

        cls.CATEGORY_GROCERIES = mapper.CategoryMap(category="Groceries",
                merchant="Spam and More Spam")

        cls.CATEGORY_HEALTHCARE = mapper.CategoryMap(category="Healthcare",
                merchant="Foo's Medical Services")

        cls.CATEGORY_DINING = mapper.CategoryMap(category="Dining",
                merchant="Spam and Eggs Only Diner")

        cls.DATE1 = core.timestamp("1970-01-01")
        cls.DATE2 = core.timestamp("1970-01-02")
        cls.DATE3 = core.timestamp("1970-01-03")
        cls.DATE4 = core.timestamp("1970-01-04")

        cls.TRANSACTION1 = mapper.Transaction(amount=-10,
                currency="CAD",
                account=cls.ACCOUNT1,
                date=cls.DATE1,
                category=cls.CATEGORY_GROCERIES,
                description="transaction 1")

        cls.TRANSACTION2 = mapper.Transaction(amount=-20,
                currency="CAD",
                account=cls.ACCOUNT2,
                date=cls.DATE2,
                category=cls.CATEGORY_HEALTHCARE,
                description="transaction 2")

        cls.TRANSACTION3 = mapper.Transaction(amount=-30,
                currency="USD",
                account=cls.ACCOUNT3,
                date=cls.DATE3,
                category=cls.CATEGORY_DINING,
                description="transaction 3")
        print('Populated temporary data')
        cls.populate_data()

    @classmethod
    def tearDownClass(cls):
        """Destroy the temporary database"""
        print("Removing temporary DB: {}".format(cls.db_name))
        cls.client.fsync()
        cls.client.drop_database(cls.db_name)

    @classmethod
    def populate_data(cls):
        cls.ACCOUNT1.save()
        cls.ACCOUNT2.save()
        cls.ACCOUNT3.save()
        cls.CATEGORY_GROCERIES.save()
        cls.CATEGORY_HEALTHCARE.save()
        cls.CATEGORY_DINING.save()
        cls.TRANSACTION1.save()
        cls.TRANSACTION2.save()
        cls.TRANSACTION3.save()
