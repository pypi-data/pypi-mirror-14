# -*- coding: utf8 -*-

import pandas as _pd
from kyper.data._utils import get_data as _get_data

_VERSION = "0.0.2"
_SERVICE = "tej_tw_derivative"


def get_warrant_attr(co_id=None):
    ''' Query warrant attribute for the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_warrant_attr", co_id=co_id)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_warrant(co_id=None, start_date=None, end_date=None):
    ''' Query warrant price for the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_warrant", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_future_attr(co_id=None):
    ''' Query future attribute for the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_future_attr", co_id=co_id)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_future(co_id=None, start_date=None, end_date=None):
    ''' Query future price of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_future", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_option_attr(co_id=None):
    ''' Query option attribute of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_option_attr", co_id=co_id)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_option(co_id=None, start_date=None, end_date=None):
    ''' Query option price of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_option", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)
