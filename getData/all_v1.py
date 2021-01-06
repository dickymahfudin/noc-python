import subprocess
import asyncio
import redis
import datetime
import time
import requests
import os
from ast import literal_eval
from variable import BASE_URL, PORT_100S_V1, TOKEN_100S_V1, RASPI

baseUrl = f"http://{BASE_URL}:{PORT_100S_V1}"

urlQueue = f"{baseUrl}/api/raspi"
urlJs = f"{baseUrl}/api/nojs"
urlLoggers = f"{baseUrl}/api/logger"
payload = {'noc': RASPI}
headers = {'Authorization': f"Bearer {TOKEN_100S_V1}"}


def ceckProgramRunning():
    data = {'name': RASPI}
    send = requests.get(urlQueue, headers=headers, params=data)
    datas = send.json()
    for x in datas:
        data = (x)

    return data


def updateData(datas):
    data = {'status': f'{datas["status"]}'}
    requests.put(
        f"{urlQueue}/{datas['id']}", headers=headers, data=data)


def listJS():
    send = requests.get(urlJs, headers=headers, params=payload)
    datas = send.json()

    return datas


async def deleteRedis(datas, redis):
    try:
        for key in datas:
            while (1):
                try:
                    # print(f"delete data {key}")
                    redis.hdel("data", key)
                    break
                except:
                    pass
    except:
        pass


async def storeData(datas):
    try:
        for data in datas["data"]:
            send = requests.post(urlLoggers, headers=headers, data=data)

        elapsed = time.perf_counter() - datas['time']
        if len(datas['tempRedis']) != 0:
            await deleteRedis(datas['tempRedis'], datas['redis'])
            return f"{datas['site']['nojs']} {datas['site']['site']}, {len(datas['tempRedis'])} Data => {elapsed:0.2f} seconds"
        else:
            return f"{datas['site']['nojs']} {datas['site']['site']}, {len(datas['tempRedis'])} Data => {elapsed:0.2f} seconds"

    except:
        elapsed = time.perf_counter() - datas['time']
        return f"{datas['site']['nojs']} {datas['site']['site']}, 1 Data Error Value => {elapsed:0.2f} seconds"


async def getPushData(site):
    errorValue = None
    red = redis.Redis(
        host=site["ip"],
        port=6379,
        db=0,
        password='9ff7b9d0-891b-4980-8559-6a67a76a73ac',
        socket_timeout=25
    )

    start = time.perf_counter()
    while(1):
        try:
            data = red.hgetall('data')
            datas = []
            tempRedis = []

            if len(data) != 0:
                for key, val in data.items():
                    # time_gathering = datetime.datetime.now()
                    time_stamp = str(key)[2:-1]
                    site_data = literal_eval(str(val)[2:-1])
                    # list_data = [i_data for i_data in site_data.values()]
                    time_local = f"{time_stamp[0:4]}-{time_stamp[4:6]}-{time_stamp[6:8]} {time_stamp[9:11]}:{time_stamp[11:13]}:{time_stamp[13:15]}"
                    edl1 = int(round(site_data["edl1"] / 10000000, 0))
                    edl2 = int(round(site_data["edl2"] / 10000000, 0))

                    try:
                        datas.append({
                            "time_local": time_local,
                            "nojs": site["nojs"],
                            "eh1": int(site_data["eh1"]) * 36,
                            "eh2": int(site_data["eh2"]) * 36,
                            "vsat_curr": int(site_data["load1"]),
                            "bts_curr": int(site_data["load2"]),
                            "load3": int(site_data["load3"]),
                            "batt_volt1": int(site_data["batt_volt1"]),
                            "batt_volt2": int(site_data["batt_volt2"]),
                            "edl1": edl1,
                            "edl2": edl2,
                            "pms_state": site_data["pms_state"]
                        })
                        tempRedis.append(key)

                    except:
                        pass
            break

        except:
            tempRedis = 0
            time_local = datetime.datetime.now()
            datas = [{
                "time_local": time_local.strftime("%Y-%m-%d %H:%M:%S"),
                "nojs": site["nojs"],
                "eh1": errorValue,
                "eh2": errorValue,
                "vsat_curr": errorValue,
                "bts_curr": errorValue,
                "load3": errorValue,
                "batt_volt1": errorValue,
                "batt_volt2": errorValue,
                "edl1": errorValue,
                "edl2": errorValue,
                "pms_state": errorValue
            }]
            break

    store = await storeData({
        "data": datas,
        "site": site,
        "tempRedis": tempRedis,
        "redis": red,
        "time": start
    })

    return store


async def main(site, status):
    updateData({
        "id": status["id"],
        "status": True
    })

    start = time.perf_counter()
    coroutines = [getPushData(data) for data in site]
    completed, pending = await asyncio.wait(coroutines)

    elapsed = time.perf_counter() - start

    for item in completed:
        print(item.result())

    updateData({
        "id": status["id"],
        "status": False
    })

    print(f"\nProgram completed in {elapsed:0.2f} seconds.\n")


def runAllV1():
    start = time.perf_counter()
    status = ceckProgramRunning()
    if status["status"] == False:
        site = listJS()
        print(f"\n--- Get All Data V1 100 Site ---")
        print(f"\nRunning Raspi name {RASPI}")
        for data in site:
            print(f"=> {data['nojs']} {data['site']}")
        print("\nProcessing...\nDon't turn off the application\n")

        event_loop = asyncio.get_event_loop()
        try:
            event_loop.run_until_complete(main(site, status))
        finally:
            event_loop.close()
    else:
        print(f"\n--- Get All Data V1 100 Site ---")
        print(f"\nRunning Raspi name {RASPI}")
        print("\nOpps, The Program is Running\nHappy Programming :)\n")
        elapsed = time.perf_counter() - start
        print(f"\nProgram completed in {elapsed:0.2f} seconds.\n")


if __name__ == '__main__':
    runAllV1()
