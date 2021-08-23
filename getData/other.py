import time
import aiohttp
import asyncio
import datetime
import json
from variable import headerSite, log_path

async def delother(data, site):
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

async def getOther(session, site):
    print(site)
    urlSite = f"http://{site['ip']}/api/logger"
    try:
        async with session.get(urlSite) as response:
            datas = await response.json()
            date = datetime.datetime.now().strftime("%d-%m-%Y") 
            if len(datas) != 0:
                f = open(f"{log_path}/{site['site']}-{date}.txt", "w+")
                f.write(json.dumps(datas))
                await delother(json, site)
    except:
        print("error")

async def main():
    sites=[{"site": "satap", "ip": "122.128.30.230:8081"}, {"site": "Kota", "ip": "122.128.30.142:8081"}]
    start = time.perf_counter()
    for data in sites:
        print(f"=> {data['site']} {data['ip']}")
    print("\nProcessing...\nDon't turn off the application\n")

    async with aiohttp.ClientSession(headers=headerSite) as session:
        tasks = [getOther(session, js)
                    for js in sites]
        await asyncio.gather(*tasks)

    elapsed = time.perf_counter() - start
    print(f"\nProgram completed in {elapsed:0.2f} seconds.\n")


def runOtherSite():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
