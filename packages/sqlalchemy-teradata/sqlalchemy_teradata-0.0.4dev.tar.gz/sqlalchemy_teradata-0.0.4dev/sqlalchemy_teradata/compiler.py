from sqlalchemy.sql import compiler
from sqlalchemy import exc
from sqlalchemy import schema as sa_schema
from sqlalchemy.types import Unicode


class TeradataCompiler(compiler.SQLCompiler):

    def __init__(self, dialect, statement, column_keys=None, inline=False, **kwargs):
        super(TeradataCompiler, self).__init__(dialect, statement, column_keys, inline, **kwargs)

    def get_select_precolumns(self, select, **kwargs):
        """Teradata uses TOP instead of LIMIT """

        if select._distinct or select._limit is not None:
            s = select._distinct and "DISTINCT " or ""
            if select._limit is not None:
                s += "TOP %d " % (select._limit)
            if select._offset is not None:
                raise exc.InvalidRequestError('Teradata does not support LIMIT with an offset')
            return s
        return compiler.SQLCompiler.get_select_precolumns(self, select)

    def render_literal_value(self, value, type_):
        if value is None:
            print "\n\tFOUND A NONE LITERAL!\n\t"

        if type(type_) == Unicode:
            pass
            # TODO: should the DBAPI handles this or should I?

        return compiler.SQLCompiler.render_literal_value(self, value, type_)

    def limit_clause(self, select):
        """Limit after SELECT"""
        return ""

#    def visit_select(self, select, **kwargs):
#        """ Implement LIMIT and OFFSET with QUALIFY/ROW_NUMBER()
#        ex:
#            SELECT ROW_NUMBER() OVER (ORDER BY custID) AS RowNum_
#                 , col1
#                   FROM myDatabase.myTable
#                   QUALIFY RowNum_ BETWEEN 10 and 100;
#
#            <=>
#
#            SELECT col1
#                   FROM myDatabase.myTable
#                   ORDER BY custID
#                   LIMIT 90 OFFSET 10;
#        """
#        if select._offset is not None:
#            orderby = self.process(select._order_by_clause)
#            if not orderby:
#                raise exc.CompileError('Teradata requires an order_by when using an offset')
#
#            _offset = select._offset
#            _limit = select._limit
#
#            # build the new select clause for QUALIFY_ROWNUMBER()
#            select = select.column(
#                sql.literal_column("ROW_NUMBER() OVER (ORDER BY %s)" % orderby).label("td_qr_clause")). \
#                order_by(None).alias()
#
#            td_qr_clause = sql.column('td_qr_clause')
#
#            result = sql.select([col for col in select.c if col.key != 'td_qr_clause'])
#            return self.process(result, isWrapper=True, **kwargs)
#
#        return compiler.SQLCompiler.visit_select(self, select, **kwargs)


class TeradataDDLCompiler(compiler.DDLCompiler):

    def visit_create_table(self, create):
        """ create is a CreateTable DDL clause"""

        # Table Kind: Set/MultiSet/Volatile, etc
        table = create.element
        print type(create)
        print type(table)
        table._prefixes = ["SET"]

        if 'table_kind' in table.kwargs:
            table._prefixes = [table.kwargs['table_kind']]


        # Fallback/Journal/Global Temp/Volatile -> todo

        return compiler.DDLCompiler.visit_create_table(self, create)

    def post_create_table(self, table):
        """ Processes Teradata specific keyword args passed in TABLE
            Currently, we support the following keywords:
                tdalchemy_unique_pi = col name for the UPI
                tdalchemy_nunique_pi = col name for the NUPI
                tdalchemy_index = col name for the index

         """
        table_opts = ' '
        table_kwargs = dict((k, v) for k, v in table.kwargs.items())
        if ('tdalchemy_unique_pi' in table_kwargs):
            table_opts += 'UNIQUE PRIMARY INDEX ('+table_kwargs['tdalchemy_unique_pi']+')'

        if not table.primary_key:
            table_opts += 'NO PRIMARY INDEX'

        return table_opts

    def get_column_specification(self, column, **kwargs):
        if column.table is None:
            raise exc.CompileError(
                "Teradata requires Table-bound columns "
                "in order to generate DDL")

        colspec = (self.preparer.format_column(column) + " " + self.dialect.type_compiler.process(
                     column.type, type_expression=column)
                   )

        # Null/NotNull
        if column.nullable is not None:
            if not column.nullable or column.primary_key:
                colspec += " NOT NULL"
            # else:
                # colspec += " NULL"

        # Use IDENTITY or SEQUENCE to autoincrement
        if isinstance(column.default, sa_schema.Sequence):
            if column.default.start == 0:
                start = 0
            else:
                start = column.default.start or 1
            colspec += " GENERATED ALWAYS AS IDENTITY(START WITH %s INCREMENT BY %s NO CYCLE)" % (start,
                                                                                                  column.default.increment or 1)
        elif column is column.table._autoincrement_column:
            colspec += " GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1 NO CYCLE)"

        return colspec


