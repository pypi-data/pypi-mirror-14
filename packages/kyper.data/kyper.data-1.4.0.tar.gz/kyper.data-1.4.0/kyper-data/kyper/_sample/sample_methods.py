# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json

import pandas as pd

from kyper.data._utils import get_data as _get_data

VERSION = "0"
SERVICE = "sampleservice"

def sample_method(**kwargs):
   return json.loads(_get_data(SERVICE, VERSION, "sample_method", **kwargs))

def sample_error(**kwargs):
   return _get_data(SERVICE, VERSION, "sample_error", **kwargs)

def sample_df(num_cols):
   response = _get_data(SERVICE, VERSION, "sample_df", num_cols=num_cols)
   return pd.read_json(response)