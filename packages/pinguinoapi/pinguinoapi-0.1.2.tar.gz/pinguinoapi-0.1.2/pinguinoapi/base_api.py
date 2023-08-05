#!/usr/bin/env python

"""
  Author:  Yeison Cardona --<yeison.eng@gmail.com>
  Purpose:
  Created: 22/10/15
"""

import os
import requests

########################################################################
class Base:
    """"""
    FORMAT = None

    #----------------------------------------------------------------------
    def __init__(self):
        """"""
        token = os.environ.get("PINGUINOAPI_TOKEN", None)
        assert token, "Where is the token!!"
        self.headers = {'Authorization': "JWT {}".format(token)}

        self.__endpoints__ = self.endpoints()

        assert self.__endpoints__, "No endpoinds, API is running?"


    #----------------------------------------------------------------------
    def endpoints(self):
        """"""
        response = requests.get(self.HTTP_SERVICE, headers=self.headers)
        if response.ok:
            return response.json()
        else:
            return None
            # raise Exception(response.reason)


    #----------------------------------------------------------------------
    def options(self, endpoint=""):
        """"""
        response = requests.options(self.HTTP_SERVICE+endpoint, headers=self.headers)
        return response.json()


    #----------------------------------------------------------------------
    def __request__(self, call, **kwargs):
        """"""
        kwargs = self.__fix_lists__(kwargs)
        response = requests.get(self.HTTP_SERVICE+call+"/", params=kwargs, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
            # raise Exception(response.reason)


    #----------------------------------------------------------------------
    def __fix_lists__(self, kwargs):
        """"""
        data = {}
        for kw in  kwargs:
            if isinstance(kwargs[kw], (list, dict)):
                # data[kw] = ("[" + "{}," * len(kwargs[kw]) + "]").format(*kwargs[kw])
                data[kw] = str(kwargs[kw])

            # elif isinstance(kwargs[kw], dict):
                # data[kw] = str(kwargs[kw])

            else:
                data[kw] = kwargs[kw]

        return data


    #----------------------------------------------------------------------
    def __getattr__(self, attr):
        """"""
        if attr in self.__endpoints__.keys():

            def f(**kwargs):
                if self.FORMAT:
                    request = self.__request__(attr, **kwargs)
                    if isinstance(request, (str, bytes)):
                        return self.FORMAT(request)
                    else:
                        return request
                else:
                    return self.__request__(attr, **kwargs)

            return f


        else:
            raise AttributeError("Endpoint '{}' not found".format(attr))
