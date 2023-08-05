from datetime import date as vanilla_date


def ordinal(n):
    suffix = "th"
    if (0 < n % 10 < 4) and not (10 < n % 100 < 14):
        if n % 10 == 1:
            suffix = "st"
        elif n % 10 == 2:
            suffix = "nd"
        else:
            suffix = "rd"
    return "%d%s" % (n, suffix)


def month_string(n):
    d = vanilla_date(1995, n, 1)
    return d.strftime("%B")
