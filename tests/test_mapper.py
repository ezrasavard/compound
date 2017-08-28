from .context import compoundfin
from . import util
from compoundfin import core
from compoundfin import mapper

import datetime
import mongoengine as mdb


class TestMapper(util.DBTest):

    def test_category_insertion_and_retrieval(self):
        row = mapper.CategoryMap()
        row.category = "Groceries"
        row.merchant = "Foobar's Vegetables"
        row.no_cache = True
        row.save()

        # test persistence
        self.client.close()
        self.client = mdb.connect(self.db_name)
        self.assertTrue(row in mapper.CategoryMap.objects())

    def test_category_invalid(self):
        row = mapper.CategoryMap()
        row.category = "foobar"
        self.assertRaises(mdb.ValidationError, row.save)

    def test_transaction_insertion_and_retrieval(self):
        row = mapper.CategoryMap()
        row.category = "Costco"
        row.merchant = "CostcoPurchaseSomethingSomething"
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
                category_filters=[self.CATEGORY_GROCERIES.category])
        self.assertEquals(len(results), 1)

    def test_transaction_query_multi_category_filtering(self):
        results = mapper.Transaction.query(start_date=self.DATE1,
                end_date=self.DATE4,
                category_filters=[self.CATEGORY_GROCERIES.category,
                    self.CATEGORY_HEALTHCARE.category])
        self.assertEquals(len(results), 2)
