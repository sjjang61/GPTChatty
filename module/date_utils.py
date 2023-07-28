import datetime

def now_date():
    return datetime.datetime.now()

def now_date_str( fmt='%Y-%m-%d'):
    now = datetime.datetime.today()
    return date_to_str( now, fmt )

def str_to_date(str, fmt='%Y-%m-%d'):
    return datetime.datetime.strptime(str, fmt)


def str_delta_date(str, days, fmt='%Y-%m-%d'):
    date = str_to_date(str, fmt)
    return date + datetime.timedelta(days=days)


def date_to_str(date, fmt='%Y-%m-%d'):
    return date.strftime(fmt)


def get_diff_days(date1, date2):
    delta = str_to_date(date1) - str_to_date(date2)
    return delta.days

def add_date( date, days ):
    return date + datetime.timedelta(days=days)
