# -*- coding: utf8 -*-

import pandas as _pd
from kyper.data._utils import get_data as _get_data

_VERSION = "0.0.2"
_SERVICE = "tej_tw_fund_bond"


def get_fund_attr(co_id=None):
    ''' Query fund attribute information
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_fund_attr", co_id=co_id)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_fund_portfolio(co_id=None, start_date=None, end_date=None):
    ''' Query investment portfolio of the fund
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_fund_portfolio", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_fund_nav(co_id=None, start_date=None, end_date=None):
    ''' Query net asset value information of the fund
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_fund_nav", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_bond_attr(co_id=None):
    ''' Query bond attribute information
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_bond_attr", co_id=co_id)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_bond(co_id=None, start_date=None, end_date=None):
    ''' Query bond trading price information
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_bond", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_bond_otc(co_id=None, start_date=None, end_date=None):
    ''' Query government bond trading system (OTC and Securities Firms only) information
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_bond_otc", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)
