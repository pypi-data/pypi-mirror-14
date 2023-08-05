#!/usr/bin/python

import argparse
import os
import sys
from sheetsite.site import Site
from sheetsite.source import read_source

def run():
    parser = argparse.ArgumentParser(description='Run a website from a spreadsheet. '
                                     'Take a spreadsheet (from google sheets or locally), and '
                                     'convert it to a .json file that a static website '
                                     'generator like jekyll can use.  Optionally strip private '
                                     'information and add derived geographic fields like '
                                     'latitude and longitude.')
    parser.add_argument('--credential', nargs=1, required=False, help='credential json file '
                        'from google, see http://gspread.readthedocs.org/en/latest/oauth2.html '
                        '(and don\'t forget to share the spreadsheet with the client_email you '
                        'will find in the json google gives you)')
    parser.add_argument('--geocache', nargs=1, required=False, default=['sheetsite_geo.sqlite'],
                        help='name of file to use for caching geographic lookups.')
    parser.add_argument('spreadsheet',help='name of spreadsheet - either a local .xls(x) file, '
                        'or the name (or key) of a spreadsheet on google sheets')
    parser.add_argument('output_file', nargs='?', default=None,
                        help='file to write public sheets to, either output.json or output.xls(x). '
                        'When saving to json, the first row is assumed to contain column names. '
                        'When saving to xls(x), the file will not retain original formatting.')
    parser.add_argument('private_output_file', nargs='?', default=None,
                        help='file to write private sheets to.')
    parser.add_argument('--include', nargs='*', required=False, help='sheet name to include.')
    parser.add_argument('--exclude', nargs='*', required=False, help='sheet name to exclude.')
    parser.add_argument('--fill', nargs='*', required=False, help='special columns to fill, by name.')

    args = parser.parse_args()

    params = {}

    if os.path.exists(args.spreadsheet) and args.credential is None:
        params['filename'] = args.spreadsheet
    elif args.credential is None:
        raise IOError("Spreadsheet not found locally, "
                      "and no credentials given for looking online.")
    else:
        params['credential_file'] = args.credential[0]
        params['key'] = args.spreadsheet

    wb = read_source(params)
    ss = Site(wb, args.geocache[0])
    ss.add_sheet_filter(args.include, args.exclude)
    ss.add_column_fills(args.fill)
    ss.save_local(args.output_file)
    if args.private_output_file is not None:
        ss.save_local(args.private_output_file, private_sheets=True)
