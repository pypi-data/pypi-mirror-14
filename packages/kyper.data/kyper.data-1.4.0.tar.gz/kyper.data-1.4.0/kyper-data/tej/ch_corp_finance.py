# -*- coding: utf8 -*-

import pandas as _pd
from kyper.data._utils import get_data as _get_data

_VERSION = "0.0.2"
_SERVICE = "tej_ch_corp_finance"


def search_corp_id(search_term=None):
    ''' Search corpration ID of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "search_corp_id", search_term=search_term)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_ytd_sim(co_id=None, start_date=None, end_date=None):
    ''' Query (simplified) balance sheet of the company (YTD, All sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_ytd_sim", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_ytd_sim(co_id=None, start_date=None, end_date=None):
    ''' Query (simplified) income statement of the company (YTD, All sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_ytd_sim", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_ytd_sim(co_id=None, start_date=None, end_date=None):
    ''' Query (simplified) cash flow statement of the company (YTD, All sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_ytd_sim", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_financial_ytd_sim(co_id=None, start_date=None, end_date=None):
    ''' Query (simplified) others corporation fiancials of the company (YTD, All sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_financial_ytd_sim", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_qr_sim(co_id=None, start_date=None, end_date=None):
    ''' Query (simplified) balance sheet of the company (Quartely, All sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_qr_sim", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_qr_sim(co_id=None, start_date=None, end_date=None):
    ''' Query (simplified) income statement of the company (Quartely, All sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_qr_sim", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_qr_sim(co_id=None, start_date=None, end_date=None):
    ''' Query (simplified) cash flow statement(Quartely, All sector) of the company cnmq1
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_qr_sim", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_finanicial_qr_sim(co_id=None, start_date=None, end_date=None):
    ''' Query (simplified) other corporation fiancials of the company (Quartely, All sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_finanicial_qr_sim", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_ytd_general(co_id=None, start_date=None, end_date=None):
    ''' Query balance sheet of the company (YTD, General sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_ytd_general", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_ytd_bank(co_id=None, start_date=None, end_date=None):
    ''' Query balance sheet of the company (YTD, Banking sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_ytd_bank", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_ytd_insurance(co_id=None, start_date=None, end_date=None):
    ''' Query balance sheet of the company (YTD, Insurance sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_ytd_insurance", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_ytd_security(co_id=None, start_date=None, end_date=None):
    ''' Query balance sheet of the company (YTD, Security sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_ytd_security", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_ytd_general(co_id=None, start_date=None, end_date=None):
    ''' Query income statement of the company (YTD, General sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_ytd_general", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_ytd_bank(co_id=None, start_date=None, end_date=None):
    ''' Query income statement of the company (YTD, Banking sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_ytd_bank", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_ytd_insurance(co_id=None, start_date=None, end_date=None):
    ''' Query income statement of the company (YTD, Insurance sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_ytd_insurance", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_ytd_security(co_id=None, start_date=None, end_date=None):
    ''' Query income statement of the company (YTD, Security sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_ytd_security", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_ytd_general(co_id=None, start_date=None, end_date=None):
    ''' Query cash flow of the company (YTD, General sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_ytd_general", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_ytd_bank(co_id=None, start_date=None, end_date=None):
    ''' Query cash flow of the company (YTD, Banking sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_ytd_bank", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_ytd_insurance(co_id=None, start_date=None, end_date=None):
    ''' Query cash flow of the company (YTD, Insurance sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_ytd_insurance", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_ytd_security(co_id=None, start_date=None, end_date=None):
    ''' Query cash flow of the company (YTD, Security sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_ytd_security", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_financial_ytd_general(co_id=None, start_date=None, end_date=None):
    ''' Query other corporation fiancials of the company (YTD, General sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_financial_ytd_general", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_financial_ytd_bank(co_id=None, start_date=None, end_date=None):
    ''' Query other corporation fiancials of the company (YTD, Banking sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_financial_ytd_bank", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_financial_ytd_insurance(co_id=None, start_date=None, end_date=None):
    ''' Query other corporation fiancials of the company (YTD, Insurance sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_financial_ytd_insurance", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_financial_ytd_security(co_id=None, start_date=None, end_date=None):
    ''' Query other corporation fiancials of the company (YTD, Security sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_financial_ytd_security", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_qr_general(co_id=None, start_date=None, end_date=None):
    ''' Query balance sheet of the company (quarterly, General sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_qr_general", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_qr_bank(co_id=None, start_date=None, end_date=None):
    ''' Query balance sheet of the company (quarterly, Banking sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_qr_bank", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_qr_insurance(co_id=None, start_date=None, end_date=None):
    ''' Query balance sheet of the company (quarterly, Insurance sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_qr_insurance", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_qr_security(co_id=None, start_date=None, end_date=None):
    ''' Query balance sheet of the company (quarterly, Security sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_qr_security", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_qr_general(co_id=None, start_date=None, end_date=None):
    ''' Query income statement of the company (quarterly, General sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_qr_general", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_qr_bank(co_id=None, start_date=None, end_date=None):
    ''' Query income statement of the company (quarterly, Banking sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_qr_bank", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_qr_insurance(co_id=None, start_date=None, end_date=None):
    ''' Query income statement of the company (quarterly, Insurance sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_qr_insurance", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_qr_security(co_id=None, start_date=None, end_date=None):
    ''' Query income statement of the company (quarterly, Security sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_qr_security", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_qr_general(co_id=None, start_date=None, end_date=None):
    ''' Query cash flow of the company (quarterly, General sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_qr_general", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_qr_bank(co_id=None, start_date=None, end_date=None):
    ''' Query cash flow of the company (quarterly, Banking sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_qr_bank", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_qr_insurance(co_id=None, start_date=None, end_date=None):
    ''' Query cash flow of the company (quarterly, Insurance sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_qr_insurance", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_qr_security(co_id=None, start_date=None, end_date=None):
    ''' Query cash flow of the company (quarterly, Security sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_qr_security", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_financial_qr_general(co_id=None, start_date=None, end_date=None):
    ''' Query other corporation fiancials of the company (quarterly, General sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_financial_qr_general", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_financial_qr_bank(co_id=None, start_date=None, end_date=None):
    ''' Query other corporation fiancials of the company (quarterly, Banking sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_financial_qr_bank", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_financial_qr_insurance(co_id=None, start_date=None, end_date=None):
    ''' Query other corporation fiancials of the company (quarterly, Insurance sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_financial_qr_insurance", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_financial_qr_security(co_id=None, start_date=None, end_date=None):
    ''' Query other corporation fiancials of the company (quarterly, Security sector)
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_financial_qr_security", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)
