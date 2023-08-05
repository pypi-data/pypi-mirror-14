# -*- coding: utf8 -*-

import pandas as _pd
from kyper.data._utils import get_data as _get_data

_VERSION = "1.0.0"
_SERVICE = "benzinga_news"


def list_channels(limit=1000):
    ''' Get news channels
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_channels", limit=limit)
    return _pd.read_json(ret, orient="split", dtype=False)

def search_tags(search_term=None, limit=1000):
    ''' Search news tags
    '''
    ret = _get_data(_SERVICE, _VERSION, "search_tags", search_term=search_term, limit=limit)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_news(search_term=None, start_dt=None, end_dt=None, published_since=None, updated_since=None, channels=None, tickers=None, tags=None, limit=1000):
    ''' Query News by keyword, ticker, or tag
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_news", search_term=search_term, start_dt=start_dt, end_dt=end_dt, published_since=published_since, updated_since=updated_since, channels=channels, tickers=tickers, tags=tags, limit=limit)
    return _pd.read_json(ret, orient="split", dtype=False)
