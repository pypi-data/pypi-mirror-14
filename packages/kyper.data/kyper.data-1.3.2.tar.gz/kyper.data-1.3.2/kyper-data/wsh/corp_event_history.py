# -*- coding: utf8 -*-

import pandas as _pd
from kyper.data._utils import get_data as _get_data

_VERSION = "1.0.0"
_SERVICE = "wsh_corp_event_history"


def search_symbols(search_term=None):
    ''' Search for ticker symbol using a keyword or regular expression.
    '''
    ret = _get_data(_SERVICE, _VERSION, "search_symbols", search_term=search_term)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_shareholder_meetings(symbols=None, start_date=None, end_date=None, meeting_types=['B', 'S']):
    ''' Query shareholder meetings of stock symbol(s).
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_shareholder_meetings", symbols=symbols, start_date=start_date, end_date=end_date, meeting_types=meeting_types)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_conference_calls(symbols=None, start_dt=None, end_dt=None, quarters=['Q1', 'Q2', 'Q3', 'Q4'], fiscal_years=['*']):
    ''' Query conference calls history of stock symbol.
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_conference_calls", symbols=symbols, start_dt=start_dt, end_dt=end_dt, quarters=quarters, fiscal_years=fiscal_years)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_earning_datebreaks(symbols=None, e_change_types=['DTT', 'DTV', 'DVT', 'DVV', 'XTV', 'XVT', 'XVV', 'NQ', 'HST'], start_dt=None, end_dt=None, quarters=['Q1', 'Q2', 'Q3', 'Q4'], fiscal_years=['*'], time_of_day=['B', 'D', 'A', 'U'], e_types=['V', 'T', 'I'], a_sources=['RESEARCH', 'NEWS', 'BASE']):
    ''' Query history of process of earnings date changes for stock symbol(s).
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_earning_datebreaks", symbols=symbols, e_change_types=e_change_types, start_dt=start_dt, end_dt=end_dt, quarters=quarters, fiscal_years=fiscal_years, time_of_day=time_of_day, e_types=e_types, a_sources=a_sources)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_dividends(symbols=None, start_date=None, end_date=None, div_freq=None):
    ''' Query history of dividends for stock symbol(s).
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_dividends", symbols=symbols, start_date=start_date, end_date=end_date, div_freq=div_freq)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_EPS(symbols=None, start_dt=None, end_dt=None, quarters=['Q1', 'Q2', 'Q3', 'Q4'], fiscal_years=['*']):
    ''' Query history of EPS actuals for stock symbol(s).
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_EPS", symbols=symbols, start_dt=start_dt, end_dt=end_dt, quarters=quarters, fiscal_years=fiscal_years)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_splits(symbols=None, start_date=None, end_date=None):
    ''' Query history of stock splits for stock symbol(s).
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_splits", symbols=symbols, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)
