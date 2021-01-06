import aiohttp
import asyncio
import time
import datetime
from variable import RASPI, BASE_URL, TOKEN_SITE

baseUrl = f"http://{BASE_URL}"
headerSite = {"Authorization": f"Bearer {TOKEN_SITE}"}
timeout = aiohttp.ClientTimeout(total=10000)


async def ceckProgramRunning(port):
    url = f"{baseUrl}:{port}/api/raspi"
    session = aiohttp.ClientSession()
    async with session.request('GET', url=url, params={"name": RASPI}) as response:
        result = await response.json()
        await session.close()
        return result["data"]


async def updateQueue(port, raspiId, status):
    url = f"{baseUrl}:{port}/api/raspi"
    session = aiohttp.ClientSession()
    async with session.request('PUT', url=f"{url}/{raspiId}", data={"status": status}) as response:
        await session.close()
        return await response.json()


async def listJs(port):
    try:
        url = f"{baseUrl}:{port}/api/nojs"
        session = aiohttp.ClientSession()
        async with session.request('GET', url=url, params={"site": RASPI}) as response:
            result = await response.json()
            await session.close()
            return result
    except:
        print('Internal Server Error')


async def delDataSite(data, site):
    try:
        for key in data:
            while (1):
                try:
                    urlSite = f"http://{site['ip']}/api/logger/{key['ts']}"
                    session = aiohttp.ClientSession(headers=headerSite)
                    async with session.request('DELETE', url=urlSite):
                        await session.close()
                        break
                except:
                    pass
    except:
        pass


async def pushDb(port, data, site, start):
    url = f"{baseUrl}:{port}/api/logger"
    timeout = aiohttp.ClientTimeout(total=10000)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.request('POST', url=url, json=data, timeout=timeout) as response:
            result = await response.json()
            await session.close()
            elapsed = time.perf_counter() - start
            if data["status"] == "success":
                await delDataSite(data["data"], site)
                print(
                    f"{data['nojs']} {site['site']}, {result['data']}  => {elapsed:0.2f} seconds")

            else:
                print(
                    f"{data['nojs']} {site['site']}, {result['data']} Value Error => {elapsed:0.2f} seconds")


async def getDataSite(port, session, site):
    urlSite = f"http://{site['ip']}/api/logger"
    startTime = time.perf_counter()
    try:
        async with session.get(urlSite) as response:
            json = await response.json()
            data = {
                "status": "success",
                "nojs": site["nojs"],
                "data": json
            }
            await pushDb(port, data, site, startTime)
    except:
        data = {
            "status": "error",
            "nojs": site["nojs"],
            "data": [
                {
                    "batt_volt": None,
                    "dock_active": None,
                    "cpu_temp": None,
                    "load1": None,
                    "load2": None,
                    "ts": datetime.datetime.now().strftime('%Y%m%dT%H%M%S%z')
                }
            ]
        }
        await pushDb(port, data, site, startTime)


async def pushDbProgramSite(port, data, site, start, status):
    url = f"{baseUrl}:{port}/api/statusprogram"
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.request('POST', url=url, json=data, timeout=timeout):
            await session.close()
            elapsed = time.perf_counter() - start
            if status == "success":
                print(
                    f"{site['nojs']} {site['site']}, => {elapsed:0.2f} seconds")
                return data

            else:
                print(
                    f"{site['nojs']} {site['site']}, Value Error => {elapsed:0.2f} seconds")
                return data


async def checkStatusProgramSite(port, session, site):
    urlSite = f"http://{site['ip']}/api/status/program"

    startTime = time.perf_counter()
    try:
        async with session.get(urlSite) as response:
            json = await response.json()
            data = {
                "nojs_id": site["id"],
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
            return await pushDbProgramSite(port, data, site, startTime, 'success')

    except:
        data = {
            "nojs_id": site["id"],
            "accumulate_energy_service": None,
            "check_button_service": None,
            "handle_canbus_service": None,
            "handle_mosfet_service": None,
            "handle_mosfet_timer": None,
            "handle_relay_service": None,
            "handle_relay_timer": None,
            "keep_alive_dock_service": None,
            "keep_alive_dock_timer": None,
            "mppt_service": None,
            "mppt_snmp_service": None,
            "mppt_snmp_timer": None,
            "store_log_data_service": None,
            "store_log_data_timer": None,
        }
        return await pushDbProgramSite(port, data, site, startTime, 'no')
