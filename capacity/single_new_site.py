import time
import asyncio
import aiohttp
from variable import headerSite, RASPI
from helpers import listJs, checkCapacitySite


async def main(nojs, port, temp):
    start = time.perf_counter()
    tempSite = await listJs(port)
    site = next(x for x in tempSite['data'] if x['nojs'] == nojs)
    print(f"\n--- Check Capacity {temp} ---")
    print(f"=> {site['nojs']} {site['site']}")
    print("\nProcessing...\nDon't turn off the application\n")

    async with aiohttp.ClientSession(headers=headerSite) as session:
        status = await asyncio.gather(checkCapacitySite(port, session, site))
        print(status)

    elapsed = time.perf_counter() - start
    print(f"\nProgram completed in {elapsed:0.2f} seconds.\n")


def runSingleCapacity(nojs, port, temp):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(nojs, port, temp))
