import mapper

import argparse
import datetime
import sys


# timestamp generator for argument type
def timestamp(datestring):
    return datetime.datetime.strptime(datestring, '%Y-%m-%d')

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='Commands')

# TODO: Implement "fetch" command
# fetch_parser = subparsers.add_parser('fetch',
#         help='Do the fetchy stuff')

query_parser = subparsers.add_parser('query',
        help=('Query the database, filter and specify output methods using'
              ' the command arguments'))

query_parser.add_argument('--start',
        help='start date (inclusive), YYYY-MM-DD',
        type=timestamp,
        dest='START_DATE',
        required=True)

query_parser.add_argument('--end',
        help='end date (exclusive), YYYY-MM-DD',
        type=timestamp,
        dest='END_DATE',
        default=datetime.datetime.today())

query_parser.add_argument('--categories',
        help='space separated list of categories to filter to',
        nargs='*',
        choices=mapper.CategoryMap.CATEGORIES)

query_parser.add_argument('--convert-currencies',
        help=('convert all transactions to one currency at the rate specified'
              ' in the configuration file'),
        default="CAD",
        choices=mapper.Account.CURRENCIES)

query_parser.add_argument('--plot',
        help='Writes data as a pie chart to the specified output file')

query_parser.add_argument('--csv',
        help='Writes data in CSV format to the specified output file')


def run():
    parser.parse_args(sys.argv[1:])
    print(parser)
