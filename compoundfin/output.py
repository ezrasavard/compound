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

    agg = {x: {'amount': 0.0} for x in mapper.Category.CATEGORIES}
    for row in data:
        agg[row.category.label]['amount'] += float(row.amount)
        if row.category.budget is not None:
            agg[row.category.label]['budget'] = float(row.category.budget)

    return agg


def transaction_data_by_category_csv(data, outfile):
    """
    Make a CSV aggregating the transaction data by category

    @param data: a list of mapper.Transaction objects
    @param outfile: string designating the desired output file to write
    """

    with open(outfile, 'w') as f:
        f.write('category,budget,spent\n')
        aggs = _aggregate_transactions_by_category(data)
        for category, quantities in aggs.items():
            spent = -1 * quantities['amount']
            budget = quantities.get('budget', 0.0)
            f.write('{}, {:.2f}, {:.2f}\n'
                    .format(category, budget, spent))


def transaction_data_by_category_pie_chart(data, outfile, title):
    """
    Make a pie chart from transaction data
    The image format will be interpreted from the file extension
    See SUPPORTED_IMAGE_FORMATS for options

    @param data: a list of mapper.Transaction objects
    @param outfile: string designating the desired output file to write
    @param title: string to use at the title in the image
    """

    image_format = os.path.splittext(outfile)[1][1:]

    if image_format not in SUPPORTED_IMAGE_FORMATS:
        raise ValueError(('unsupported image format {}. File extension must'
                          ' be one of {}').format(image_format,
                              SUPPORTED_IMAGE_FORMATS))

    agg = _aggregate_transactions_by_category(data)

    labels = []
    sizes = []
    for label, qty in agg.items():
        spent = -1 * qty['amount']
        labels.append('{}: ${:.0f}'.format(label, spent))
        sizes.append(int(spent))

    plt.pie(sizes, labels=labels, shadow=True)
    plt.axis('equal')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outfile, format=image_format)
