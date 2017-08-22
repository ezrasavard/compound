import mapper

import matplotlib.pyplot as plt
import os


SUPPORTED_IMAGE_FORMATS = [
        'svg',
        'png',
        ]


def transaction_data_csv(data, outfile):
    """
    Make a CSV from all rows of the transaction data

    @param data: a list of mapper.Transaction objects
    @param outfile: string designating the desired output file to write
    """

    with open(outfile, 'w') as f:
        f.write(mapper.Transaction.csv_header())
        for row in data:
            f.write(row.csv_row())


def _aggregate_transactions_by_category(data):
    """Reduce all transactions to a single sum for each category"""

    agg = {x: 0.0 for x in mapper.CategoryMap.CATEGORIES}
    for row in data:
        agg[row.category.description] += row.amount

    return sorted(agg)


def _validate_single_currency(data):
    currencies = set([x.currency for x in data])
    if len(currencies) != 1:
        raise ValueError('Data must use a single currency, received: {}'
                .format(currencies))

    return currencies[0]


def transaction_data_by_category_csv(data, outfile):
    """
    Make a CSV aggregating the transaction data by category

    @param data: a list of mapper.Transaction objects in a single currency
    @param outfile: string designating the desired output file to write
    """

    currency = _validate_single_currency(data)
    with open(outfile, 'w') as f:
        f.write('category,amount')
        for category, amount in _aggregate_transactions_by_category(data):
            f.write('{},{:.2f} {}'.format(category, amount, currency))


def transaction_data_by_category_pie_chart(data, outfile, title):
    """
    Make a pie chart from transaction data
    The image format will be interpreted from the file extension
    See SUPPORTED_IMAGE_FORMATS for options

    @param data: a list of mapper.Transaction objects in a single currency
    @param outfile: string designating the desired output file to write
    @param title: string to use at the title in the image
    """

    currency = _validate_single_currency(data)
    image_format = os.path.splittext(outfile)[1][1:]

    if image_format not in SUPPORTED_IMAGE_FORMATS:
        raise ValueError(('unsupported image format {}. File extension must'
                          ' be one of {}').format(image_format,
                              SUPPORTED_IMAGE_FORMATS))

    agg = _aggregate_transactions_by_category(data)
    labels = [x[0] for x in agg]
    sizes = ['${} {}'.format(int(x[1]), currency) for x in agg]

    plt.pie(sizes, labels=labels, shadow=True)
    plt.axis('equal')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outfile, format=image_format)
