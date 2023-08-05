# -*- coding: utf8 -*-

import pandas as _pd
from kyper.data._utils import get_data as _get_data

_VERSION = "1.0.0"
_SERVICE = "kyper_corpfin"


def get_income_statement_quarterly(ticker=None, start_date="1900-01-01", end_date="2100-12-12", fields=['operating revenue', 'gross operating profit', 'EBITDA', 'operating profit after depreciation', 'EBIT', 'net income (total operations)', 'total net income', 'Basic EPS from Total Operations', 'Basic EPS - Total', 'Basic EPS - Normalized', 'Diluted EPS from Total Operations', 'Diluted EPS - Total', 'Diluted EPS - Normalized', 'Dividends Paid Per Share (DPS)', 'date']):
    ''' Get quarterly income statement for ticker
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_quarterly", ticker=ticker, start_date=start_date, end_date=end_date, fields=fields)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_income_statement_yearly(ticker=None, start_date="1900-01-01", end_date="2100-12-12", fields=['operating revenue', 'gross operating profit', 'EBITDA', 'operating profit after depreciation', 'EBIT', 'net income (total operations)', 'total net income', 'Basic EPS from Total Operations', 'Basic EPS - Total', 'Basic EPS - Normalized', 'Diluted EPS from Total Operations', 'Diluted EPS - Total', 'Diluted EPS - Normalized', 'Dividends Paid Per Share (DPS)', 'date']):
    ''' Get yearly income statement for ticker, the year is representing fiscal year
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_income_statement_yearly", ticker=ticker, start_date=start_date, end_date=end_date, fields=fields)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_quarterly(ticker=None, start_date="1900-01-01", end_date="2100-12-12", fields=['total current assets', 'total fixed assets', 'total assets', 'total current liabilities', 'total non-current liabilities', 'total liabilities', 'total equity', 'total liabilities & stock equity', 'total common shares out', 'basic weighted shares', 'diluted weighted shares', 'date']):
    ''' Get quarterly balance sheet for ticker
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_quarterly", ticker=ticker, start_date=start_date, end_date=end_date, fields=fields)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_balance_sheet_yearly(ticker=None, start_date="1900-01-01", end_date="2100-12-12", fields=['total current assets', 'total fixed assets', 'total assets', 'total current liabilities', 'total non-current liabilities', 'total liabilities', 'total equity', 'total liabilities & stock equity', 'total common shares out', 'basic weighted shares', 'diluted weighted shares', 'date']):
    ''' Get yearly balance sheet for ticker, the year is representing fiscal year
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_balance_sheet_yearly", ticker=ticker, start_date=start_date, end_date=end_date, fields=fields)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_quarterly(ticker=None, start_date="1900-01-01", end_date="2100-12-12", fields=['net cash from total operating activities', 'net cash from investing activities', 'net cash from financing activities', 'net change in cash & equivalents', 'date']):
    ''' Get quarterly cash flow for the ticker
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_quarterly", ticker=ticker, start_date=start_date, end_date=end_date, fields=fields)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_cash_flow_yearly(ticker=None, start_date="1900-01-01", end_date="2100-12-12", fields=['net cash from total operating activities', 'net cash from investing activities', 'net cash from financing activities', 'net change in cash & equivalents', 'date']):
    ''' Get yearly cash flow for ticker, the year is representing fiscal year
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_cash_flow_yearly", ticker=ticker, start_date=start_date, end_date=end_date, fields=fields)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_financial_ratios_quarterly(ticker=None, start_date="1900-01-01", end_date="2100-12-12", fields=[]):
    ''' Get quarterly financial ratios for the ticker
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_financial_ratios_quarterly", ticker=ticker, start_date=start_date, end_date=end_date, fields=fields)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_financial_ratios_yearly(ticker=None, start_date="1900-01-01", end_date="2100-12-12", fields=[]):
    ''' Get yearly financial ratios for the ticker, the year is representing fiscal year
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_financial_ratios_yearly", ticker=ticker, start_date=start_date, end_date=end_date, fields=fields)
    return _pd.read_json(ret, orient="split", dtype=False)

def search_symbols(search_term=None):
    ''' Search company symbol
    '''
    ret = _get_data(_SERVICE, _VERSION, "search_symbols", search_term=search_term)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_available_quarterly_report(ticker=None):
    ''' List of available quarter (enddate of the quarter) for quarterly reports for the ticker
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_available_quarterly_report", ticker=ticker)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_available_yearly_report(ticker=None):
    ''' List of available years for yearly reports for the ticker
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_available_yearly_report", ticker=ticker)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_indicators_fields():
    ''' List of fields in indicators
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_indicators_fields")
    return _pd.read_json(ret, orient="split", dtype=False)

def list_income_statements_fields():
    ''' List of fields in income statements
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_income_statements_fields")
    return _pd.read_json(ret, orient="split", dtype=False)

def list_balance_sheets_fields():
    ''' List of fields in balance sheets
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_balance_sheets_fields")
    return _pd.read_json(ret, orient="split", dtype=False)

def list_cash_flow_statements_fields():
    ''' List of fields in cash flow
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_cash_flow_statements_fields")
    return _pd.read_json(ret, orient="split", dtype=False)

def list_financial_ratios_fields():
    ''' List all the fields in financial ratios
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_financial_ratios_fields")
    return _pd.read_json(ret, orient="split", dtype=False)
