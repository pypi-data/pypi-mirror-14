# This file is part of csvpandas
#
#    csvpandas is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    csvpandas is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with csvpandas.  If not, see <http://www.gnu.org/licenses/>.

"""Run stats on a dataframe
"""

import logging
import pandas

log = logging.getLogger(__name__)


def build_parser(parser):
    parser.add_argument(
        '--describe',
        action='store_true',
        help='Generate various summary statistics, excluding NaN values.')
    return parser


def action(args):
    report = []

    for col in args.csv.columns:
        for dtype in [int, float]:
            try:
                args.csv[col] = args.csv[col].astype(dtype)
                break
            except ValueError:
                continue

        if args.describe:
            report.append(args.csv[col].describe())

    report_df = pandas.concat(report, axis=1, ignore_index=True)
    report_df.to_csv(args.out)