class TeradataTypeCompiler(compiler.GenericTypeCompiler):

    def _string_extend(self, type_, defaults, spec):

        def attr(name):
            return getattr(type_, name, defaults.get(name))
        """
        Generate the SQL for extended string-type declaration

        """
        # CHARACTER SETS
        if attr('charset'):
            charset = 'CHARACTER SET %s' % attr('charset')
        else:
            charset = None

        return ' '.join([w for w in (spec, charset) if w is not None])

    def _interval_extend(self, type_, defaults, spec):
        """
        Generate the SQL for INTERVAL types
        """
        def attr(name):
            return getattr(type_, name, defaults.get(name))

        # PRECISION
        if attr('precision'):
            spec += '(%s)' % attr('precision')

        # INTERVAL TO Data Type
        if attr('to'):
            to_type = "TO %s" % attr('to')
            if attr('to').upper() == 'SECOND':
                if attr('second_precision'):
                    to_type += '(%s)' % attr('second_precision')
        else:
            to_type = None

        return ' '.join([w for w in (spec, to_type) if w is not None])

    def visit_BOOLEAN(self, type_):
        return "BYTEINT"

    def visit_INTERVAL(self, type_):
        kind = getattr(type_, 'kind', None)
        prec = getattr(type_, 'precision', None)

        if kind is None:
            raise exc.InvalidRequestError("INTERVAL requires an argument ('YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'SECOND') for kind")

        elif kind.upper() == 'SECOND':
            frac_sec_prec = type_.second_precision
            if frac_sec_prec is not None and prec is not None:
                return "INTERVAL (%s, %s)" % (prec, frac_sec_prec)

        return self._interval_extend(type_, {'precision': 2, 'second_precision': 6}, "INTERVAL %s" % kind)

    # DATE, TIME, and TIMESTAMP
    def visit_TIME(self, type_):
        precision = getattr(type_, 'precision', None)
        if precision is not None:
            return "TIME(%s)" % precision
        return "TIME"

    def visit_TIMESTAMP(self, type_):
        precision = getattr(type_, 'precision', None)
        if precision is not None:
            return "TIMESTAMP(%s)" % precision
        return "TIMESTAMP"

    # NUMERIC (Decimals)
    def visit_DECIMAL(self, type_):
        if type_.precision is None and type_.scale is None:
            type_.precision = 5
            type_.scale = 0
        elif type_.scale is None:
            type_.scale = 0

        return "DECIMAL(%s,%s)" % (type_.precision, type_.scale)

    def visit_NUMERIC(self, type_):
        return self.visit_DECIMAL(type_)

    # CHARACTER and STRINGs
    def visit_CHAR(self, type_):
        if type_.length is not None:
            return self._string_extend(type_, {}, "CHAR(%s)" % type_.length)
        return self._string_extend(type_, {}, "CHAR")

    def visit_CLOB(self, type_):
        if type_.length is not None:
            if type_.multiplier is not None:
                return self._string_extend(type_, {}, "CLOB(%s)" % str(type_.length)+str(type_.multiplier))
            else:
                return self._string_extend(type_, {}, "CLOB(%s)" % str(type._length))

        return self._string_extend(type_, {}, "CLOB(%s)" % str(type._length))

    def visit_NCHAR(self, type_):
        if type_.length is not None:
            return self._string_extend(type_, {'charset': 'UNICODE'}, "CHAR(%s)" % type_.length)
        return self._string_extend(type_, {'charset': 'UNICODE'}, "CHAR")

    def visit_NVARCHAR(self, type_):
        if type_.length is None:
            return self._string_extend(type_, {'charset': 'UNICODE'}, "LONG VARCHAR")
        else:
            return self._string_extend(type_, {'charset': 'UNICODE'}, "VARCHAR(%s)" % type_.length)

    def visit_VARCHAR(self, type_):
        if type_.length is None:
            return self._string_extend(type_, {}, "LONG VARCHAR")
        else:
            return self._string_extend(type_, {}, "VARCHAR(%s)" % type_.length)

    def visit_TEXT(self, type_):
        if type_.length is None:
            return self._string_extend(type_, {'charset': 'UNICODE'}, "CLOB")
        return self._string_extend(type_, {'charset': 'UNICODE'}, "CLOB(%s)" % type_.length)

    def visit_UNICODE(self, type_):
        return self.visit_NVARCHAR(type_)

    def visit_unicode(self, type_):
        return self.visit_NVARCHAR(type_)

    def visit_unicode_text(self, type_):
        return self.visit_TEXT(type_)
