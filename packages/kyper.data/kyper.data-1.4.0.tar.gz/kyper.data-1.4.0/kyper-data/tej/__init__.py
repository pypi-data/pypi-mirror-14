#!/usr/bin/env python
# -*- coding: utf8 -*-

import pandas as _pd
from kyper.data._utils import get_data as _get_data
 
VERSION = "0"
SERVICE = "tej"

def tables():
    ret = _get_data(SERVICE, VERSION, "tables")
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret

def fields(table):
    ret = _get_data(SERVICE, VERSION, "fields", table=table)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_mar_code(text=None ,mar_name= ""):
    ret = _get_data(SERVICE, VERSION, "mar", text = text, mar_name = mar_name)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret

def get_ticker(text=None ,location=""):
    ret = _get_data(SERVICE, VERSION, "ticker", text = text, location = location)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret

def get_future(text=None):
    ret = _get_data(SERVICE, VERSION, "future", text = text)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret

def get_bond(text=None):
    ret = _get_data(SERVICE, VERSION, "bond", text = text)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret

def get_fund(text=None):
    ret = _get_data(SERVICE, VERSION, "fund", text = text)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret

def get(table, co_id, fields="VAL", start_time = None, end_time = None):
    ret = _get_data(SERVICE, VERSION, "get", table = table, co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret

def get_tw_macroeconomics( co_id, fields=None, start_time=None, end_time=None):
    """ get taiwan macroeconomics

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get", table = "wnmar", co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_company_attribute(co_id, fields=None, start_time=None, end_time=None):
    """ get taiwan company attribute

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table ="wind", co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_directors_holding(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan directors holding

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wbstn" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_holding_transfer(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan holding transfer

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wtrans" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_lt_investment_detail(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Long-Term Investment Detail

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "winv" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_investment_transfer(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Investment Transfer

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wtinvc" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_investment_china_company(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Investment in China (Company)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wcinv1" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_monthly_sales(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Monthly Sales

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wsale" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_dividends_policy(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Dividends Policy

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wmt1" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_ipo(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan IPO

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wipo", co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_corporate_action(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Corporate Action

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wstk1" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_cash_dividend(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Cash Dividend

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wdiv" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_central_deposit(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Central Deposit

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wtscd" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_deposit_statistics(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Deposit Statistics

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wdcshr" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_sales_break_down_yearly(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Sales Break Down(Yearly)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wmix" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_equity_view(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Equity View

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wshr1" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_adjusted_price(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Adjusted Price

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "waprcd1" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_suspended_records(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Suspended Records

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wsusp" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_warrant_attribute(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Warrant Attribute

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "warbas" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_warrant_trading(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Warrant Trading

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "warnt" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_future_attribute(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Future Attribute

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wfutrstd" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_future_db(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Future DB

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wfutr" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_option_attribute(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Option Attribute

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wopbas" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_option(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Option

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "woption", co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_fund_attribute(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Fund's Attribute

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "watt" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_fund_invest_portfolio(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Fund's Invest Portfolio

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wftinv" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_fund_nav(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Fund's NAV

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wnav" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_bound_attribute(co_id, fields = None, start_time=None, end_time=None):
    """ get Bound's Attribute

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wgbd" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_bounds_trading_price(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Bounds Trading Price

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wgbd6" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_gredei_government_bounds_system(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan Gredei Government Bounds System

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wgbd7" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_consolidated_first_acc_all(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan IFRS_TEJ Consolidated First(Acc)-ALL

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wim1a" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_consolidated_first_qly_all(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan IFRS_TEJ Consolidated First(Qly)-ALL

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wim1aq" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_consolidated_first_financial_general(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan IFRS_TEJ Consolidated First Financial_General

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
        :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wim4" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_consolidated_first_financial_banking(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan IFRS_TEJ Consolidated First Financial_Banking

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wimh4" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_consolidated_first_financial_fhc_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan IFRS_TEJ Consolidated First Financial_FHC(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wihm4" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_consolidated_first_financial_insurrance_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan IFRS_TEJ Consolidated First Financial_Insurance(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wimb4" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_consolidated_first_financial_security_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan IFRS_TEJ Consolidated First Financial_Security(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wims4" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_consolidated_first_financial_general_qly(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan IFRS_TEJ Consolidated First Financial_General(Qly)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wimq4" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_consolidated_first_financial_banking_qly(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan IFRS_TEJ Consolidated First Financial_Banking(Qly)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wimhq4" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_consolidated_first_financial_fhc_qly(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan IFRS_TEJ Consolidated First Financial_FHC(Qly)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wihmq4" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_consolidated_first_financial_insurrance(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan IFRS_TEJ Consolidated First Financial_Insurance

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wimbq4" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_tw_consolidated_first_financial_security(co_id, fields = None, start_time=None, end_time=None):
    """ get taiwan IFRS_TEJ Consolidated First Financial_Security

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "wimsq4" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_cn_macroeconomics(co_id, fields = None, start_time=None, end_time=None):
    """ get china Macroeconomicse

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "cmar" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_cn_company_attribute(co_id, fields = None, start_time=None, end_time=None):
    """ get china Company Attribute

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "cbas" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_cn_shareholder_meeting(co_id, fields = None, start_time=None, end_time=None):
    """ get china Shareholder Meeting

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "cmt" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_cn_ipo(co_id, fields = None, start_time=None, end_time=None):
    """ get china IPO

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "cipo" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_cn_corporate_action(co_id, fields = None, start_time=None, end_time=None):
    """ get china China Corporate Action

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "ccap" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_cn_cash_dividend(co_id, fields = None, start_time=None, end_time=None):
    """ get china Cash Dividend

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "cdiv" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_cn_director_holding(co_id, fields = None, start_time=None, end_time=None):
    """ get china Director Holding

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "cdirtop" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_cn_consolidates_subsidiary(co_id, fields = None, start_time=None,end_time=None):
    """ get china Consolidates subsidiary

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "ccon" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_cn_sales_breakdown_annual_product(co_id, fields = None, start_time=None,end_time=None):
    """ get china Sales Breakdown(Annual)-Product

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "cmix" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_cn_adjusted_stock_price(co_id, fields = None, start_time=None, end_time=None):
    """ get china Adjusted Stock Price

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "caprcd1" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_cn_margin_trading(co_id, fields = None, start_time=None, end_time=None):
    """ get china Margin Trading

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "cgin" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_cn_financial_acc_all(co_id, fields = None, start_time=None, end_time=None):
    """ get china Financial(Acc)-ALL

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "cnm1" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_cn_financial_qly_all(co_id, fields = None, start_time=None, end_time=None):
    """ get china Financial(Qly)-ALL

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "cnmq1" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_cn_new_financial_general_acc(co_id, fields = None, start_time=None,end_time=None):
    """ get china New Financial General(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "cmf3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_cn_new_financial_banking_acc(co_id, fields = None, start_time=None,end_time=None):
    """ get TEJ_China New Financial_Banking(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "cmh3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_cn_new_financial_insurance_acc(co_id, fields = None, start_time=None,end_time=None):
    """ get TEJ_China New Financial_Insurance(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "cmk3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_cn_new_financial_security_acc(co_id, fields = None, start_time=None,end_time=None):
    """ get TEJ_China New Financial_Security(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "cms3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_cn_new_financial_general_qly(co_id, fields = None, start_time=None, end_time=None):
    """ get TEJ_China New Financial_General(Qly)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "cmfq3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_cn_new_financial_banking_acc(co_id, fields = None, start_time=None,end_time=None):
    """ get TEJ_China New Financial_Banking(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "cmhq3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_cn_new_financial_insurance_qly(co_id, fields = None, start_time=None, end_time=None):
    """ get TEJ_China New Financial_Insurance(Qly)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "cmkq3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_cn_new_financial_security_qly(co_id, fields = None, start_time=None,
        end_time=None):
    """ get TEJ_China New Financial_Security(Qly)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "CMSQ3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_hk_macroeconomics(co_id, fields = None, start_time=None, end_time=None):
    """ get hongkong Macroeconomics

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "hkmar" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_hk_company_attribute(co_id, fields = None, start_time=None, end_time=None):
    """ get hongkong Company Attribute

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "hind" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_hk_consolidated_entities(co_id, fields = None, start_time=None, end_time=None):
    """ get hongkong Consolidated Entities

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "hinv" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_hk_corporate_action(co_id, fields = None, start_time=None, end_time=None):
    """ get hongkong Corporate Action

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "hstk1" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_hk_cash_dividend(co_id, fields = None, start_time=None, end_time=None):
    """ get hongkong Cash Dividend

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "hdiv" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_hk_shareholder_meeting(co_id, fields = None, start_time=None, end_time=None):
    """ get hongkong Shareholder Meeting

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "hmt" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_hk_ipo(co_id, fields = None, start_time=None, end_time=None):
    """ get hongkong IPO

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "hipo" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_hk_sales_breakdown_yearly_product(co_id, fields = None, start_time=None, end_time=None):
    """ get hongkong Sales Breakdown(Yearly)-Product

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "hmix" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_hk_substantial_share_holding(co_id, fields = None, start_time=None, end_time=None):
    """ get hongkong Substantial Share Holding

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "hbst" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_hk_company_suspended_records(co_id, fields = None, start_time=None, end_time=None):
    """ get hongkong Company Suspended Records

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "hsusp" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_hk_margin_trading(co_id, fields = None, start_time=None, end_time=None):
    """ get hongkong Margin Trading

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "hgin" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_hk_new_consolidated_financial_acc_all(co_id, fields = None, start_time=None, end_time=None):
    """ get hongkong New Consolidated Financial(Acc)-ALL

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "hnm1" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_hk_new_consolidated_financial_qly_all(co_id, fields = None, start_time=None, end_time=None):
    """ get hongkong New Consolidated Financial(Qly)-ALL

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "hnmq1" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_hk_new_company_financial_acc_all_hkd(co_id, fields = None, start_time=None, end_time=None):
    """ get hongkong New Consolidated Financial(Acc)-ALL_HKD

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "hnm1o" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_hk_new_consolidated_financial_qly_all_hkd(co_id, fields = None, start_time=None, end_time=None):
    """ get hongkong New Consolidated Financial(Qly)-ALL_HKD

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "hnmq1o" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_hk_new_consolidated_financial_general_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get hongkong New Consolidated Financial_General(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "hknf3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_hk_new_consolidated_financial_banking_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get hongkong New Consolidated Financial_Banking(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "hknh3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_hk_new_consolidated_financial_insurance_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get hongkong New Consolidated Financial_Insurance(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "hknb3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_hk_new_consolidated_financial_investment_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get hongkong New Consolidated Financial_Investment(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "hknv3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_hk_new_consolidated_financial_general_acc_hkd(co_id, fields = None, start_time=None, end_time=None):
    """ get hongkong New Consolidated Financial_General(Acc)_HKD

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "hknf3o" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_hk_new_consolidated_financial_banking_acc_hkd(co_id, fields = None, start_time=None, end_time=None):
    """ get hongkong New Consolidated Financial_Banking(Acc)_HKD

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "hknh3o" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_hk_new_consolidated_financial_insurance_acc_hkd(co_id, fields = None, start_time=None, end_time=None):
    """ get hongkong New Consolidated Financial_Insurance(Acc)_HKD

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "hknb3o" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_hk_new_consolidated_financial_investment_acc_hkd(co_id, fields = None, start_time=None, end_time=None):
    """ get hongkong New Consolidated Financial_Investment(Acc)_HKD

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "hknv3o" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_sg_macroeconomics(co_id, fields = None, start_time=None, end_time=None):
    """ get singapore Macroeconomics

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "smar" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_sg_company_attribute(co_id, fields = None, start_time=None, end_time=None):
    """ get singapore Company Attribute

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "sind" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_sg_largest_shareholders(co_id, fields = None, start_time=None, end_time=None):
    """ get singapore 20 Largest Shareholders

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "sbst" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_sg_sales_breakdown_yearly_product(co_id, fields = None, start_time=None, end_time=None):
    """ get singapore Breackdown(Yearly)-Product

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "smix" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_sg_company_holding_detail(co_id, fields = None, start_time=None, end_time=None):
    """ get singapore Company Holding Detail

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "sinv" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_sg_corporate_action(co_id, fields = None, start_time=None, end_time=None):
    """ get singapore Corporate Action

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "sstk1" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_sg_cash_dividend(co_id, fields = None, start_time=None, end_time=None):
    """ get singapore Cash Dividend

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "sdiv" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_sg_shareholder_meeting(co_id, fields = None, start_time=None, end_time=None):
    """ get singapore Shareholder Meeting

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "smt" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_sg_ipo(co_id, fields = None, start_time=None, end_time=None):
    """ get singapore ipo

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "sipo" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_sg_new_consolidated_financial_general_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get singapore new Consolidated Financial_General(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "snmf1" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_sg_consolidated_financial_banking_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get singapore Consolidated Financial_Banking(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "smh3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_sg_consolidated_financial_life_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get singapore Consolidated Financial_Life Ins.(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "smb3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_sg_consolidated_financial_finance_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get singapore Consolidated Financial_Finance(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "smi3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_sg_consolidated_financial_investment_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get singapore Consolidated Financial_Investment(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "smv3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_my_macroeconomics(co_id, fields = None, start_time=None, end_time=None):
    """ get malaysia Macroeconomics

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "mmar" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_my_company_attribute(co_id, fields = None, start_time=None, end_time=None):
    """ get malaysia Company Attribute

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "mind" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_my_substantial_share_holding(co_id, fields = None, start_time=None, end_time=None):
    """ get malaysia Substantial share Holding

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "mbst" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_my_corporate_action(co_id, fields = None, start_time=None, end_time=None):
    """ get malaysia Corporate Action

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "mstk1" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_my_cash_dividend(co_id, fields = None, start_time=None, end_time=None):
    """ get malaysia Cash Dividend

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "mdiv" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_my_sales_breakdown(co_id, fields = None, start_time=None, end_time=None):
    """ get malaysia Sales Breakdown

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "mmix" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_my_new_financial_general_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get malaysia New Financial General(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "mif4" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_my_new_financial_banking_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get malaysia New Financial Banking(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "mib4" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_my_new_financial_insurance_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get malaysia New Financial Insurance(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "mih4" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_th_macroeconomics(co_id, fields = None, start_time=None, end_time=None):
    """ get thailand Macroeconomics

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "tmar" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_th_company_attribute(co_id, fields = None, start_time=None, end_time=None):
    """ get thailand Company Attribute

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "tind" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_th_corporate_action(co_id, fields = None, start_time=None, end_time=None):
    """ get thailand Corporate Action

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "tskt1" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_th_cash_dividend(co_id, fields = None, start_time=None, end_time=None):
    """ get thailand Cash Dividend

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "tdiv" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_th_substantial_share_holding(co_id, fields = None, start_time=None, end_time=None):
    """ get thailand Substantial Share Holding

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "tbst" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_th_consolidated_financial_general_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get THAI Consolidated Financial_General(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "tmf4" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_th_consolidated_financial_banking_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get THAI Consolidated Financial_Banking(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "tmh4" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_th_consolidated_financial_property_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get THAI Consolidated Financial_Property(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "tmk4" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_th_consolidated_financial_broker_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get THAI Consolidated Financial_Broker(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "tms4" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_th_consolidated_financial_investment_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get THAI Consolidated Financial_Investment(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "tmv4" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_jp_company_attribute(co_id, fields = None, start_time=None, end_time=None):
    """ get japan Company Attribute

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "jind" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_jp_corporate_action(co_id, fields = None, start_time=None, end_time=None):
    """ get japan Corporate Action

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "jstk1" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_jp_cash_dividend(co_id, fields = None, start_time=None, end_time=None):
    """ get japan Cash Dividend

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "jdiv" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_jp_sales_breakdown_product(co_id, fields = None, start_time=None, end_time=None):
    """ get japan Sales Breakdown Product

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "jmix1" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_jp_director_manager_holding(co_id, fields = None, start_time=None, end_time=None):
    """ get japan Director & Manager Holding

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "jbstn" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_jp_financial_general_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get japan Financial General(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "jnf3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_jp_financial_banking_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get japan Financial Banking(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "jnh3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_jp_financial_security_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get japan Financial Security(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "jns3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_jp_financial_property_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get japan Financial Property(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "jnk3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_jp_financial_all(co_id, fields = None, start_time=None, end_time=None):
    """ get japan Financial(All)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "jmf1" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_kr_macroeconomics(co_id, fields = None, start_time=None, end_time=None):
    """ get korea Macroeconomics

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "kmar" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_kr_company_attribute(co_id, fields = None, start_time=None, end_time=None):
    """ get korea Company Attribute

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "kind" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_kr_corporate_action(co_id, fields = None, start_time=None, end_time=None):
    """ get korea Corporate Action

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "kstk1" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_kr_cash_dividend(co_id, fields = None, start_time=None, end_time=None):
    """ get korea Cash Dividend

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "kdiv" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_kr_substantial_share_holding(co_id, fields = None, start_time=None, end_time=None):
    """ get korea Substantial Share Holding

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "kmix" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_kr_sales_breakdown(co_id, fields = None, start_time=None, end_time=None):
    """ get korea Sales Breakdown

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "kbst" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_kr_financial_general_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get korea Financial General(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "kf3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_kr_financial_banking_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get korea Financial Banking(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "kh3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_kr_financial_property(co_id, fields = None, start_time=None, end_time=None):
    """ get korea Financial Property(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "kk3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_kr_financial_broker_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get korea Financial Broker(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "ks3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_kr_consolidated_financial_general_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get KOREA Consolidated Financial_General(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "kmf3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_kr_consolidated_financial_banking_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get KOREA Consolidated Financial_Banking(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "kmh3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_kr_consolidated_financial_property_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get KOREA Consolidated Financial_Property(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "kmk3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_kr_consolidated_financial_broker_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get KOREA Consolidated Financial_Broker(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "kms3" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_ph_macroeconomics(co_id, fields = None, start_time=None, end_time=None):
    """ get philippine Macroeconomics

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "fmas" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_ph_company_attribute(co_id, fields = None, start_time=None, end_time=None):
    """ get philippine Company Attribute

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "find" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_ph_corporate_action(co_id, fields = None, start_time=None, end_time=None):
    """ get philippine Corporate Action

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "fstk1" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_ph_cash_dividend(co_id, fields = None, start_time=None, end_time=None):
    """ get philippine Cash Dividend

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "fdiv" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_ph_substantial_share_holding(co_id, fields = None, start_time=None, end_time=None):
    """ get philippine Substantial Share Holding

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "fbst" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_ph_sales_breakdown_product(co_id, fields = None, start_time=None, end_time=None):
    """ get philippine Sales Breakdown Product

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "fmix" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_ph_new_financial_general_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get philippine New Financial General(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "fimf4" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_ph_consolidated_financial_finance_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get philippine Consolidated Financial_Finance(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "fmh4" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret


def get_ph_consolidated_financial_acc(co_id, fields = None, start_time=None, end_time=None):
    """ get philippine Consolidated Financial_Ins.(Acc)

    :param co_id str: cooperation id
    :param fields str: country
    :param start_time ["str"]: start date
    :param end_time ["str"]: end date

    :ret pandas.DataFrame

    """
    ret = _get_data(SERVICE, VERSION, "get",table = "fmb4" , co_id = co_id, fields = fields, start_time = start_time, end_time = end_time)
    try:
        return _pd.read_json(ret, orient="split")
    except:
        return ret



# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4


