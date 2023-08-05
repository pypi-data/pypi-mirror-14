#!/usr/bin/python3

"""
  Author:  Yeison Cardona --<yeison.eng@gmail.com>
  Purpose:
  Created: 26/10/15
"""

from pinguinoapi import Pinguino, setup_pinguinoapi

# TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0NDg5ODc3ODksInVzZXJfaWQiOjEsImVtYWlsIjoieWVpc29uZW5nQGdtYWlsLmNvbSIsInVzZXJuYW1lIjoieWVpc29uIn0.oxCC8GcsnnJwnlOyyK0gG9X4YjsJ6wuKCdt0Ufy7UX8"
#TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InllaXNvbiIsImVtYWlsIjoieWVpc29uZW5nQGdtYWlsLmNvbSIsImV4cCI6MTQ0OTAyMTQ1NywidXNlcl9pZCI6MX0.JY-vJf5N7ckYQxyun1MsdH8MzoW9eQ1xP1YTs6_W2h4"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBpbmd1aW5vIiwidXNlcl9pZCI6MSwiZW1haWwiOiJ5ZWlzb25lbmdAZ21haWwuY29tIiwiZXhwIjoxNDU2NjgzMTk5fQ.b7SFLW43AJ1Cg5eV7SKpjYXJF5gUEuxsSzLJnWpHx7M"
setup_pinguinoapi(TOKEN)


api = Pinguino()

code = "setup(){} loop(){}"

compile_ = api.compile(board="PINGUINO2550", code=code, compiler="sdcc")

print(compile_)







pass