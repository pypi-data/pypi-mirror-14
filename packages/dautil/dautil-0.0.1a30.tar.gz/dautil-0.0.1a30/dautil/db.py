''' Database related utilities. '''
from dautil import log_api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def not_empty(session, table):
    ''' Checks whether a table is empty.

    :param session: A `SQLAlchemy` session.
    :param table: The entity class of a database table.

    :returns: `True` if the table is not empty.
    '''
    return session.query(table).count() > 0


def create_session(dbname, base, prefix='sqlite:///{}'):
    ''' Creates a database session.

    :param dbname: The name of the database.
    :param base: The declarative Base class.
    :param prefix: The string at the start of the database URL.

    :returns: The database session.
    '''
    engine = create_engine(prefix.format(dbname))
    DBSession = sessionmaker(bind=engine)
    base.metadata.create_all(engine)

    return DBSession()


def count_where(session, column, search_val):
    ''' Gets the count of a query as in the following SQL \
        `SELECT count(column) from atable where atable = 'search_val'`\

        .. note:: **DO NOT USE** when high-performance is required.

    :param session: A `SQLAlchemy` session.
    :param column: A table column as attribute in a Python class.
    :param search_val: Value to search for.

    :returns: The count of the query.
    '''
    return session.query(column).filter(column == search_val).count()


def entity_from_column(column):
    ''' Utility function which returns the entity of a column.

    :param column: A table column as attribute in a Python class.

    :returns: The entity.
    '''
    return column.parent.entity


def where_first(session, column, search_val):
    ''' Gets the first row as in the following SQL \
        `SELECT * from atable where atable = 'search_val'`

    :param session: A `SQLAlchemy` session.
    :param column: A table column as attribute in a Python class.
    :param search_val: Value to search for.

    :returns: The first row of the query.
    '''
    logger = log_api.env_logger()
    result = session.query(entity_from_column(column)).\
        filter(column == search_val).first()
    logger.debug('search_val=%s result=%s', search_val, result)

    return result


def map_to_id(session, column):
    ''' Assuming that a table has a primary key column 'id'. \
        This function creates dictionary with column value as key \
        and id as value.

    :param session: A `SQLAlchemy` session.
    :param column: A table column as attribute in a Python class.

    :returns: A dictionary with column values mapped to id.
    '''
    id_map = {}
    logger = log_api.env_logger()
    table = column.parent.entity
    query = session.query(table.id, column)
    logger.debug('Query %s', query)

    for id, val in query.all():
        id_map[val] = id

    logger.debug('Id map %s', id_map)

    return id_map
