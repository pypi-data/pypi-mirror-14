def previous_month(year, month):
    if month == 1:
        return (year - 1, 12)
    return (year, month - 1)
