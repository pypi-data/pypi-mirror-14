# encoding: utf-8
#
# Autogenerated by Thrift Compiler (0.9.2)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException
from ttypes import *

ERROR_BACKOFF = {
    2 : 1000,
    25 : 1000,
    37 : 0,
    32 : 0,
    1 : 1000,
    35 : 1000,
}
ERROR_RETRY_TYPE = {
    2 :   0,
    25 :   0,
    37 :   0,
    32 :   0,
    1 :   1,
    35 :   1,
}
MAX_RETRY = 1
