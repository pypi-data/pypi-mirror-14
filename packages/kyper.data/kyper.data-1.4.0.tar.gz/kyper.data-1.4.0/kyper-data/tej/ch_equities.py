# -*- coding: utf8 -*-

import pandas as _pd
from kyper.data._utils import get_data as _get_data

_VERSION = "0.0.2"
_SERVICE = "tej_ch_equities"


def search_corp_id(search_term=None):
    ''' Search corpration ID of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "search_corp_id", search_term=search_term)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_company_attr(co_id=None):
    ''' Query company attribute
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_company_attr", co_id=co_id)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_meeting(co_id=None, start_date=None, end_date=None):
    ''' Query meeting information for the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_meeting", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_ipo(co_id=None):
    ''' Query ipo information of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_ipo", co_id=co_id)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_corporate_act(co_id=None, start_date=None, end_date=None):
    ''' Query corporate action for the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_corporate_act", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_dividend(co_id=None, start_date=None, end_date=None):
    ''' Query dividend information for the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_dividend", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_director_holding(co_id=None, start_date=None, end_date=None):
    ''' Query directors holding information for the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_director_holding", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_consolidated_sub(co_id=None, start_date=None, end_date=None):
    ''' Query consolidated subsidary information for the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_consolidated_sub", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_sale_bd(co_id=None, start_date=None, end_date=None):
    ''' Query annual product sales break down of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_sale_bd", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_adjust_price(co_id=None, start_date=None, end_date=None):
    ''' Query adjusted stock price of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_adjust_price", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_margin_trading(co_id=None, start_date=None, end_date=None):
    ''' Query trading margin information of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_margin_trading", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)
