import config
import mapper

import argparse
import datetime
import mongoengine as mdb
import sys


def run_query(args):
    print("Executing query...")
    client = mdb.connect(config.DB_NAME)
    results = mapper.Transaction.query(start_date=args.start_date,
            end_date=args.end_date,
            category_filters=args.categories,
            currency_target=args.convert_currencies)

    print("Query complete:")
    print(results)
    # TODO do output stuff here with CSV and plotting


# timestamp generator for argument type
def timestamp(datestring):
    return datetime.datetime.strptime(datestring, '%Y-%m-%d')

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
        help='Writes data as a pie chart to the specified output file')

query_parser.add_argument('--csv',
        help='Writes data in CSV format to the specified output file')


def run():
    args = parser.parse_args(sys.argv[1:])
    args.func(args)
