# -*- coding: utf8 -*-

import pandas as _pd
from kyper.data._utils import get_data as _get_data

_VERSION = "1.0.0"
_SERVICE = "kyper_factormodels"


def list_factors(date=None):
    ''' Lists the factors for which you can extract the covariance matrix
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_factors", date=date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_covariance_matrix(date=None, factors=None):
    ''' Covariance matrix for the factors (both fundamental and statistical).
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_covariance_matrix", date=date, factors=factors)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_factor_loadings(date=None):
    ''' Lists the factor loadings i.e. the factors for which the beta forecasts can be extracted.
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_factor_loadings", date=date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_factor_loadings(date=None, symbols=None, factors=None):
    ''' Values of the factor loadings used to evaluate the model for the given day.
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_factor_loadings", date=date, symbols=symbols, factors=factors)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_factors_with_returns(date=None):
    ''' Lists the factors for which returns are available to be extracted.
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_factors_with_returns", date=date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_factor_returns(date=None, start_date=None, end_date=None, factors=None):
    ''' Values of the factor returns used to evaluate the model for the given day.
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_factor_returns", date=date, start_date=start_date, end_date=end_date, factors=factors)
    return _pd.read_json(ret, orient="split", dtype=False)

def list_available_symbols(date=None):
    ''' Lists the ticker symbols for which we can extract the Industry classification used while evaluating the model.
    '''
    ret = _get_data(_SERVICE, _VERSION, "list_available_symbols", date=date)
    return _pd.read_json(ret, orient="split", dtype=False)

def get_industry_membership(date=None, symbols=None):
    ''' Industry membership details for the equities used to evaluate the model for the given day.
    '''
    ret = _get_data(_SERVICE, _VERSION, "get_industry_membership", date=date, symbols=symbols)
    return _pd.read_json(ret, orient="split", dtype=False)
