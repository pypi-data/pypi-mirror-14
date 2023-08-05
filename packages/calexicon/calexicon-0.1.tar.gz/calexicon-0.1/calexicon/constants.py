from datetime import date as vanilla_date

first_julian_date = (-45, 1, 1)

first_vanilla_date = vanilla_date(1, 1, 1)
last_vanilla_date = vanilla_date(9999, 12, 31)

julian_day_number_of_first_vanilla_date = 1721423
julian_day_number_of_last_vanilla_date = (
    julian_day_number_of_first_vanilla_date +
    (last_vanilla_date - first_vanilla_date).days
)

number_of_vanilla_dates = (last_vanilla_date - first_vanilla_date).days

number_of_days_in_400_gregorian_years = (vanilla_date(2000, 1, 1) - vanilla_date(1600, 1, 1)).days
