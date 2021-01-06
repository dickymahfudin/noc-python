import time
import asyncio
import aiohttp
from variable import headerSite, RASPI
from helpers import listJs, checkCapacitySite


async def main(port, temp):
    print("ok")
    start = time.perf_counter()
    site = await listJs(port)
    if site["status"] == "success":
        print(f"\n--- Check Capacity, All Site {temp} ---")
        print(f"\nRunning Raspi name {RASPI}")
        for data in site["data"]:
            print(f"=> {data['nojs']} {data['site']}")
        print("\nProcessing...\nDon't turn off the application\n")

        async with aiohttp.ClientSession(headers=headerSite) as session:
            tasks = [checkCapacitySite(port, session, js)
                     for js in site["data"]]
            await asyncio.gather(*tasks)
    else:
        print("\nOpps, Nojs Not Found :)\nHappy Programming :)\n")

    elapsed = time.perf_counter() - start
    print(f"\nProgram completed in {elapsed:0.2f} seconds.\n")


def runAllCapacity(port, temp):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(port, temp))
