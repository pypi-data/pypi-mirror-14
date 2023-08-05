# -*- coding: utf8 -*-

import pandas as _pd
from kyper.data._utils import get_data as _get_data

_VERSION = "0.0.2"
_SERVICE = "tej_tw_corp_finance"


def search_corp_id(search_term=None):
    ''' Search corpration ID of the company
    '''
    ret = _get_data(_SERVICE, _VERSION, "search_corp_id", search_term=search_term)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_ytd_sim(co_id=None, start_date=None, end_date=None):
    ''' Query YTD simplified balance sheet for all sectors
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_ytd_sim", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_ytd_sim(co_id=None, start_date=None, end_date=None):
    ''' Query YTD simplified income statement for all sectors
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_ytd_sim", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_ytd_sim(co_id=None, start_date=None, end_date=None):
    ''' Query YTD cash flow statement for all sectors
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_ytd_sim", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_financial_ytd_sim(co_id=None, start_date=None, end_date=None):
    ''' Query YTD simplified corporate financial statements (others) for all sectors
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_financial_ytd_sim", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_qr_sim(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly simplified balance sheet for all sectors
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_qr_sim", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_qr_sim(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly simplified income statement for all sectors
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_qr_sim", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_qr_sim(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly simplified cash flow statement for all sectors
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_qr_sim", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_finanicial_qr_sim(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly financial statements (other) for all sectors
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_finanicial_qr_sim", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_ytd_general(co_id=None, start_date=None, end_date=None):
    ''' Query YTD balance sheet for general sectors
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_ytd_general", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_ytd_general(co_id=None, start_date=None, end_date=None):
    ''' Query YTD simplified income statement for general sectors
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

def get_balance_sheet_qr_general(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly balance sheet for general sectors
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_qr_general", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_qr_general(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly income statement for general sectors
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_qr_general", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_qr_general(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly cash flow statement for general sectors
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_qr_general", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_finanicial_qr_general(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly financial statements (other) for general sectors
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_finanicial_qr_general", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_ytd_bank(co_id=None, start_date=None, end_date=None):
    ''' Query YTD balance sheet for banking sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_ytd_bank", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_ytd_bank(co_id=None, start_date=None, end_date=None):
    ''' Query YTD income statement for banking sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_ytd_bank", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_ytd_bank(co_id=None, start_date=None, end_date=None):
    ''' Query YTD cash flow statement for banking sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_ytd_bank", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_financial_ytd_bank(co_id=None, start_date=None, end_date=None):
    ''' Query YTD corporate financial statements (others) for banking sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_financial_ytd_bank", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_qr_bank(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly balance sheet for banking sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_qr_bank", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_qr_bank(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly income statement for banking sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_qr_bank", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_qr_bank(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly cash flow statement for banking sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_qr_bank", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_finanicial_qr_bank(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly financial statements (other) for banking sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_finanicial_qr_bank", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_ytd_FHC(co_id=None, start_date=None, end_date=None):
    ''' Query YTD balance sheet for financial holdings sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_ytd_FHC", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_ytd_FHC(co_id=None, start_date=None, end_date=None):
    ''' Query YTD income statement for financial holdings sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_ytd_FHC", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_ytd_FHC(co_id=None, start_date=None, end_date=None):
    ''' Query YTD cash flow statement for financial holdings sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_ytd_FHC", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_financial_ytd_FHC(co_id=None, start_date=None, end_date=None):
    ''' Query YTD corporate financial statements (others) for financial holdings sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_financial_ytd_FHC", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_qr_FHC(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly balance sheet for financial holdings sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_qr_FHC", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_qr_FHC(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly income statement for financial holdings sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_qr_FHC", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_qr_FHC(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly cash flow statement for financial holdings sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_qr_FHC", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_finanicial_qr_FHC(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly financial statements (other) for financial holdings sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_finanicial_qr_FHC", co_id=co_id, start_date=start_date, end_date=end_date)
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

def get_balance_sheet_qr_insurance(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly balance sheet for insurance sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_qr_insurance", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_qr_insurance(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly income statement for insurance sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_qr_insurance", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_qr_insurance(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly cash flow statement for insurance sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_qr_insurance", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_finanicial_qr_insurance(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly financial statements (other) for insurance sector
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_finanicial_qr_insurance", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_ytd_security(co_id=None, start_date=None, end_date=None):
    ''' Query YTD simplified balance sheet for securities
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_ytd_security", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_ytd_security(co_id=None, start_date=None, end_date=None):
    ''' Query YTD income statement for securities
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_ytd_security", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_ytd_security(co_id=None, start_date=None, end_date=None):
    ''' Query YTD cash flow statement for securities
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_ytd_security", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_financial_ytd_security(co_id=None, start_date=None, end_date=None):
    ''' Query YTD corporate financial statements (others) for securities
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_financial_ytd_security", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_qr_security(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly balance sheet for securities
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_qr_security", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_qr_security(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly income statement for securities
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_qr_security", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_qr_security(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly cash flow statement for securities
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_qr_security", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_finanicial_qr_security(co_id=None, start_date=None, end_date=None):
    ''' Query quarterly financial statements (other) for securities
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_finanicial_qr_security", co_id=co_id, start_date=start_date, end_date=end_date)
    return _pd.read_json(ret, orient="split", dtype=False)
