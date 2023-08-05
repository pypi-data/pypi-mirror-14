DrillPy

drillpy is a Python wrapper for Apache Drill's REST API, which lets you query and import data to Python directly from a working Drill cluster/drillbit instance. It is built on top on requests, numpy and pandas.


Installation

pip install drillpy


Usage

drillpy follows the Python Database API Specification v2.0, so it's usage is pretty similar to the one you can find e.g. in the builtin sqlite3 module from CPython's Standard Library.


As with sqlite3, you should start by creating a Connection object, using drillpy.connect():

from drillpy import connect
con = connect(host="some_drillbit_host", db="some_database_managed_by_drill", port=8047)


Once created, you must create a Cursor:

cur = con.cursor()

Now you can use this cursor to write SQL queries against your Drill cluster. Parameter substitution is handled by question marks ? (as in sqlite3):

query = cur.execute("SELECT * FROM mytable WHERE somecolumn > ? AND someothercolumn < ? LIMIT 10", (value, other_value))


Results are returned in a pandas DataFrame, with NaNs in missing values. Column types are inferred automatically. You can retreive results with fetchone(), fetchmany(size) and fetchall(). With fetchone(), a pandas Series is returned rather than a DataFrame:

returned_df = query.fetchall()



Keep in mind that drillpy cannot insert new data in your tables/databases, since Drill itself is a querying engine meant to be used for exploratory data analysis and BI/visualization tools.

Once finished, you should call Connection.close():

con.close()



