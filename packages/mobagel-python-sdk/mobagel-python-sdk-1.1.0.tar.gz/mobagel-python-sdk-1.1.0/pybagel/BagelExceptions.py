import sys
class Error(Exception):
   """Base class for exceptions in this module."""
   pass

class HttpsResponseException(Error):

   def __init__(self, message, resp, content):
       self.message = message
       self.resp = resp
       self.content = content
