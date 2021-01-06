import time
import aiohttp
import asyncio
from variable import PORT_NEW_SITE, headerSite
from helpers import ceckProgramRunning, listJs, updateQueue, RASPI, getDataSite


async def main():
    start = time.perf_counter()
    status = await ceckProgramRunning(PORT_NEW_SITE)
    if status["status"] == False:
        raspiId = status["id"]
        site = await listJs(PORT_NEW_SITE)
        if site["status"] == "success":
            print(f"\n--- Get All Data V3 APT2 ---")
            print(f"\nRunning Raspi name {RASPI}")
            await updateQueue(PORT_NEW_SITE, raspiId, True)
            for data in site["data"]:
                print(f"=> {data['nojs']} {data['site']}")
            print("\nProcessing...\nDon't turn off the application\n")

            async with aiohttp.ClientSession(headers=headerSite) as session:
                tasks = [getDataSite(PORT_NEW_SITE, session, js)
                         for js in site["data"]]
                await asyncio.gather(*tasks)
                await updateQueue(PORT_NEW_SITE, raspiId, False)

        else:
            print("\nOpps, Nojs Not Found :)\n")

    else:
        print(f"\n--- Get All Data V3 APT2 ---")
        print(f"\nRunning Raspi name {RASPI}")
        print("\nOpps, The Program is Running\nHappy Programming :)\n")

    elapsed = time.perf_counter() - start
    print(f"\nProgram completed in {elapsed:0.2f} seconds.\n")


def runAllNewSite():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
