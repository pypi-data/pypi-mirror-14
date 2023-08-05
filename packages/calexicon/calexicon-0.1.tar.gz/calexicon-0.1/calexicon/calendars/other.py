from datetime import date as vanilla_date, timedelta

from .base import Calendar
from ..constants import number_of_vanilla_dates
from ..dates.bce import BCEDate
from ..dates.distant import DistantDate


class JulianDayNumber(Calendar):
    first_ce_day = vanilla_date(1, 1, 1)
    first_ce_day_number = 1721423
    display_name = "Julian Day Number"
    representation_keys = set(['day_number'])

    @staticmethod
    def date_display_string(d):
        n = JulianDayNumber._day_number(d)
        return "Day %d" % n

    @staticmethod
    def representation(d):
        return {'day_number': JulianDayNumber._day_number(d)}

    @staticmethod
    def _day_number(d):
        return (d - JulianDayNumber.first_ce_day).days + JulianDayNumber.first_ce_day_number

    @staticmethod
    def _bce_representation(n):
        count = 0 - n
        n_4_yr_periods = count // (365 * 4 + 1)
        remainder = count % (365 * 4 + 1)
        td = vanilla_date(8, 1, 1) - timedelta(days=remainder)
        year = td.year - 8 - 4 * n_4_yr_periods
        return (year, td.month, td.day)

    def date(self, n):
        offset = n - self.first_ce_day_number
        if offset >= 0 and offset <= number_of_vanilla_dates:
            vd = self.first_ce_day + timedelta(days=offset)
            return self.from_date(vd)
        elif offset > number_of_vanilla_dates:
            d = DistantDate(10000, 1, 1) + timedelta(days=offset - number_of_vanilla_dates - 1)
            return self.from_date(d)
        else:
            d = BCEDate(*self._bce_representation(offset))
            return self.from_date(d)


class AstronomicalCalendar(Calendar):
    display_name = "Astronomical Calendar"
    representation_keys = set(['year', 'month', 'day'])

    @staticmethod
    def date_display_string(d):
        return "0/1/1"

    @staticmethod
    def representation(d):
        return dict(year=0, month=1, day=1)

    def date(self, y, m, d):
        try:
            vd = vanilla_date(y, m, d)
            return self.from_date(vd)
        except ValueError:
            d = None
            return self.from_date(d)
