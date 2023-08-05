#!/usr/bin/env python

from wintx.errors import WintxDriverError
from mysql.connector import errorcode, Error as MySQLClientError

class MySQLError(WintxDriverError):

  def __init__(self, mysql_error):
    """MySQLError class constructor
    Inputs:
      mysql_error: mysql.connector.Error instance
    """
    self.original = mysql_error

  def __str__(self):
    return self.original.msg
