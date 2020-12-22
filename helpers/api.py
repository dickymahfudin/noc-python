import os
import aiohttp
import asyncio
import time
import datetime
from os.path import join, dirname
from dotenv import load_dotenv

print('\n')
# dotenv_path = join(dirname(__file__), '.env')
dotenv_path = join(os.getcwd(), '.env')
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