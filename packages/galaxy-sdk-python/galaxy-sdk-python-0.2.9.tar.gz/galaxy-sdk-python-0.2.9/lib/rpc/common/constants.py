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

DEFAULT_CLIENT_TIMEOUT = 10000
DEFAULT_MAX_CLIENT_TIMEOUT = 10000
DEFAULT_ADMIN_CLIENT_TIMEOUT = 30000
DEFAULT_CLIENT_CONN_TIMEOUT = 3000
API_ROOT_PATH = "/v1/api"
AUTH_SERVICE_PATH = "/v1/api/auth"
ADMIN_SERVICE_PATH = "/v1/api/admin"
DEFAULT_THRIFT_HEADER = "application/x-thrift"
THRIFT_JSON_HEADER = "application/x-thrift-json"
THRIFT_COMPACT_HEADER = "application/x-thrift-compact"
THRIFT_BINARY_HEADER = "application/x-thrift-binary"
THRIFT_HEADER_MAP = {
    0 : "application/x-thrift-compact",
    1 : "application/x-thrift-json",
    2 : "application/x-thrift-binary",
}
HEADER_THRIFT_MAP = {
  "application/x-thrift-compact" :   0,
  "application/x-thrift-json" :   1,
  "application/x-thrift-binary" :   2,
  "application/x-thrift" :   1,
}
HK_REQUEST_TIMEOUT = "X-Xiaomi-Request-Timeout"
HK_ERROR_CODE_HEADER = "X-Xiaomi-Error-Code"
MAX_CONTENT_SIZE = 524288
