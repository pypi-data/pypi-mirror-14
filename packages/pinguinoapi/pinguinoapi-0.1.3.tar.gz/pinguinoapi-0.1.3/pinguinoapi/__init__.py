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


HOST = "api.pinguino.xyz"
#HOST = "localhost:8000"


########################################################################
class PinguinoAPI(Base):
    """"""
    #HTTP_SERVICE = "http://api.pinguino.xyz/api/"
    HTTP_SERVICE = "http://{}/api/".format(HOST)
    # FORMAT = ast.literal_eval



    #----------------------------------------------------------------------
    def register(self, **kwargs):
        """"""
        URL = "http://{}/user/".format(HOST)
        CALL = "register"
        METHOD = "post"

        return self.__custom_request__(URL, CALL, METHOD, **kwargs)


    #----------------------------------------------------------------------
    def get_token(self, **kwargs):
        """"""
        URL = "http://{}/".format(HOST)
        CALL = "api-token-auth"
        METHOD = "post"

        return self.__custom_request__(URL, CALL, METHOD, **kwargs)
