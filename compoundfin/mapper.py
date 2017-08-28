import config

import mongoengine as mdb


class Category(mdb.Document):
    """Stores a category label and its optional budget"""

    CATEGORIES = (
            "Groceries",
            "Costco",
            "Dining",
            "Transportation",
            "Entertainment",
            "Shopping",
            "Healthcare",
            "Bills",
            "TBD",
            )

    label = mdb.StringField(required=True, choices=CATEGORIES)

    budget = mdb.DecimalField(required=False)


class CategoryMap(mdb.Document):
    """Stores mapping of merchant to category"""

    category = mdb.ReferenceField(Category, required=True)

    merchant = mdb.StringField(required=True, max_length=80)


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


class Transaction(mdb.Document):
    """Describes a single transaction event"""

    # dollar amount
    amount = mdb.DecimalField(required=True)

    # descriptive account name (human readable)
    account = mdb.ReferenceField(Account, required=True)

    # date of transaction
    date = mdb.DateTimeField(required=True)

    # full description either from original statement or provided by user
    description = mdb.StringField(required=False, max_length=80)

    category = mdb.ReferenceField(Category)

    # TODO - not sure if this date index works
    meta = {
            'ordering': ['-date'],
            'indexes': ['date'],
           }

    def csv_row(self):
        return ",".join([
                self.date.strftime(config.time_format),
                self.category.label,
                self.account.description,
                self.description,
                '{:.2f}'.format(self.amount),
                ]) + '\n'

    @staticmethod
    def csv_header():
        return ",".join([
                'date (YYYY-MM-DD)',
                'category',
                'account',
                'description',
                'amount',
                ]) + '\n'

    @staticmethod
    def query(start_date, end_date, category_filters=None):
        """Returns a list of filtered and mutated objects"""

        if category_filters:
            categories = Category.objects(
                    label__in=category_filters)

            results = Transaction.objects(
                    date__gte=start_date,
                    date__lt=end_date,
                    category__in=categories)
        else:
            results = Transaction.objects(
                    date__gte=start_date,
                    date__lt=end_date)

        return results
