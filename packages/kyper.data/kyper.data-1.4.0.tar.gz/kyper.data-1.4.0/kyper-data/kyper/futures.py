# -*- coding: utf8 -*-

import pandas as _pd
from kyper.data._utils import get_data as _get_data

_VERSION = "1.0.0"
_SERVICE = "kyper_futures"


def list_symbols():
    ''' Return all available U.S. futures ticker symbols
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_symbols")
    return _pd.read_json(ret, orient="split", dtype=False)

def search_symbols(search_term=None, case=False):
    ''' Search for U.S. futures ticker symbol using a keyword or regular expression.
    '''
    ret = _get_data(_SERVICE, _VERSION, "search_symbols", search_term=search_term, case=case)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_tick_data(symbol=None, delivery=None, start_dt=None, end_dt=None, limit=None, session_filter=None):
    ''' Query U.S. futures contract market data (all trades for the time period), with limit of 1 hour
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_tick_data", symbol=symbol, delivery=delivery, start_dt=start_dt, end_dt=end_dt, limit=limit, session_filter=session_filter)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_minute_data(symbol=None, delivery=None, start_dt=None, end_dt=None, limit=None, interval=1):
    ''' Query U.S. futures contract market data (aggregated by minute), with limit of 30 days
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_minute_data", symbol=symbol, delivery=delivery, start_dt=start_dt, end_dt=end_dt, limit=limit, interval=interval)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_minute_data_continuous(symbol=None, start_dt=None, end_dt=None, limit=None, interval=1):
    ''' Query U.S. futures (front-month) contract market data (aggregated by minute, auto-switching to next front-month contract after expired), with limit of 30 days
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_minute_data_continuous", symbol=symbol, start_dt=start_dt, end_dt=end_dt, limit=limit, interval=interval)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_daily_data(symbol=None, delivery=None, start_date=None, end_date=None, limit=None, volume="contract"):
    ''' Query U.S. futures contract market data (daily aggregation).
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_daily_data", symbol=symbol, delivery=delivery, start_date=start_date, end_date=end_date, limit=limit, volume=volume)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_daily_data_continuous(symbol=None, start_date=None, end_date=None, limit=None, volume="contract", nearby=1):
    ''' Query U.S. futures (front-month) contract market data (aggregated daily, auto-switching to next front-month contract after expired)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_daily_data_continuous", symbol=symbol, start_date=start_date, end_date=end_date, limit=limit, volume=volume, nearby=nearby)
    return _pd.read_json(ret, orient="split", dtype=False)
