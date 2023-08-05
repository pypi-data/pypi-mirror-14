"""The data_access module contains the DataAccess class and some methods for managing transactions.
"""
import logging
from contextlib import contextmanager

from bidon.util import get_value


logger = logging.getLogger(__name__)


class DataAccess(object):
  """A thin wrapper over a DB API2 database connection.

  Provides a context manager, direct access to the execute method, and wrappers over some common
  methods to reduce the amount of boilerplate SQL required.

  This can work with several database engines, such as MySQL and SQLite, but is primarily targeted
  at Postgres, and includes functionality specific to Postgres features.
  """
  def __init__(self, core, *, search_path=None):
    """Initialize a DataAccess object with a DataAccessCore

    :core: a DataAccessCore instance
    :search_path: Postgres only. a list of schema names, which is the order in
                  which to search for unqualified objects.
    """
    self.core = core
    self.connection = None
    self.last_query = None
    self.row_count = -1
    self._search_path = search_path

  def __enter__(self):
    """Opens DataAccess and returns self as context manager."""
    return self.open()

  def __exit__(self, ex_type, ex_value, ex_traceback):
    """Closes DataAccess, requesting commit if no execption was thrown.

    :ex_type: the type of the exception
    :ex_value: the parameters passed to the exception
    :ex_traceback: the traceback object attached to the exception
    """
    self.close(commit=ex_type is None)

  def _update_cursor_stats(self, cursor):
    """Sets DataAccess members according to the given cursor.

    :cursor: a cursor object
    """
    self.row_count = cursor.rowcount

  @property
  def sql_writer(self):
    """The SQLWriter object associated with the core."""
    return self.core.sql_writer

  def commit(self):
    """Commit the pending statements."""
    logger.debug("Commit")
    self.connection.commit()

  def rollback(self):
    """Rollback the pending statements."""
    logger.debug("Rollback")
    self.connection.rollback()

  @property
  def autocommit(self):
    """Get the autocommit value."""
    return self.core.get_autocommit(self.connection)

  @autocommit.setter
  def autocommit(self, value):
    """Set the autocommit value.

    :value: the new autocommit value
    """
    logger.debug("Setting autocommit from %s to %s", self.autocommit, value)
    self.core.set_autocommit(self.connection, value)

  def _configure_connection(self, name, value):
    """Sets a Postgres run-time connection configuration parameter.

    :name: the name of the parameter
    :value: a list of values matching the placeholders
    """
    self.update("pg_settings", dict(setting=value), dict(name=name))

  def open(self, *, autocommit=False):
    """Sets the connection with the core's open method. Returns self.

    :autocommit: boolean, default autocommit state
    """
    if self.connection is not None:
      raise Exception("Connection already set")
    self.connection = self.core.open()
    if self._search_path:
      self._configure_connection(
        "search_path",
        self._search_path)
    self.autocommit = autocommit
    return self

  def close(self, *, commit=True):
    """Closes the connection via the core's close method.

    :commit: boolean, if true the current transaction is commited, otherwise it is rolled back
    """
    self.core.close(self.connection, commit=commit)
    self.connection = None
    return self

  def execute(self, query_string, params=None):
    """Executes a query. Returns the resulting cursor.

    :query_string: the parameterized query string
    :params: can be either a tuple or a dictionary, and must match the parameterization style of the
             query
    """
    cr = self.connection.cursor()
    logger.info("SQL: %s (%s)", query_string, params)
    self.last_query = (query_string, params)
    cr.execute(query_string, params or self.core.empty_params)
    self._update_cursor_stats(cr)
    return cr

  def callproc(self, name, params, param_types=None):
    """Calls a procedure.

    :name: the name of the procedure
    :params: a list or tuple of parameters to pass to the procedure.
    :param_types: a list or tuple of type names. If given, each param will be cast via sql_writers
                  typecast method. This is useful to disambiguate procedure calls when several
                  parameters are null and therefore cause overload resoluation issues.
    """

    if param_types:
      placeholders = [self.sql_writer.typecast(self.sql_writer.to_placeholder(), t)
                      for t in param_types]
    else:
      placeholders = [self.sql_writer.to_placeholder() for p in params]

    # TODO: This may be Postgres specific...
    qs = "select * from {0}({1});".format(name, ", ".join(placeholders))
    return self.execute(qs, params), params

  def get_callproc_signature(self, name, param_types):
    """Gets a procedure's signature from the name and list of types.

    :name: the name of the procedure
    :params: can be either strings, or 2-tuples. 2-tuples must be of the form (name, db_type).
    """
    if isinstance(param_types[0], (list, tuple)):
      params = [self.sql_writer.to_placeholder(*pt) for pt in param_types]
    else:
      params = [self.sql_writer.to_placeholder(None, pt) for pt in param_types]

    return name + self.sql_writer.to_tuple(params)

  def find(self, table_name, constraints=None, *, columns=None, order_by=None):
    """Find the first record that matches the given criteria.

    :table_name: the name of the table to search on
    :constraints: is any construct that can be parsed by SQLWriter.parse_constraints.
    :columns: either a string or a list of column names
    :order_by: the order by clause
    """
    query_string, params = self.sql_writer.get_find_all_query(
      table_name, constraints, columns=columns, order_by=order_by)
    query_string += " limit 1;"
    return self.execute(query_string, params).fetchone()

  def find_all(self, table_name, constraints=None, *, columns=None, order_by=None, limiting=None):
    """Find all records that match a given criteria.

    :table_name: the name of the table to search on
    :constraints: is any construct that can be parsed by SQLWriter.parse_constraints.
    :columns: either a string or a list of column names
    :order_by: the order by clause
    """
    query_string, params = self.sql_writer.get_find_all_query(
      table_name, constraints, columns=columns, order_by=order_by, limiting=limiting)
    query_string += ";"
    return self.execute(query_string, params)

  def page(self, table_name, paging, constraints=None, *, columns=None, order_by=None,
           get_count=True):
    """Performs a find_all method with paging. Returns a 2-tuple of (records, total_count)

    :table_name: the name of the table to search on
    :paging: is a tuple containing (page, page_size).
    :constraints: is any construct that can be parsed by SQLWriter.parse_constraints.
    :columns: either a string or a list of column names
    :order_by: the order by clause
    :get_count: if True, the total number of records that would be included without paging are
                returned. If False, None is returned for the count.
    """
    if get_count:
      count = self.count(table_name, constraints)
    else:
      count = None

    page, page_size = paging

    limiting = None
    if page_size > 0:
      limiting = (page_size, page * page_size)

    records = list(self.find_all(
      table_name, constraints, columns=columns, order_by=order_by, limiting=limiting))
    return (records, count)

  def update(self, table_name, values, constraints=None, *, returning=None):
    """Builds and executes and update statement.

    :table_name: the name of the table to update
    :values: can be either a dict or an enuerable of 2-tuples in the form (column, value).
    :constraints: can be any construct that can be parsed by SQLWriter.parse_constraints. However,
                  you cannot mix tuples and dicts between values and constraints.
    :returning: the columns to return after updating. Only works for cores that support the
                returning syntax
    """
    if constraints is None:
      constraints = "1=1"
    assignments, assignment_params = self.sql_writer.parse_constraints(
      values, ", ", is_assignment=True)
    where, where_params = self.sql_writer.parse_constraints(constraints, " and ")
    returns = ""
    if returning and self.core.supports_returning_syntax:
      returns = " returning {0}".format(returning)
    sql = "update {0} set {1} where {2}{3};".format(table_name, assignments, where, returns)
    params = assignment_params

    if constraints is None or isinstance(constraints, str):
      pass
    elif isinstance(constraints, dict):
      if isinstance(params, list):
        raise ValueError("you cannot mix enumerable and dict values and constraints")
      params = params or {}
      params.update(where_params)
    else:
      if isinstance(params, dict):
        raise ValueError("you cannot mix enumerable and dict values and constraints")
      params = params or []
      params.extend(where_params)

    cr = self.execute(sql, params)
    return cr

  def insert(self, table_name, values, *, returning=None):
    """Builds and executes an insert statement.

    :table_name: the name of the table to insert into
    :values: can be either a dict or an enumerable of 2-tuples in the form (column, value).
    :returning: the columns to return after updating. Only works for cores that support the
                returning syntax
    """
    if isinstance(values, dict):
      names = values.keys()
      placeholders = [self.sql_writer.to_placeholder(i) for i in names]
      params = values
    else:
      names = [i[0] for i in values]
      placeholders = [self.sql_writer.to_placeholder() for i in values]
      params = [i[1] for i in values]
    placeholders = self.sql_writer.to_tuple(placeholders)
    names = self.sql_writer.to_tuple(names)
    returns = ""
    if returning and self.core.supports_returning_syntax:
      returns = " returning {0}".format(returning)
    sql = "insert into {0} {1} values {2}{3};".format(table_name, names, placeholders, returns)
    cr = self.execute(sql, params)
    return cr

  def delete(self, table_name, constraints=None):
    """Builds and executes an delete statement.

    :table_name: the name of the table to delete from
    :constraints: can be any construct that can be parsed by SQLWriter.parse_constraints.
    """
    if constraints is None:
      constraints = "1=1"
    where, params = self.sql_writer.parse_constraints(constraints)
    sql = "delete from {0} where {1};".format(table_name, where)
    self.execute(sql, params)

  def count(self, table_name, constraints=None, *, extract="index"):
    """Get the count of records in a table.

    If the default cursor is a tuple or named tuple, this method will work without specifying an
    extract parameter. If it is a dict cursor, it is necessary to specify any value other than
    'index' for extract. This method will not work with cursors that aren't like tuple, namedtuple
    or dict cursors.

    :table_name: the name of the table to count records on
    :constraints: can be any construct that can be parsed by SQLWriter.parse_constraints.
    :extract: the property to pull the count value from the cursor
    """
    where, params = self.sql_writer.parse_constraints(constraints)
    sql = "select count(*) as count from {0} where {1};".format(table_name, where or "1 = 1")
    # NOTE: Won't work right with dict cursor
    return self.get_scalar(self.execute(sql, params), 0 if extract == "index" else "count")

  def get_scalar(self, cursor, index=0):
    """Get a single value from the first returned record from a cursor.

    By default it will get cursor.fecthone()[0] which works with tuples and namedtuples. For dict
    cursor it is necessary to specify index. This method will not work with cursors that aren't
    indexable.

    :cursor: a cursor object
    :index: the index of the cursor to return the value from
    """
    if isinstance(index, int):
      return cursor.fetchone()[index]
    else:
      return get_value(cursor.fetchone(), index)


class RollbackTransaction(Exception):
  """This Exception class is handled specially by transaction. It will cause the current transaction
  to be rolled back, but the exception won't be reraised.
  """
  pass


@contextmanager
def transaction(dax):
  """Wrap statements in a transaction. If the statements succeed, commit, otherwise rollback."""
  old_autocommit = dax.autocommit
  dax.autocommit = False
  try:
    yield dax
  except RollbackTransaction as ex:
    dax.rollback()
  except Exception as ex:
    dax.rollback()
    raise ex
  else:
    dax.commit()
  finally:
    dax.autocommit = old_autocommit


@contextmanager
def autocommit(dax):
  """Make statements autocommit."""
  if not dax.autocommit:
    dax.commit()
  old_autocommit = dax.autocommit
  dax.autocommit = True
  try:
    yield dax
  finally:
    dax.autocommit = old_autocommit
