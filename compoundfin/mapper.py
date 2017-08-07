import mongoengine as mdb


"""
Stores historical mapping of merchant category codes
to human readable categories
"""
class CategoryMap(mdb.Document):

    CATEGORIES = (
            "Groceries",
            "Costco",
            "Dining",
            "Transportation",
            "Entertainment",
            "Shopping",
            "Healthcare",
            "Bills",
            )

    # IRS merchant category code
    category_code = mdb.IntField(required=False, max_length=4)

    # category name (human readable)
    category = mdb.StringField(required=True, choices=CATEGORIES)


"""Describes a single transaction event"""
class Transaction(mdb.Document):

    CURRENCIES = (
            "CAD",
            "USD",
            )

    # dollar amount in specified currency
    amount = mdb.DecimalField(required=True)
    
    # three letter currency code
    currency = mdb.StringField(required=True, max_length=3,
            choices=CURRENCIES)

    # descriptive account name (human readable)
    account = mdb.StringField(required=True, max_length=80)

    # date of transaction
    date = mdb.DateTimeField(required=True)

    # full description either from original statement or provided by user
    description = mdb.StringField(required=False, max_length=80)

    category = mdb.ReferenceField(CategoryMap)

    # TODO - not sure if this date index works
    meta = {
            'ordering': ['-date'],
            'indexes': ['date'],
           }

