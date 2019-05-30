from __future__ import absolute_import

RET = {
    "OK":0,
    "ERR_COMMON":1,
    "ERR_UNKNOWN":2,

    "ERR_SOCKET_CREATE":11,
    "ERR_SOCKET_OPERAT":12,
    "ERR_SOCKET_BIND":13,
    "ERR_SOCKET_LISTEN":14,

    "ERR_FILE_OPEN":21,
    "ERR_FILE_READ":22,
    "ERR_FILE_WRITE":23,

    "ERR_DB_CONNECTION":31,
    "ERR_DB_OPEN":32,
    "ERR_DB_QUERY":33,
}

class BaseError(RuntimeError):
    errno = None
    message = None
    description = None

    def __str__(self):
        FMT = "[ERROR{}]{}:{}"
        if not self.args:
            return FMT.format(
                self.errno,
                self.__class__.__name__,
                self.message
            )
        else:
            return FMT.format(
                self.errno,
                self.__class__.__name__,
                super(BaseError, self).__str__()
            )

class NoError(BaseError):
    errno = RET["OK"]
    message = "no error"
    description = "no error, it run normally"

class CommonError(BaseError):
    errno = RET["ERR_COMMON"]
    message = "common error"
    description = "a common error"

class UnknownError(BaseError):
    errno = RET["ERR_UNKNOWN"]
    message = "unknown error"
    description = "an unexpected error"

class SocketError(BaseError):
    def __str__(self):
        return "{}".format(super(DBError, self).__str__())

class SocketCreateException(SocketError):
    errno = RET["ERR_SOCKET_CREATE"]
    message = "socket create error"
    description = "this exception happen when socket can't create"

class SocketOperatException(SocketError):
    errno = RET["ERR_SOCKET_OPERAT"]
    message = "socket operation error"
    description = "this exception happen when operation socket error"

class SocketBindException(SocketError):
    errno = RET["ERR_SOCKET_BIND"]
    message = "socket bind error"
    description = "this exception happen when socket can't bind on a address and port"

class SocketListenException(SocketError):
    errno = RET["ERR_SOCKET_LISTEN"]
    message = "socket listen error"
    description = "this exception happen when socket can't listen on a address and port"

class DBError(BaseError):
    def __str__(self):
        return "{}".format(super(DBError, self).__str__())

class DBConnectionException(DBError):
    errno = RET["ERR_DB_CONNECTION"]
    message = "database connection error"
    description = "database connection error"

class DBOpenException(DBError):
    errno = RET["ERR_DB_OPEN"]
    message = "database open error"
    description = "database open error"

class DBQueryException(DBError):
    errno = RET["ERR_DB_QUERY"]
    message = "database query error"
    description = "database do sql query error"

class DataLoadError(BaseError):
    def __str__(self):
        return "{}".format(super(DataLoadError, self).__str__())

class TrackerParseException(DataLoadError):
    errno = RET["ERR_TRACKER_PARSE"]
    message = "tracker data parse error"
    description = "tracker data parse error"

class TravelParseException(DataLoadError):
    errno = RET["ERR_TRAVEL_PARSE"]
    message = "travel data parse error"
    description = "travel data parse error"

def error_test():
    try:
        raise UnknownError("Not Good")
    except Exception as e:
        print(e)
        return e.errno
    else:
        return NoError.errno
