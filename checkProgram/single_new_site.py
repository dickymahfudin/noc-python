import time
import asyncio
import aiohttp
from variable import PORT_NEW_SITE, headerSite, RASPI
from helpers import listJs, checkStatusProgramSite


async def main(nojs):
    start = time.perf_counter()
    tempSite = await listJs(PORT_NEW_SITE)
    site = next(x for x in tempSite['data'] if x['nojs'] == nojs)
    print(f"\n--- Check Status Program APT2 ---")
    print(f"=> {site['nojs']} {site['site']}")
    print("\nProcessing...\nDon't turn off the application\n")

    async with aiohttp.ClientSession(headers=headerSite) as session:
        status = await asyncio.gather(checkStatusProgramSite(PORT_NEW_SITE, session, site))
        print(status)

    elapsed = time.perf_counter() - start
    print(f"\nProgram completed in {elapsed:0.2f} seconds.\n")


def runSingleChechNew(nojs):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(nojs))
