# import datetime

# datetime_object = datetime.datetime.now().strftime('%Y%m%dT%H%M%S%z')
# print(datetime_object)
# utc_dt_aware = datetime.datetime.now(datetime.timezone.utc).timestamp()
# print(utc_dt_aware)

a = [{'nojs': 'JS10', 'site': 'ok'}, {'nojs': 'JS11', 'site': 'ok1'}]
for x in a:
    if x['nojs'] == 'JS11':
        site = x
        break

test = next(x for x in a if x['nojs'] == 'JS11')
print(test)
