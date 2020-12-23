# import datetime

# datetime_object = datetime.datetime.now().strftime('%Y%m%dT%H%M%S%z')
# print(datetime_object)
# utc_dt_aware = datetime.datetime.now(datetime.timezone.utc).timestamp()
# print(utc_dt_aware)

# a = [{'nojs': 'JS10', 'site': 'ok'}, {'nojs': 'JS11', 'site': 'ok1'}]
# for x in a:
#     if x['nojs'] == 'JS11':
#         site = x
#         break

# test = next(x for x in a if x['nojs'] == 'JS11')
# print(test)

json = {
    "accumulate_energy.service": "active",
    "check_button.service": "active",
    "handle_canbus.service": "active",
    "handle_mosfet.service": "inactive",
    "handle_mosfet.timer": "active",
    "handle_relay.service": "inactive",
    "handle_relay.timer": "active",
    "keep_alive_dock.service": "active",
    "keep_alive_dock.timer": "active",
    "mppt.service": "active",
    "mppt_snmp.service": "inactive",
    "mppt_snmp.timer": "active",
    "store_log_data.service": "inactive",
    "store_log_data.timer": "active"
}
data = {
    "accumulate_energy_service": json["accumulate_energy.service"],
    "check_button_service": json["check_button.service"],
    "handle_canbus_service": json["handle_canbus.service"],
    "handle_mosfet_service": json["handle_mosfet.service"],
    "handle_mosfet_timer": json["handle_mosfet.timer"],
    "handle_relay_service": json["handle_relay.service"],
    "handle_relay_timer": json["handle_relay.timer"],
    "keep_alive_dock_service": json["keep_alive_dock.service"],
    "keep_alive_dock_timer": json["keep_alive_dock.timer"],
    "mppt_service": json["mppt.service"],
    "mppt_snmp_service": json["mppt_snmp.service"],
    "mppt_snmp_timer": json["mppt_snmp.timer"],
    "store_log_data_service": json["store_log_data.service"],
    "store_log_data_timer": json["store_log_data.timer"],
}
print(json)
print(data)
