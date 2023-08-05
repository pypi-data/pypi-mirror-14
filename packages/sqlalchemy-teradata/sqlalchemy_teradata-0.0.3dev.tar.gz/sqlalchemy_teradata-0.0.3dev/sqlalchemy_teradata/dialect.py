# The MIT License (MIT)
#
# Copyright (c) 2015 by Teradata
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from sqlalchemy.engine import default
from sqlalchemy import pool
from sqlalchemy.sql import select, and_, or_
from sqlalchemy_teradata.compiler import TeradataCompiler, TeradataDDLCompiler, TeradataTypeCompiler
from sqlalchemy_teradata.base import TeradataIdentifierPreparer, TeradataExecutionContext
from sqlalchemy_teradata.base import ischema_names as ischema
from sqlalchemy.sql.expression import text, table, column

class TeradataDialect(default.DefaultDialect):
    """
    Implements the Dialect interface. TeradataDialect inherits from the
       default.DefaultDialect. Changes made here are specific to Teradata where
       the default implementation isn't sufficient.

       Note that the default.DefaultDialect delegates some methods to the OdbcConnection
       in the tdodbc module passed in the dbapi class method

       """

    #name = 'teradata'
    driver = 'teradata'
    default_paramstyle = 'qmark'

    poolclass = pool.SingletonThreadPool
    statement_compiler = TeradataCompiler
    ddl_compiler = TeradataDDLCompiler
    type_compiler = TeradataTypeCompiler
    preparer = TeradataIdentifierPreparer
    execution_ctx_cls = TeradataExecutionContext

    ischema_names = ischema
    supports_native_boolean = False
    supports_native_decimal = True
    # convert_unicode = True
    encoding = 'utf-8'

    supports_unicode_statements = True
    supports_unicode_binds = True

    postfetch_lastrowid = False
    implicit_returning = False
    preexecute_autoincrement_sequences = False

    def __init__(self, **kwargs):
        super(TeradataDialect, self).__init__(**kwargs)

    def create_connect_args(self, url):
        if url is not None:
            params = super(TeradataDialect, self).create_connect_args(url)[1]
            return (("Teradata", params['host'], params['username'], params['password']), {})

    @classmethod
    def dbapi(cls):
        """ Hook to the dbapi2.0 implementation's module"""
        from teradata import tdodbc
        return tdodbc

    def normalize_name(self, name, **kw):
        return name.lower()

    def has_table(self, connection, table_name, schema=None):

        if schema is None:
            schema=self.default_schema_name

        stmt = select([column('tablename')],
                      from_obj=[text('dbc.tablesvx')]).where(
                          and_(text('creatorname=:user'),
                               text('tablename=:name')))
        res = connection.execute(stmt, user=schema, name=table_name).fetchone()
        return res is not None

    def _get_default_schema_name(self, connection):
        return self.normalize_name(
            connection.execute('select user').scalar())

    def get_table_names(self, connection, schema=None, **kw):

        if schema is None:
            schema = self.default_schema_name

        stmt = select([column('tablename')],
                from_obj = [text('dbc.TablesVX')]).where(
                and_(text('creatorname = :user'),
                    or_(text('tablekind=\'T\''),
                        text('tablekind=\'O\''))))
        res = connection.execute(stmt, user=schema).fetchall()
        return [self.normalize_name(name['tablename']) for name in res]

    def get_schema_names(self, connection, **kw):
        stmt = select(['username'],
               from_obj=[text('dbc.UsersV')],
               order_by=['username'])
        res = connection.execute(stmt).fetchall()
        return [self.normalize_name(name['tablename']) for name in res]

    def get_view_names(self, connection, schema=None, **kw):
        stmt = select(['tablename'],
               from_obj=[text('dbc.TablesVX')],
               whereclause='tablekind=\'V\'')
        res = connection.execute(stmt).fetchall()
        return [self.normalize_name(name['tablename']) for name in res]


dialect = TeradataDialect
