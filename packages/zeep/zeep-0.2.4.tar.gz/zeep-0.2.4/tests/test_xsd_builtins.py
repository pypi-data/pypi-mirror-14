import datetime
from decimal import Decimal as D

import isodate
import six

from zeep.xsd import builtins


class TestString:

    def test_xmlvalue(self):
        instance = builtins.String()
        result = instance.xmlvalue('foobar')
        assert result == 'foobar'

    def test_pythonvalue(self):
        instance = builtins.String()
        result = instance.pythonvalue('foobar')
        assert result == 'foobar'


class TestBoolean:

    def test_xmlvalue(self):
        instance = builtins.Boolean()
        assert instance.xmlvalue(True) == 'true'
        assert instance.xmlvalue(False) == 'false'
        assert instance.xmlvalue(1) == 'true'
        assert instance.xmlvalue(0) == 'false'

    def test_pythonvalue(self):
        instance = builtins.Boolean()
        assert instance.pythonvalue('1') is True
        assert instance.pythonvalue('true') is True
        assert instance.pythonvalue('0') is False
        assert instance.pythonvalue('false') is False


class TestDecimal:

    def test_xmlvalue(self):
        instance = builtins.Decimal()
        assert instance.xmlvalue(D('10.00')) == '10.00'
        assert instance.xmlvalue(D('10.000002')) == '10.000002'
        assert instance.xmlvalue(D('10.000002')) == '10.000002'
        assert instance.xmlvalue(D('10')) == '10'
        assert instance.xmlvalue(D('-10')) == '-10'

    def test_pythonvalue(self):
        instance = builtins.Decimal()
        assert instance.pythonvalue('10') == D('10')
        assert instance.pythonvalue('10.001') == D('10.001')
        assert instance.pythonvalue('+10.001') == D('10.001')
        assert instance.pythonvalue('-10.001') == D('-10.001')


class TestFloat:

    def test_xmlvalue(self):
        instance = builtins.Float()
        assert instance.xmlvalue(float(10)) == '10.0'
        assert instance.xmlvalue(float(3.9999)) == '3.9999'
        assert instance.xmlvalue(float('inf')) == 'INF'
        assert instance.xmlvalue(float(12.78e-2)) == '0.1278'
        if six.PY2:
            assert instance.xmlvalue(float('1267.43233E12')) == '1.26743233E+15'
        else:
            assert instance.xmlvalue(float('1267.43233E12')) == '1267432330000000.0'

    def test_pythonvalue(self):
        instance = builtins.Float()
        assert instance.pythonvalue('10') == float('10')
        assert instance.pythonvalue('-1E4') == float('-1E4')
        assert instance.pythonvalue('1267.43233E12') == float('1267.43233E12')
        assert instance.pythonvalue('12.78e-2') == float('0.1278')
        assert instance.pythonvalue('12') == float(12)
        assert instance.pythonvalue('-0') == float(0)
        assert instance.pythonvalue('0') == float(0)
        assert instance.pythonvalue('INF') == float('inf')


class TestDateTime:

    def test_xmlvalue(self):
        instance = builtins.DateTime()
        value = datetime.datetime(2016, 3, 4, 21, 14, 42)
        assert instance.xmlvalue(value) == '2016-03-04T21:14:42'

    def test_pythonvalue(self):
        instance = builtins.DateTime()
        value = datetime.datetime(2016, 3, 4, 21, 14, 42)
        assert instance.pythonvalue('2016-03-04T21:14:42') == value


class TestDate:

    def test_xmlvalue(self):
        instance = builtins.Date()
        value = datetime.datetime(2016, 3, 4)
        assert instance.xmlvalue(value) == '2016-03-04'

    def test_pythonvalue(self):
        instance = builtins.Date()
        value = datetime.date(2016, 3, 4)
        assert instance.pythonvalue('2016-03-04') == value


class TestTime:

    def test_xmlvalue(self):
        instance = builtins.Time()
        value = datetime.time(21, 14, 42)
        assert instance.xmlvalue(value) == '21:14:42'

    def test_pythonvalue(self):
        instance = builtins.Time()
        value = datetime.time(21, 14, 42)
        assert instance.pythonvalue('21:14:42') == value

        value = datetime.time(21, 14, 42, 120000)
        assert instance.pythonvalue('21:14:42.120') == value

        value = isodate.parse_time('21:14:42.120+0200')
        assert instance.pythonvalue('21:14:42.120+0200') == value


class TestDuration:

    def test_xmlvalue(self):
        instance = builtins.Duration()
        value = isodate.parse_duration('P0Y1347M0D')
        assert instance.xmlvalue(value) == 'P1347M'

    def test_pythonvalue(self):
        instance = builtins.Duration()
        expected = isodate.parse_duration('P0Y1347M0D')
        value = 'P0Y1347M0D'
        assert instance.pythonvalue(value) == expected
