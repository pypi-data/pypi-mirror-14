from tornado.options import options
from sqlalchemy import (
    MetaData, Table, Column, Numeric, Integer, Boolean, DateTime)

# keys containing
_indexable = ['.status', 'plo.ok']


def initialize(comb, engine):
    """Initialize and create a new table if it does not already exist.

    Parameters
    ----------
    comb : :class:`brush.comb.FrequencyComb`
    engine
        SQLAlchemy engine

    """
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

    data = Table(options.sql_table, metadata,
                 Column('id', Integer, primary_key=True),
                 Column('timestamp', DateTime, index=True, unique=True),
                 *columns)

    metadata.create_all(engine)
    return data
