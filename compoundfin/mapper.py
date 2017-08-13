import mongoengine as mdb


class CategoryMap(mdb.Document):
    """
    Stores historical mapping of merchant category codes
    to human readable categories
    """

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
    code = mdb.IntField(required=False, max_length=4)

    # category name (human readable)
    description = mdb.StringField(required=True, choices=CATEGORIES)


class Account(mdb.Document):
    """Stores all accounts of interest, including closed accounts"""

    BANKS = {
            "CapitalOne",
            "Chase",
            "Tangerine",
            "RBC",
            "Fidelity",
            }

    CARD_TYPES = {
            "VISA",
            "MASTERCARD",
            "AMEX",
            "DEBIT",
            }

    CURRENCIES = (
            "CAD",
            "USD",
            )

    # Financial institution backing the account
    bank = mdb.StringField(required=True, choices=BANKS)

    # The type of card
    card_type = mdb.StringField(required=True, choices=CARD_TYPES)

    # Last four digits of the card
    last_four = mdb.IntField(required=True, min_length=4, max_length=4)

    # The date the account was closed, if no longer active
    closed_date = mdb.DateTimeField()

    # descriptive information like "Costco" or "Amazon Canadian Visa"
    description = mdb.StringField(max_length=80)

    # native currency for the card
    native_currency = mdb.StringField(required=True, max_length=3,
            choices=CURRENCIES)


class Transaction(mdb.Document):
    """Describes a single transaction event"""

    # dollar amount in specified currency
    amount = mdb.DecimalField(required=True)

    # three letter currency code
    currency = mdb.StringField(required=True, max_length=3,
            choices=Account.CURRENCIES)

    # descriptive account name (human readable)
    account = mdb.ReferenceField(Account, required=True)

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
