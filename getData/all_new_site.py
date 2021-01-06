import time
import aiohttp
import asyncio
from variable import headerSite
from helpers import ceckProgramRunning, listJs, updateQueue, RASPI, getDataSite


async def main(port, temp):
    start = time.perf_counter()
    status = await ceckProgramRunning(port)
    if status["status"] == False:
        raspiId = status["id"]
        site = await listJs(port)
        if site["status"] == "success":
            print(f"\n--- Get All Data V3 {temp} ---")
            print(f"\nRunning Raspi name {RASPI}")
            await updateQueue(port, raspiId, True)
            for data in site["data"]:
                print(f"=> {data['nojs']} {data['site']}")
            print("\nProcessing...\nDon't turn off the application\n")

            async with aiohttp.ClientSession(headers=headerSite) as session:
                tasks = [getDataSite(port, session, js)
                         for js in site["data"]]
                await asyncio.gather(*tasks)
                await updateQueue(port, raspiId, False)

        else:
            print("\nOpps, Nojs Not Found :)\n")

    else:
        print(f"\n--- Get All Data V3 {temp} ---")
        print(f"\nRunning Raspi name {RASPI}")
        print("\nOpps, The Program is Running\nHappy Programming :)\n")

    elapsed = time.perf_counter() - start
    print(f"\nProgram completed in {elapsed:0.2f} seconds.\n")


def runAllNewSite(port, temp):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(port, temp))
