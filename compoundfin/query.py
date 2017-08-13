import config
import mapper

import datetime


class Transactions():

    start_date = None
    end_date = None
    category_filters = []
    currency_target = None
    plot_output_file = None
    csv_output_file = None

    def execute(self):

        if self.category_filters:
            categories = mapper.CategoryMap.objects(
                    description__in=self.category_filters)

            results = mapper.Transaction.objects(
                    date__gte=self.start_date,
                    date__lt=self.end_date,
                    category__in=categories)
        else:
            results = mapper.Transaction.objects(
                    date__gte=self.start_date,
                    date__lt=self.end_date)

        results = [self._convert_currency(x) for x in results]

        # TODO write the CSV

        # TODO plot the pie chart

        return results

    def _convert_currency(self, row):
        if self.currency_target is not None:
            rate = config.EXCHANGE_RATES[self.currency_target][row.currency]
            row.amount *= rate
        return row
