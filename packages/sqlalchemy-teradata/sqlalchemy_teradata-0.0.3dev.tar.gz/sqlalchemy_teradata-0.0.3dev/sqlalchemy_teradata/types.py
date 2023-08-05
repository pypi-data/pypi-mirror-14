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

from sqlalchemy import types, exc
import datetime


# TIME

class _TimeType(types.Time):
    """ Base class for teradata time types """
    def __init__(self, precision=None, **kwargs):
        """ Construct a TIME

        Note: TIME is non-ANSI standard. The Teradata Database stores TIME in UTC
        :param precision: fractional seconds precision. A single digit
        representing the number of significant digits in the fractional
        portion of the SECOND field. Valid values range from 0 to 6 inclusive.
        The default precision is 6
        """
        self.precision = precision

        super(_TimeType, self).__init__(**kwargs)


class TIME(_TimeType, types.TIME):
    """ Teradata TIME type stored in UTC """

    __visit__name = 'TIME'

    def __init__(self, precision=None, **kwargs):
        """ Construct a TIME stored as UTC in Teradata

        :param precision: optional fractional seconds precision. A single digit
        representing the number of significant digits in the fractional
        portion of the SECOND field. Valid values range from 0 to 6 inclusive.
        The default precision is 6

        """
        self.precision = precision

        super(TIME, self).__init__(precision=precision, **kwargs)


class TIMESTAMP(_TimeType, types.TIMESTAMP):
    """ Teradata TIMESTAMP type stored in UTC """

    __visit__name = 'TIMESTAMP'

    def __init__(self, precision=None, **kwargs):
        """ Construct a TIMESTAMP stored as UTC in Teradata

        :param precision: optional fractional seconds precision. A single digit
        representing the number of significant digits in the fractional
        portion of the SECOND field. Valid values range from 0 to 6 inclusive.
        The default precision is 6

        """
        self.precision = precision

        super(TIMESTAMP, self).__init__(precision=precision, **kwargs)


# Interval
class _IntervalType(types.Interval):
    """ Base class for teradata interval types """

    # TODO: probably should make sure kind and to are valid
    def __init__(self, kind, to=None, precision=None, isliteral=False, **kwargs):

        """ Construct an Interval
        :param kind: the kind of interval to create. The argument to kind
        can be 'YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'SECOND'.
        This parameter is not optional. If kind is None, an InvalidRequestError is thrown.

        :param to: optional parameter to specify in combination with kind. The argument can be
        'MONTH', 'HOUR', 'MINUTE', 'SECOND'. Valid arguments for 'to' depend on the kind: If kind is 'YEAR'
        to can be 'MONTH'. If kind is 'DAY' to can be 'HOUR', 'MINUTE', 'SECOND'. If kind is 'HOUR' to can
        be 'MINUTE', 'SECOND'. If kind is 'MINUTE' to can be 'SECOND'.

        :param precision: permitted range of digits for Interval YEAR/MONTH/DAY/HOUR/MINUTE/SECOND
        ranging from 1 to 4. The default precision is 2. Note that this should not be confused with
        second_precision nor day_precision.

        :param second_precision: optional fractional precision for the values of SECOND from 0 to 6. The default is 6.
        This paramter is only used and applied when kind or to is 'SECOND'

        :param day_precision: this parameter is IGNORED. Use precision instead.

        :param literal: optional boolean set to False by default. If set to True,
        expects a 'string' key in kwargs whose value is the literal. You can also provide an optional
        'sign' key. If the 'sign' key is found then it indicates a negative interval, otherwise the
        default is a positive interval.

        """
        if kind is None:
            raise exc.InvalidRequestError("INTERVAL requires an argument ('YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'SECOND') to kind")

        self.kind = kind
        self.to = to
        self.precision = precision

        super(_IntervalType, self).__init__(**kwargs)


class INTERVAL(_IntervalType, types.Interval):
    """ Teradata Interval """

    __visit_name__ = 'INTERVAL'

    def __init__(self, second_precision=None, day_precision=None, **kwargs):
        return super(INTERVAL, self).__init__(second_precision=second_precision,
                                              day_precision=day_precision, **kwargs)


class _StringType(types.String):
    """ Base class for Teradata string types """

    # TODO: add FORMAT/TITLE attributes
    def __init__(self, charset=None, **kw):

        self.charset = charset

        super(_StringType, self).__init__(**kw)


class CHAR(_StringType, types.CHAR):
    """ Teradata fixed length character string """

    __visit_name__ = 'CHAR'

    def __init__(self, length=None, **kwargs):
        """ Construct a CHAR

        :param length: number of characters or bytes allocated. Maximum value
        for n depends on the character set. For LATIN - 64000 characters,
        For UNICODE - 32000 characters, For KANJISJIS - 32000 bytes. If a value
        for n is not specified, the default is 1.

        :param charset: Server character set for the character column.
        The default server character set depends on how the user is
        defined in the DEFAULT CHARACTER SET clause of the CREATE USER statement.
        Supported values:
            LATIN: fixed 8-bit characters from the ASCII ISO 8859 Latin1
            or ISO 8859 Latin9.
            UNICODE: fixed 16-bit characters from the UNICODE 6.0 standard.
            GRAPHIC: fixed 16-bit UNICODE characters defined by IBM
            Corporation for DB2.
            KANJISJIS: mixed single byte/multibyte characters intended for
            Japanese applications that rely on KanjiShiftJIS characteristics.

        """
        super(CHAR, self).__init__(length=length, **kwargs)


class VARCHAR(_StringType, types.VARCHAR):
    """ Teradata VARCHAR type, for variable length char data """

    __visit_name__ = 'VARCHAR'

    # TODO: add more column attributes (casespecific, etc.)
    def __init__(self, length=None, **kwargs):
        """Construct a VARCHAR

        :param length: Optional 0 to n. If None, it will use LONG
        (the longest permissible variable length character string)

        :param charset: optional character set for varchar.

        """
        super(VARCHAR, self).__init__(length=length, **kwargs)


class CLOB(_StringType, types.CLOB):
    """ Teradata CLOB  for large character srtings such as Text or HTML """

    __visit_name__ = 'CLOB'

    def __init__(self, length=None, multiplier=None, **kwargs):

        """Construct a CLOB

        :param length: Optional length for clob. For Latin server character set,
        n cannot exceed 2097088000. For Unicode server character set,
        n cannot exceed 1048544000. If no length is specified then the maximum is used.

        :param multiplier: Either 'K', 'M', or 'G'.
        K specifies number of characters to allocate as nK, where K=1024
        (For Latin char sets, n < 2047937 and For Unicode char sets, n < 1023968)
        M specifies nM, where M=1024K
        (For Latin char sets, n < 1999 and For Unicode char sets, n < 999)
        G specifies nG, where M=1024M
        (For Latin char sets, n must be 1 and char set must be LATIN)

        :param charset: LATIN (fixed 8-bit characters from the ASCII ISO 8859 Latin1 or ISO 8859 Latin9)
        or UNICODE (fixed 16-bit characters from the UNICODE 6.0 standard)
        """
        self.multipler = multiplier

        super(CLOB, self).__init__(length=length, **kwargs)


class TEXT(_StringType, types.Text):
    """ TEXT is essentially CLOB w/o a multiplier"""

    __visit_name__ = 'TEXT'

    def __init__(self, length=None, **kwargs):
        super(TEXT, self).__init__(length=length, **kwargs)
