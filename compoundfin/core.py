import config
import mapper
import output

import argparse
import datetime
import mongoengine as mdb
import sys


def run_query(args):
    print('Executing query...')
    data = mapper.Transaction.query(start_date=args.start_date,
            end_date=args.end_date,
            category_filters=args.categories,
            currency_target=args.convert_currencies)

    print('Query complete:')
    print(data)

    if args.raw_csv:
        print('Writing raw data to csv: {}'.format(args.raw_csv))
        output.transaction_data_csv(data, args.raw_csv)

    if args.csv:
        print('Writing aggregated data to csv: {}'.format(args.csv))
        output.transaction_data_by_category_csv(data, args.csv)

    if args.plot:
        print('Plotting aggregated data to: {}'.format(args.plot))
        title = 'Transactions by Category\n{} to {}'.format(
                args.start_date.strftime(config.time_format),
                args.end_date.strftime(config.time_format))
        output.transaction_data_by_category_pie_chart(data, args.plot, title)


# timestamp generator for argument type
def timestamp(datestring):
    return datetime.datetime.strptime(datestring, config.time_format)

parser = argparse.ArgumentParser()
# the 'dest' argument is required due to a bug in argparse in Python3
subparsers = parser.add_subparsers(dest='command', help='Commands')
subparsers.required = True

# TODO: Implement "fetch" command
# fetch_parser = subparsers.add_parser('fetch',
#         help='Do the fetchy stuff')

query_parser = subparsers.add_parser('query',
        help=('Query the database, filter and specify output methods using'
              ' the command arguments'))

query_parser.set_defaults(func=run_query)

query_parser.add_argument('--start',
        help='start date (inclusive), YYYY-MM-DD',
        type=timestamp,
        dest='start_date',
        required=True)

query_parser.add_argument('--end',
        help='end date (exclusive), YYYY-MM-DD',
        type=timestamp,
        dest='end_date',
        default=datetime.datetime.today())

query_parser.add_argument('--categories',
        help='space separated list of categories to filter to',
        nargs='*',
        choices=mapper.CategoryMap.CATEGORIES)

query_parser.add_argument('--convert-currencies',
        help=('convert all transactions to one currency at the rate specified'
              ' in the configuration file'),
        choices=mapper.Account.CURRENCIES)

query_parser.add_argument('--plot',
        help=('Writes category aggregated data as a pie chart to the specified'
              ' output file. The option "--convert-currencies" must be used'
              ' with this option'))

query_parser.add_argument('--csv',
        help=('Writes category aggregated data in CSV format to the specified'
              ' output file. The option "--convert-currencies" must be used'
              ' with this option'))

query_parser.add_argument('--raw-csv',
        help='Writes data in CSV format to the specified output file')


class Application:

    def __init__(self, db_name=None):
        """Class exists to bind the application to a Mongo Database"""
        if db_name is None:
            db_name = config.DB_NAME
        self.client = mdb.connect(db_name)


def run():
    args = parser.parse_args(sys.argv[1:])
    app = Application()
    args.func(args)
