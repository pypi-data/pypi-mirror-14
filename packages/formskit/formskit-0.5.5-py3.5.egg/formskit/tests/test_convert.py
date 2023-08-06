from datetime import datetime

from formskit.converters import ToBool
from formskit.converters import ToDate
from formskit.converters import ToDatetime
from formskit.converters import ToInt
from formskit.field import Field
from formskit.tests.base import FormskitTestCase


class TestFakeConvert(FormskitTestCase):

    def setUp(self):
        super().setUp()
        self.field = Field('name1')

    def test_convert(self):
        self.field.set_values(['data'])
        assert self.field.values[0].value == 'data'
        assert self.field.get_value() == 'data'

    def test_convert_back(self):
        self.field.set_value('data')
        assert self.field.values[0].value == 'data'
        assert self.field.get_value() == 'data'


class TestToInt(FormskitTestCase):

    def setUp(self):
        super().setUp()
        self.field = Field('name1', convert=ToInt())

    def test_convert(self):
        self.field.set_values(['12'])
        assert self.field.values[0].value == '12'
        assert self.field.get_value() == 12

    def test_convert_fail(self):
        self.field.set_values([''])
        assert self.field.values[0].value == ''
        assert self.field.get_value() is None

    def test_convert_back(self):
        self.field.set_value(12)
        assert self.field.values[0].value == '12'
        assert self.field.get_value() == 12

    def test_convert_back_fail(self):
        self.field.set_value(None)
        assert self.field.values[0].value is None
        assert self.field.get_value() is None


class TestToBool(FormskitTestCase):

    def setUp(self):
        super().setUp()
        self.field = Field('name1', convert=ToBool())

    def test_convert(self):
        self.field.set_values(['1'])
        self.field.get_raw_value() == '1'
        assert self.field.get_value() is True

        self.field.set_values(['0'])
        self.field.get_raw_value() == '0'
        assert self.field.get_value() is False

    def test_unconvert(self):
        self.field.set_value(True)
        self.field.get_raw_value() == '1'
        assert self.field.get_value() is True

        self.field.set_value(False)
        self.field.get_raw_value() == '0'
        assert self.field.get_value() is False

    def test_make_convert(self):
        self.field.validate()
        assert self.field.get_value() is False


class TestToDate(FormskitTestCase):

    def setUp(self):
        super().setUp()
        self.field = Field('name1', convert=ToDate())

    def test_convert(self):
        self.field.set_values(['2016-01-02'])
        self.field.get_raw_value() == '2016-01-02'
        assert self.field.get_value() == datetime(year=2016, month=1, day=2)

    def test_convert_fail(self):
        self.field.set_values(['2016-01x-02'])
        self.field.get_raw_value() == '2016-01-02'
        assert self.field.get_value() is None

    def test_convert_back(self):
        self.field.set_value(datetime(year=2016, month=1, day=2))
        self.field.get_raw_value() == '2016-01-02'
        assert self.field.get_value() == datetime(year=2016, month=1, day=2)

    def test_convert_back_fail(self):
        self.field.set_value(None)
        self.field.get_raw_value() is None
        assert self.field.get_value() is None


class TestToDatetime(FormskitTestCase):
    timestamp = datetime(year=2016, month=1, day=2, hour=15, minute=12)

    def setUp(self):
        super().setUp()
        self.field = Field('name1', convert=ToDatetime())

    def test_convert(self):
        self.field.set_values(['2016-01-02 15:12'])
        self.field.get_raw_value() == '2016-01-02 15:12'
        assert self.field.get_value() == self.timestamp

    def test_convert_fail(self):
        self.field.set_values(['2016-01x-02'])
        self.field.get_raw_value() == '2016-01-02 15:12'
        assert self.field.get_value() is None

    def test_convert_back(self):
        self.field.set_value(self.timestamp)
        self.field.get_raw_value() == '2016-01-02 15:12'
        assert self.field.get_value() == self.timestamp

    def test_convert_back_fail(self):
        self.field.set_value(None)
        self.field.get_raw_value() is None
        assert self.field.get_value() is None

    def test_make_convert(self):
        self.field.set_values(['2016-01-02', '15:12'])
        self.field.validate()
        assert self.field.get_value() == self.timestamp
