# -*- coding: utf8 -*-

import pandas as _pd
from kyper.data._utils import get_data as _get_data

_VERSION = "1.0.0"
_SERVICE = "benzinga_calendar"


def list_categories():
    ''' List all calendar categories
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_categories")
    return _pd.read_json(ret, orient="split", dtype=False)

def list_fields(category=None):
    ''' Return all fields with description of specified category.
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_fields", category=category)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_dividends(start_date=None, end_date=None, date_filter=None, tickers=None, importance=0, limit=1000, fields=None):
    ''' Get events of dividends calendar
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_dividends", start_date=start_date, end_date=end_date, date_filter=date_filter, tickers=tickers, importance=importance, limit=limit, fields=fields)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_earnings(start_date=None, end_date=None, tickers=None, importance=0, limit=1000, fields=None):
    ''' Get events of earnings calendar
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_earnings", start_date=start_date, end_date=end_date, tickers=tickers, importance=importance, limit=limit, fields=fields)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_economics(start_date=None, end_date=None, country=None, importance=0, limit=1000, fields=None):
    ''' Get events of economics calendar
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_economics", start_date=start_date, end_date=end_date, country=country, importance=importance, limit=limit, fields=fields)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_guidance(start_date=None, end_date=None, tickers=None, importance=0, limit=1000, fields=None):
    ''' Get events of guidance calendar
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_guidance", start_date=start_date, end_date=end_date, tickers=tickers, importance=importance, limit=limit, fields=fields)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_ipos(start_date=None, end_date=None, tickers=None, limit=1000, fields=None):
    ''' Get events of ipos calendar
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_ipos", start_date=start_date, end_date=end_date, tickers=tickers, limit=limit, fields=fields)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_ratings(start_date=None, end_date=None, tickers=None, importance=0, action=None, limit=1000, fields=None):
    ''' Get events of ratings calendar
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_ratings", start_date=start_date, end_date=end_date, tickers=tickers, importance=importance, action=action, limit=limit, fields=fields)
    return _pd.read_json(ret, orient="split", dtype=False)
