# coding: utf-8

from json import dumps
from numpy import nan
from pandas import Series, DataFrame, to_datetime
from requests import Session

# Globals
apilevel = '2.0'
threadsafety = 3
paramstyle = 'qmark'
_HEADER = {"Content-Type": "application/json"}
_PAYLOAD = {"queryType":"SQL", "query": None}


# Exceptions
class Warning(StandardError):
    pass

class Error(StandardError):
    pass

class DatabaseError(Error):
    def __init__(self, message, httperror):
        self.message = message
        self.httperror = httperror
    def __str__(self):
        return repr(self.message + " HTTP ERROR: %s" % self.httperror)

class ProgrammingError(DatabaseError):
    def __init__(self, message, httperror):
        self.message = message
        self.httperror = httperror
    def __str__(self):
        return repr(self.message + " HTTP ERROR: %s" % self.httperror)

class CursorClosedException(Error):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class ConnectionClosedException(Error):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

# Object types
class STRING(type):
    pass

class NUMBER(type):
    pass

class DATETIME(type):
    pass


# Helper functions
def substitute_in_query(string_query, parameters):
    query = string_query
    for param in parameters:
        if type(param) == str:
            query = query.replace("?", "'" + param + "'", 1)
        else:
            query = query.replace("?", str(param), 1)
    return query

def submit_query(query, host, db, port, session):
    local_payload_db = _PAYLOAD.copy()
    local_payload = _PAYLOAD.copy()
    local_payload_db["query"] = "USE {}".format(db)
    local_payload["query"] = query
    session.post("http://"
                 + host
                 + ":"
                 + str(port)
                 + "/query.json",
                 data = dumps(local_payload_db),
                 headers = _HEADER)
    return session.post("http://"
                        + host
                        + ":"
                        + str(port)
                        + "/query.json",
                        data = dumps(local_payload),
                        headers = _HEADER)

def parse_column_types(df):
    names = []
    types = []
    for column in df:
        try:
            df[column] = df[column].astype(int)
            types.append(NUMBER)
            names.append(column)
        except ValueError:
            try:
                df[column] = df[column].astype(float)
                types.append(NUMBER)
                names.append(column)
            except ValueError:
                try:
                    df[column] = to_datetime(df[column])
                    types.append(DATETIME)
                    names.append(column)
                except ValueError:
                    types.append(STRING)
                    names.append(column)
    return (names, types)
                

# Python DB API 2.0 classes
class Cursor(object):
    def __init__(self, host, db, port, session, conn):
        self.arraysize = 1
        self.db = db
        self.description = None
        self.host = host
        self.port = port
        self._session = session
        self._connected = True
        self.connection = conn
        self._resultSet = None
        self._resultSetStatus = None

    # Decorator for methods which require connection
    def connected(func):
        def func_wrapper(self, *args, **kwargs):
            if self._connected == False:
                raise CursorClosedException("Cursor object is closed")
            elif self.connection._connected == False:
                raise ConnectionClosedException("Connection object is closed")
            else:
                return func(self, *args, **kwargs)
        return func_wrapper

    @connected
    def close(self):
        self._connected = False

    @connected
    def execute(self, operation, parameters=()):
        result = submit_query(substitute_in_query(operation, parameters),
                              self.host,
                              self.db,
                              self.port,
                              self._session)
            
        if result.status_code != 200:
            raise ProgrammingError(result.json()["errorMessage"], result.status_code)
        else:
            self._resultSet = (DataFrame(result.json()["rows"],
                                        columns = result.json()["columns"])
                               .fillna(value=nan))
            self._resultSetStatus = iter(range(len(self._resultSet)))
            column_names, column_types = parse_column_types(self._resultSet)
            self.description = tuple(
                zip(column_names,
                    column_types,
                    [None for i in range(len(self._resultSet.dtypes.index))],
                    [None for i in range(len(self._resultSet.dtypes.index))],
                    [None for i in range(len(self._resultSet.dtypes.index))],
                    [None for i in range(len(self._resultSet.dtypes.index))],
                    [True for i in range(len(self._resultSet.dtypes.index))]
                )
            )
            return self
            
    @connected
    def fetchone(self):
        try:
            return self._resultSet.ix[self._resultSetStatus.next()]
        except StopIteration:
            return Series([])

    @connected
    def fetchmany(self, size=None):
        fetch_size = 1
        if size == None:
            fetch_size = self.arraysize
        else:
            fetch_size = size
            
        try:
            index = self._resultSetStatus.next()
            try:
                for element in range(fetch_size - 1):
                    self._resultSetStatus.next()
            except StopIteration:
                pass
            return self._resultSet[index : index + fetch_size]
        except StopIteration:
            return Series([])

    @connected
    def fetchall(self):
        try:
            remaining = self._resultSet[self._resultSetStatus.next():]
            self._resultSetStatus = iter(tuple())
            return remaining
        except StopIteration:
            return Series([])

    def __iter__(self):
        return self._resultSet.iterrows()

class Connection(object):
    def __init__(self, host, db, port, session):
        self.host = host
        self.db = db
        self.port = port
        self._session = session
        self._connected = True

    # Decorator for methods which require connection
    def connected(func):
        def func_wrapper(self, *args, **kwargs):
            if self._connected == False:
                raise ConnectionClosedException("Connection object is closed")
            else:
                return func(self, *args, **kwargs)
        return func_wrapper

    @connected
    def close(self):
        self._connected = False

    @connected
    def commit(self):
        if self._connected == False:
            print("AlreadyClosedException")
        else:
            print("Here goes some sort of commit")

    @connected
    def cursor(self):
        return Cursor(self.host, self.db, self.port, self._session, self)
        

def connect(host, db, port=8047):
    session = Session()
    local_payload = _PAYLOAD.copy()
    local_payload["query"] = "USE {}".format(db)
    response = session.post("http://" + host + ":" + str(port) + "/query.json",
                             data = dumps(local_payload),
                             headers = _HEADER)
    if response.status_code != 200:
        raise DatabaseError(str(response.json()["errorMessage"]),
                             response.status_code)
    else:
        return Connection(host, db, port, session)
