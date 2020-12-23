import os
import aiohttp
import asyncio
import time
import datetime
from os.path import join, dirname
from dotenv import load_dotenv
from pathlib import Path

print('\n')
# dotenv_path = join(dirname(__file__), '.env')
dotenv_path = Path('.').resolve() / 'noc-python' / '.env'
# dotenv_path = "/home/ubuntu/noc-python/.env"
print(dotenv_path)
load_dotenv(dotenv_path)

BASE_URL = os.environ.get("BASE_URL")
PORT = os.environ.get("PORT")
VPN_NAME = os.environ.get("VPN_NAME")
TOKEN_SITE = os.environ.get("TOKEN_SITE")
baseUrl = f"http://{BASE_URL}:{PORT}"
raspiId = os.environ.get("RASPI_ID")
lc = os.environ.get("LC")

urlQueue = f"{baseUrl}/api/raspi"
urlJs = f"{baseUrl}/api/nojs"
urlLoggers = f"{baseUrl}/api/logger"
urlStatusProgram = f"{baseUrl}/api/statusprogram"
headerSite = {"Authorization": f"Bearer {TOKEN_SITE}"}
paramLc = {"lc": lc}
timeout = aiohttp.ClientTimeout(total=10000)


async def ceckProgramRunning():
    session = aiohttp.ClientSession()
    async with session.request('GET', url=urlQueue, params={"id": raspiId}) as response:
        result = await response.json()
        await session.close()
        return result["data"]


async def updateQueue(status):
    session = aiohttp.ClientSession()
    async with session.request('PUT', url=f"{urlQueue}/{raspiId}", data={"status": status}) as response:
        await session.close()
        return await response.json()


async def listJs():
    session = aiohttp.ClientSession()
    async with session.request('GET', url=urlJs, params=paramLc) as response:
        result = await response.json()
        await session.close()
        return result


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


async def pushDb(data, site, start):
    timeout = aiohttp.ClientTimeout(total=10000)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.request('POST', url=urlLoggers, json=data, timeout=timeout) as response:
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


async def getDataSite(session, site):
    # urlSite = f"{baseUrl}/{site['ip']}/api/logger"
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
            await pushDb(data, site, startTime)
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
        await pushDb(data, site, startTime)


async def pushDbProgramSite(data, site, start, status):
    timeout = aiohttp.ClientTimeout(total=10000)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.request('POST', url=urlStatusProgram, json=data, timeout=timeout) as response:
            await response.json()
            await session.close()
            elapsed = time.perf_counter() - start
            if status == "success":
                print(
                    f"{site['nojs']} {site['site']}, => {elapsed:0.2f} seconds")

            else:
                print(
                    f"{site['nojs']} {site['site']}, Value Error => {elapsed:0.2f} seconds")


async def checkStatusProgramSite(session, site):
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
            await pushDbProgramSite(data, site, startTime, 'success')
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
        await pushDbProgramSite(data, site, startTime, 'no')
