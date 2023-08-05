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

from sqlalchemy.sql import compiler
from sqlalchemy.engine import default
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import ClauseElement, Executable
from sqlalchemy import types as sqltypes
from sqlalchemy.types import CHAR, DATE, DATETIME, \
                    BLOB, CLOB, TIMESTAMP, FLOAT, BIGINT, DECIMAL, NUMERIC, \
                    NCHAR, NVARCHAR, INTEGER, \
                    SMALLINT, TIME, TEXT, VARCHAR, REAL

ReservedWords = set(["abort", "abortsession", "abs", "access_lock", "account",
                    "acos", "acosh", "add", "add_months", "admin", "after",
                    "aggregate","all", "alter", "amp", "and", "ansidate",
                    "any", "arglparen", "as", "asc", "asin", "asinh", "at",
                     "atan", "atan2", "atanh", "atomic", "authorization", "ave",
                     "average", "avg", "before", "begin" , "between", "bigint",
                     "binary", "blob", "both", "bt", "but", "by", "byte", "byteint",
                     "bytes", "call", "case", "case_n", "casespecific", "cast", "cd",
                     "char", "char_length", "char2hexint","count", "title", "value",
                     'user','password',"year", "match"])

ischema_names = {
 'BLOB': BLOB,
 'BIGINT': BIGINT,
 'CHAR': CHAR,
 'CHARACTER': CHAR,
 'CLOB': CLOB,
 'DATE': DATE,
 'DATETIME': DATETIME,
 'DECIMAL': DECIMAL,
 'DOUBLE PRECISION': NUMERIC,
 'FLOAT': FLOAT,
 'INT': INTEGER,
 'INTEGER': INTEGER,
 'NUMERIC': NUMERIC,
 'REAL': REAL,
 'SMALLINT': SMALLINT,
 'TEXT': CLOB,
 'TIME': TIME,
 'VARCHAR': VARCHAR,
}


# TODO: just use hard coded text for now
class QualifyClause(ClauseElement):
    def __init__(self, col):
        self.col = col


@compiles(QualifyClause)
def visit_qualify_clause(col, compiler, **kw):
    return "QUALIFY %s" % compiler.process(col.name)


class TeradataExecutionContext(default.DefaultExecutionContext):

    def __init__(self, dialect, connection, dbapi_connection, compiled_ddl):

        super(TeradataExecutionContext, self).__init__(dialect, connection,
                                                       dbapi_connection,
                                                       compiled_ddl)


class TeradataIdentifierPreparer(compiler.IdentifierPreparer):
    reserved_words = ReservedWords

    def __init__(self, dialect, initial_quote='"', final_quote=None, escape_quote='"', omit_schema=False):

        super(TeradataIdentifierPreparer, self).__init__(dialect, initial_quote, final_quote,
                                                         escape_quote, omit_schema)

