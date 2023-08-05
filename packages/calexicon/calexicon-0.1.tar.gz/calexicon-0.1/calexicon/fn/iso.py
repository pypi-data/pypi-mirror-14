from datetime import date as vanilla_date, timedelta

from ..dates.overflow import OverflowDate


def _check_week(week):
    if week < 1 or week > 54:
        raise ValueError(
            "Week number %d is invalid for an ISO calendar."
            % (week, )
        )


def iso_to_gregorian(year, week, weekday):
    _check_week(week)
    jan_8 = vanilla_date(year, 1, 8).isocalendar()
    offset = (week - jan_8[1]) * 7 + (weekday - jan_8[2])
    try:
        d = vanilla_date(year, 1, 8) + timedelta(days=offset)
    except:
        d = OverflowDate(isocalendar=(year, week, weekday))
    if d.isocalendar()[0] != year:
        raise ValueError(
            "Week number %d is invalid for ISO year %d."
            % (week, year)
        )
    return d
