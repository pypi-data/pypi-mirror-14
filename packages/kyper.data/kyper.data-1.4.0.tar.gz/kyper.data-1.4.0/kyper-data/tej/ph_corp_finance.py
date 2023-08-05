# -*- coding: utf8 -*-

import pandas as _pd
from kyper.data._utils import get_data as _get_data



_VERSION = "1.0.0"
_SERVICE = "tej_ph_corp_finance"


def search_corp_id(search_term=None):
    ''' Search corpration ID of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "search_corp_id", search_term=search_term)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_ytd_general(co_id=None, start_date=None, end_date=None):
    ''' Query YTD balance sheet statement for general sectors
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_ytd_general", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_ytd_general(co_id=None, start_date=None, end_date=None):
    ''' Query YTD income statement for general sectors
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_ytd_general", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_ytd_general(co_id=None, start_date=None, end_date=None):
    ''' Query YTD cash flow statement for general sectors
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_ytd_general", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_financial_ytd_general(co_id=None, start_date=None, end_date=None):
    ''' Query YTD corporate financial statements (others) for general sectors
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_financial_ytd_general", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_ytd_finance(co_id=None, start_date=None, end_date=None):
    ''' Query YTD balance sheet for finance sectors
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_ytd_finance", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_ytd_finance(co_id=None, start_date=None, end_date=None):
    ''' Query YTD simplified income statement for finance sectors
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_ytd_finance", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_ytd_finance(co_id=None, start_date=None, end_date=None):
    ''' Query YTD cash flow statement for finance sectors
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_ytd_finance", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_financial_ytd_finance(co_id=None, start_date=None, end_date=None):
    ''' Query YTD corporate financial statements (others) for finance sectors
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_financial_ytd_finance", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_ytd_insurance(co_id=None, start_date=None, end_date=None):
    ''' Query YTD balance sheet for insurance sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_ytd_insurance", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_ytd_insurance(co_id=None, start_date=None, end_date=None):
    ''' Query YTD income statement for insurance sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_ytd_insurance", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_ytd_insurance(co_id=None, start_date=None, end_date=None):
    ''' Query YTD cash flow statement for insurance sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_ytd_insurance", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_financial_ytd_insurance(co_id=None, start_date=None, end_date=None):
    ''' Query YTD corporate financial statements (others) for insurance sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_financial_ytd_insurance", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)
