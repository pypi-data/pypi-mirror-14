# -*- coding: utf8 -*-

import pandas as _pd
from kyper.data._utils import get_data as _get_data

_VERSION = "1.0.0"
_SERVICE = "kyper_equities"


def list_symbols():
    ''' Return all available U.S. equities ticker symbols
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_symbols")
    return _pd.read_json(ret, orient="split", dtype=False)

def search_symbols(search_term=None, case=False):
    ''' Search for U.S. equities ticker symbol using a keyword or regular expression.
    '''
    ret = _get_data(_SERVICE, _VERSION, "search_symbols", search_term=search_term, case=case)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_tick_data(symbol=None, start_dt=None, end_dt=None, limit=None, session_filter=None):
    ''' Query U.S. equities market data (all trades for the time period), with limit of 1 hour
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_tick_data", symbol=symbol, start_dt=start_dt, end_dt=end_dt, limit=limit, session_filter=session_filter)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_minute_data(symbol=None, start_dt=None, end_dt=None, limit=None, interval=1, splits=True, dividends=True):
    ''' Query U.S. equities (regular trading hours) market data (aggregated by minute), with limit of 30 days.
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_minute_data", symbol=symbol, start_dt=start_dt, end_dt=end_dt, limit=limit, interval=interval, splits=splits, dividends=dividends)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_minute_data_all(symbol=None, start_dt=None, end_dt=None, limit=None, interval=1):
    ''' Query U.S. equities (both regular trading hours and after-hours) market data (aggregated by minute), with limit of 30 days. The returned data is adjusted price for splits but no dividends adjustment
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_minute_data_all", symbol=symbol, start_dt=start_dt, end_dt=end_dt, limit=limit, interval=interval)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_daily_data(symbol=None, start_date=None, end_date=None, limit=None, splits=True, dividends=True):
    ''' Query U.S. equities market data (daily aggregation).
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_daily_data", symbol=symbol, start_date=start_date, end_date=end_date, limit=limit, splits=splits, dividends=dividends)
    return _pd.read_json(ret, orient="split", dtype=False)
