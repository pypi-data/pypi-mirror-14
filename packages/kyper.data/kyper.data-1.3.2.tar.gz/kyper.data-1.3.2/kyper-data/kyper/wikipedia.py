# -*- coding: utf8 -*-

import pandas as _pd
from kyper.data._utils import get_data as _get_data

_VERSION = "1.0.0"
_SERVICE = "kyper_wikipedia"


def find(search_term=None, start_dt=None, end_dt=None, lang=None, freq="h"):
    ''' Search count statistics of certain page on wikipeida.
    '''
    ret = _get_data(_SERVICE, _VERSION, "find", search_term=search_term, start_dt=start_dt, end_dt=end_dt, lang=lang, freq=freq)
    return _pd.read_json(ret, orient="split", dtype=False)

def lang():
    ''' Return dataframe with language keywords to be used for "lang" input variable in wikipedia.find() function.
    '''
    ret = _get_data(_SERVICE, _VERSION, "lang")
    return _pd.read_json(ret, orient="split", dtype=False)
