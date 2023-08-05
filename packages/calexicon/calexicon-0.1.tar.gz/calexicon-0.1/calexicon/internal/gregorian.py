from .general import previous_month


def is_gregorian_leap_year(y):
    if (y % 400) == 0:
        return True
    if (y % 100) == 0:
        return False
    if (y % 4) == 0:
        return True
    return False


def days_in_month(year, month):
    if month == 2 and is_gregorian_leap_year(year):
        return 29
    return [None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month]


def days_in_previous_month(year, month):
    return days_in_month(*previous_month(year, month))
