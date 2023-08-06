from datetime import datetime
from tornado.options import options
from sqlalchemy import (
    MetaData, Table, Column, Numeric, Integer, Boolean, DateTime, select)

# keys containing
_indexable = ['.status', 'plo.ok']

# Global access to the table schema
brush = None


def initialize(comb, engine):
    """Initialize and create a new table if it does not already exist.

    Parameters
    ----------
    comb : :class:`brush.comb.FrequencyComb`
    engine
        SQLAlchemy engine

    """
    global brush
    metadata = MetaData()

    sql_dtypes = {
        'double': Numeric,
        'int': Integer,
        'bool': Boolean
    }

    col_names = sorted(comb.metadata.keys())
    columns = [Column(col.replace('.', '_'),
               sql_dtypes[comb.metadata[col]['type']],
               index=(any(k in col for k in _indexable) or col == 'system.locked'),
               nullable=True)
               for col in col_names if 'timestamp' not in col]

    # Ensure that SQLAlchemy returns a Python float for serialization
    for col in columns:
        if isinstance(col.type, Numeric):
            col.type.asdecimal = False

    data = Table(options.sql_table, metadata,
                 Column('id', Integer, primary_key=True),
                 Column('timestamp', DateTime, index=True, unique=True),
                 *columns)

    metadata.create_all(engine)
    brush = data
    return data


def select_timeseries(table, start, stop=None):
    """Select timeseries data from the database.

    Parameters
    ----------
    table : SQLAlchemy.Table
        Table to query
    start : datetime.datetime
        UTC timestamp indicating the start time
    stop : datetime.datetime
        UTC timestamp indicating the end time

    Returns
    -------
    sel
        The SQLAlchemy selectable

    """
    # start = datetime.utcfromtimestamp(start)
    # if stop is not None:
    #     stop = datetime.utcfromtimestamp(stop)
    # else:
    #     stop = datetime.utcnow()
    if stop is None:
        stop = datetime.utcnow()
    sel = select([table]).\
          where(table.c.timestamp >= start).\
          where(table.c.timestamp <= stop)
    return sel
