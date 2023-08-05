# -*- coding: utf8 -*-

import pandas as _pd
from kyper.data._utils import get_data as _get_data

_VERSION = "1.0.0"
_SERVICE = "ap_news"


def search_news(search_term=None, search_fields=['headline^2', 'body'], start_dt=None, end_dt=None, archive="latest", location=None, categories=[]):
    ''' Search news based on the relevance of the keyword(s) in news headline and content.
    '''
    ret = _get_data(_SERVICE, _VERSION, "search_news", search_term=search_term, search_fields=search_fields, start_dt=start_dt, end_dt=end_dt, archive=archive, location=location, categories=categories)
    return _pd.read_json(ret, orient="split", dtype=False)

def filter_news(start_dt=None, end_dt=None, archive="latest", location=None, categories=[]):
    ''' Query news based on the arguments
    '''
    ret = _get_data(_SERVICE, _VERSION, "filter_news", start_dt=start_dt, end_dt=end_dt, archive=archive, location=location, categories=categories)
    return _pd.read_json(ret, orient="split", dtype=False)
