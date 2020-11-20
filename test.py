import datetime

datetime_object = datetime.datetime.now().strftime('%Y%m%dT%H%M%S%z')
print(datetime_object)
utc_dt_aware = datetime.datetime.now(datetime.timezone.utc).timestamp()
print(utc_dt_aware)
