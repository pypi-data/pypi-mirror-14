#!/usr/bin/env python

"""
  Author:  Yeison Cardona --<yeison.eng@gmail.com>
  Purpose:
  Created: 22/10/15
"""

import requests
from .base_api import Base
import ast

import os

#----------------------------------------------------------------------
def setup_pinguinoapi(token):
    """"""
    os.environ["PINGUINOAPI_TOKEN"] = token



########################################################################
class Pinguino(Base):
    """"""
    HTTP_SERVICE = "http://api.pinguino.xyz/api/"
    # HTTP_SERVICE = "http://localhost:8000/api/"
    # FORMAT = ast.literal_eval

