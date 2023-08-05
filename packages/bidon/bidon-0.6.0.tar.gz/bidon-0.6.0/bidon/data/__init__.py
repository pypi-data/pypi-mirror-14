"""The data package contains classes and methods for workig with DB API 2 databases.

This package contains:
* An "cored" abstraction over DB API 2 that makes common tasks simple to do, but doesn't get in your
  way for more complext tasks.
* A simple Model base class for easily defining and working with database tables.
* A simple Validation class for defining and running validations on models.
* A thing wrapper on DataAccess called ModelAccess which works with Models rather than directly
  with tables.
"""
from .data_access import DataAccess, transaction, autocommit
from .data_access_core import DataAccessCoreBase, InjectedDataAccessCore
from .foreign_model_wrapper import ForeignModelWrapper
from .model_access import ModelAccess
from .model_base import ModelBase
from .sql_writer import SQLWriter
from .validation import Validation, Validator

from . import pg_advisory_lock
