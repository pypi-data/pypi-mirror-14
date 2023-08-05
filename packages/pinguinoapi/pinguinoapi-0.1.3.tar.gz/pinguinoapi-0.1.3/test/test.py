#!/usr/bin/python3

"""
  Author:  Yeison Cardona --<yeison.eng@gmail.com>
  Purpose:
  Created: 26/10/15
"""

from pinguinoapi import PinguinoAPI


#Register on API
api = PinguinoAPI()
response = api.register(username="user", email="user@email.com", password="userpassword")
print(response)


#Get new TOKEN
api = PinguinoAPI()
response = api.get_token(username="user", password="userpassword")
print(response)


#Compile code
TOKEN = response["token"]
api = PinguinoAPI(TOKEN)
code = "setup(){} loop(){}"
compile_ = api.compile(board="PINGUINO2550", code=code, compiler="sdcc")
print(compile_)



