# -*- coding: utf8 -*-

import pandas as _pd
from kyper.data._utils import get_data as _get_data

_VERSION = "0.0.2"
_SERVICE = "tej_tw_equities"


def get_adjusted_price(co_id=None, start_date=None, end_date=None):
    ''' Query adjusted stock price of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_adjusted_price", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_central_depo(co_id=None, start_date=None, end_date=None):
    ''' Query central deposit information of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_central_depo", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_company_attr(co_id=None):
    ''' Query attribute of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_company_attr", co_id=co_id)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_corporate_act(co_id=None, start_date=None, end_date=None):
    ''' Query corporate actions of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_corporate_act", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_deposit_stat(co_id=None, start_date=None, end_date=None):
    ''' Query deposit statistics of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_deposit_stat", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_directors_holding(co_id=None, start_date=None, end_date=None):
    ''' Query directors holding for the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_directors_holding", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_dividends_policy(co_id=None, start_date=None, end_date=None):
    ''' Query dividends policy of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_dividends_policy", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_dividends(co_id=None, start_date=None, end_date=None):
    ''' Query cash dividend information of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_dividends", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_equity_view(co_id=None, start_date=None, end_date=None):
    ''' Query equity view for the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_equity_view", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_holding_trans(co_id=None, start_date=None, end_date=None):
    ''' Query holding transfer information of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_holding_trans", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_invest_ch(co_id=None, start_date=None, end_date=None):
    ''' Query investment in china (china companies) of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_invest_ch", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_invest_trans(co_id=None, start_date=None, end_date=None):
    ''' Query investment transfer of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_invest_trans", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_ipo(co_id=None):
    ''' Query IPO information for the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_ipo", co_id=co_id)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_longterm_invest(co_id=None, start_date=None, end_date=None):
    ''' Query Long-Term investment details of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_longterm_invest", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_sales(co_id=None, start_date=None, end_date=None):
    ''' Query monthly sales of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_sales", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_sales_bd(co_id=None, start_date=None, end_date=None):
    ''' Query annually sales break down of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_sales_bd", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_suspended_rec(co_id=None, start_date=None, end_date=None):
    ''' Query suspended records of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_suspended_rec", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def search_corp_id(search_term=None):
    ''' Search corpration ID of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "search_corp_id", search_term=search_term)
    return _pd.read_json(ret, orient="split", dtype=False)
