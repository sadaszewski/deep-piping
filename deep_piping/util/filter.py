#
# Copyright (C) Stanislaw Adaszewski, 2021.
# See LICENSE for terms.
#

import pandas as pd
import re


class FilterColumns(pd.DataFrame):
    def __init__(self, df, include_columns=None, exclude_columns=None):
        super().__init__()
        rx_i = None
        rx_e = None
        if include_columns is not None:
            rx_i = re.compile('(' + '|'.join(include_columns) + ')')
        if exclude_columns is not None:
            rx_e = re.compile('(' + '|'.join(exclude_columns) + ')')
        for k, v in df.items():
            if rx_e is not None and rx_e.search(k):
                continue
            if rx_i is not None and not rx_i.search(k):
                continue
            self[k] = v
