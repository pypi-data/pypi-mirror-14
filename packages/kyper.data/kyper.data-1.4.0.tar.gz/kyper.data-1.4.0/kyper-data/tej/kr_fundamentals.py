# -*- coding: utf8 -*-

import pandas as _pd
from kyper.data._utils import get_data as _get_data



_VERSION = "1.0.0"
_SERVICE = "tej_kr_fundamentals"


def search_corp_id(search_term=None):
    ''' Search corpration ID of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "search_corp_id", search_term=search_term)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_company_attr(co_id=None):
    ''' Query company attribute of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_company_attr", co_id=co_id)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_corporate_act(co_id=None, start_date=None, end_date=None):
    ''' Query corporate action of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_corporate_act", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_dividends(co_id=None, start_date=None, end_date=None):
    ''' Query cash dividend of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_dividends", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_sales_bd(co_id=None, start_date=None, end_date=None):
    ''' Query annually sales break down of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_sales_bd", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_substantial_holding(co_id=None, start_date=None, end_date=None):
    ''' Query substantial share holding information of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_substantial_holding", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)
