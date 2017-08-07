from .context import compoundfin
from compoundfin import mapper

import datetime
import mongoengine as mdb
import unittest
import uuid

class TestMapper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Create a temporary database"""
        cls.db_name = str(uuid.uuid4())
        print("Creating temporary DB: {}".format(cls.db_name))
        cls.client = mdb.connect(cls.db_name)

    @classmethod
    def tearDownClass(cls):
        """Destroy the temporary database"""
        print("Removing temporary DB: {}".format(cls.db_name))
        cls.client.fsync()
        cls.client.drop_database(cls.db_name)

    def test_category_insertion_and_retrieval(self):
        row = mapper.CategoryMap()
        row.category = "Groceries"
        row.category_code = 9999
        row.no_cache = True
        row.save()

        # test persistence
        self.client.close()
        self.client = mdb.connect(self.db_name)
        self.assertTrue(row in mapper.CategoryMap.objects())

    def test_database_dropping(self):
        self.client.drop_database(self.db_name)
        row = mapper.CategoryMap()
        row.category = "Groceries"
        row.category_code = 1
        row.no_cache = True
        row.save()
        self.assertEqual(mapper.CategoryMap.objects().count(), 1)
        self.client.drop_database(self.db_name)

        self.assertEqual(mapper.CategoryMap.objects().count(), 0)
        row = mapper.CategoryMap()
        row.category = "Groceries"
        row.category_code = 2
        row.no_cache = True
        row.save()
        self.assertEqual(mapper.CategoryMap.objects().count(), 1)
        self.client.drop_database(self.db_name)

    def test_category_invalid(self):
        row = mapper.CategoryMap()
        row.category = "foobar"
        self.assertRaises(mdb.ValidationError, row.save)

    def test_transaction_insertion_and_retrieval(self):
        row = mapper.CategoryMap()
        row.category = "Costco"
        row.category_code = 1234
        row.save()
        row.no_cache = True
        self.assertTrue(row in mapper.CategoryMap.objects())

        trans = mapper.Transaction()
        trans.amount = -13.37
        trans.currency = "CAD"
        trans.account = "foobarz-mastercard-x1234"
        trans.date = datetime.datetime.now
        trans.description = "stuff"
        trans.category = row
        trans.no_cache = True
        trans.save()

        # test persistence
        self.client.close()
        self.client = mdb.connect(self.db_name)
        self.assertTrue(trans in mapper.Transaction.objects())

if __name__ == '__main__':
    unittest.main()
