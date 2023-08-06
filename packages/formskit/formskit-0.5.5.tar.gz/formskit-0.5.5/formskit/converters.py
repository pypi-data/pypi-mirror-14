from datetime import datetime


class FakeConvert(object):
    """Default convertor which does nothing."""

    def _set_field(self, field):
        self.field = field

    def __call__(self, value):
        return self.convert(value)

    def convert(self, value):
        return value

    def convert_back(self, value):
        return value

    def back(self, value):
        return self.convert_back(value)

    def make_field(self):
        pass


class ToInt(FakeConvert):
    """Converts to int."""

    def convert(self, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    def convert_back(self, value):
        if value is None:
            return None
        else:
            return str(value)


class ToDate(FakeConvert):
    """Converts to datetime."""
    format = '%Y-%m-%d'

    def convert(self, value):
        try:
            return datetime.strptime(value, self.format)
        except (ValueError, TypeError):
            return None

    def convert_back(self, value):
        if value:
            return value.strftime(self.format)
        else:
            return None


class ToDatetime(FakeConvert):
    """Converts to datetime."""
    format = '%Y-%m-%d %H:%M'

    def convert(self, value):
        try:
            return datetime.strptime(value, self.format)
        except (ValueError, TypeError):
            return None

    def convert_back(self, value):
        if value:
            return value.strftime(self.format)
        else:
            return None

    def make_field(self):
        fvalue = self.field.values.pop(1)
        self.field.values[0].value += ' ' + fvalue.value


class ToBool(FakeConvert):

    def convert(self, value):
        if value in ['1', '2']:
            return True
        else:
            return False

    def convert_back(self, value):
        if value:
            return '1'
        else:
            return ''

    def make_field(self):
        value = (
            self.field.form and
            self.field.name in self.field.form.raw_data
        )
        self.field.set_value(value)
