import time
import asyncio
import aiohttp
from variable import PORT_NEW_SITE, headerSite, RASPI
from helpers import listJs, checkStatusProgramSite


async def main():
    print("ok")
    start = time.perf_counter()
    site = await listJs(PORT_NEW_SITE)
    if site["status"] == "success":
        print(f"\n--- Check Status Program, All Site APT2 ---")
        print(f"\nRunning Raspi name {RASPI}")
        for data in site["data"]:
            print(f"=> {data['nojs']} {data['site']}")
        print("\nProcessing...\nDon't turn off the application\n")

        async with aiohttp.ClientSession(headers=headerSite) as session:
            tasks = [checkStatusProgramSite(PORT_NEW_SITE, session, js)
                     for js in site["data"]]
            await asyncio.gather(*tasks)
    else:
        print("\nOpps, Nojs Not Found :)\nHappy Programming :)\n")

    elapsed = time.perf_counter() - start
    print(f"\nProgram completed in {elapsed:0.2f} seconds.\n")


def runAllCheckNew():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
