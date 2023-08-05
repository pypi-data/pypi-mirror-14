from ..calendars import JulianCalendar, ProlepticGregorianCalendar
from ..calendars import JulianDayNumber, ProlepticJulianCalendar


def julian_to_gregorian(year, month, day):
    calendar = JulianCalendar()
    d = calendar.date(year, month, day)
    converted = d.convert_to(ProlepticGregorianCalendar())
    converted = converted.native_representation()
    return (converted['year'], converted['month'], converted['day'])


def gregorian_to_julian(year, month, day):
    calendar = ProlepticGregorianCalendar()
    d = calendar.date(year, month, day)
    converted = d.convert_to(JulianCalendar()).native_representation()
    return (converted['year'], converted['month'], converted['day'])


def julian_to_julian_day_number(year, month, day):
    calendar = ProlepticJulianCalendar()
    d = calendar.date(year, month, day)
    converted = d.convert_to(JulianDayNumber())
    return converted.native_representation()['day_number']


def julian_day_number_to_julian(number):
    calendar = JulianDayNumber()
    d = calendar.date(number)
    converted = d.convert_to(ProlepticJulianCalendar())
    rep = converted.native_representation()
    fields = [ rep[x] for x in ['year', 'month', 'day'] ]
    return tuple(fields)
