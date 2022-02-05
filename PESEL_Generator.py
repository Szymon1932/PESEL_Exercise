import pandas as pd
from faker.providers.ssn.pl_PL import Provider as SsnProvider
from faker import Faker
from datetime import datetime
from timeit import default_timer as timer



def generate_ssns(n):
    start = timer()
    z_list = []
    Ssn = SsnProvider(Faker())
    for _ in range(n):
        z_list.append(Ssn.ssn())
    srs = pd.Series(z_list)
    stop = timer()
    print("czas trwania: ", stop - start)
    return srs


# print(generate_ssns(2))

def generate_unique_ssns(n, sex, first_date, second_date):
    start = timer()
    pesel_list = []
    Ssn = SsnProvider(Faker())

    while len(pesel_list) != n:
        new_pesel = Ssn.ssn()
        pesel_year_digits = int(new_pesel[0] + new_pesel[1])
        cond_1 = first_date.year % 100 <= pesel_year_digits <= second_date.year % 100
        pesel_month_digits = int(new_pesel[2] + new_pesel[3])
        cond_2 = pesel_month_digits <= second_date.month
        pesel_day_digits = int(new_pesel[4] + new_pesel[5])
        cond_3 = pesel_day_digits <= second_date.day
        pesel_sex_digit = int(new_pesel[9])
        cond_4 = 1
        if not (sex == 'f' and pesel_sex_digit % 2 == 0) or (sex == 'm' and pesel_sex_digit % 2 == 1):
            cond_4 = 0

        if not (cond_1 and cond_2 and cond_3 and cond_4):
            continue
        pesel_list.append(new_pesel)
        pesel_list = list(dict.fromkeys(pesel_list))

    srs = pd.Series((pesel_list), dtype=pd.StringDtype())
    stop = timer()
    print("Czas trwania: ", stop - start)
    return srs


def validate_ssn(pesel, sex, date_of_birth):
    control_sum = 0
    cond_pesel = False
    wages = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    for e in range(10):
        control_sum += wages[e] * int(pesel[e])
    pom = control_sum % 10
    x = 10 - pom
    if pom == 0:
        if int(pesel[10]) == 0:
            cond_pesel = True
    else:
        if int(pesel[10]) == x:
            cond_pesel = True

    temp_year = pesel[0] + pesel[1]
    temp_month = pesel[2] + pesel[3]
    temp_day = pesel[4] + pesel[5]
    temp_sex = int(pesel[9])
    cond = False
    if int(temp_year) == date_of_birth.year % 100 and cond_pesel:

        if date_of_birth.year >= 2000:

            if int(temp_month) - 20 == date_of_birth.month:
                if int(temp_day) == date_of_birth.day:

                    if (sex == 'f' and temp_sex % 2 == 0) or (sex == 'm' and temp_sex % 2 == 1):
                        cond = True
        else:

            if int(temp_month) == date_of_birth.month:
                if int(temp_day) == date_of_birth.day:
                    if (sex == 'f' and temp_sex % 2 == 0) or (sex == 'm' and temp_sex % 2 == 1):
                        cond = True

    return cond



# płeć żeńska = f, płeć męska = m
# założenie: daty do 1999 roku, mężczyźni
date1 = datetime.fromisoformat('1990-01-01')
date2 = datetime.fromisoformat('1990-01-19')
# print(generate_unique_ssns(1000,'m',date1,date2))

# generate_ssns(1000)
# generate_ssns(10000)
# generate_ssns(100000)
# generate_unique_ssns(100,'f',date1,date2)
# generate_unique_ssns(100,'f',date1,date2)
# generate_unique_ssns(100,'f',date1,date2)


# generate_unique_ssns(10000,'f',date1,date2)
# generate_unique_ssns(100000,'f',date1,date2)

datex = datetime.fromisoformat('2000-10-23')
datey = datetime.fromisoformat('1975-12-27')
datez = datetime.fromisoformat('1999-11-24')
print(validate_ssn('00302391914', 'm', datex))
print(validate_ssn('75122709085', 'f', datey))
print(validate_ssn('99112401890', 'm', datez))
