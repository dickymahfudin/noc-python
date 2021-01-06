import time
import aiohttp
import asyncio
from variable import PORT_NEW_SITE, headerSite
from helpers import ceckProgramRunning, listJs, updateQueue, RASPI, getDataSite


async def main(nojs):
    start = time.perf_counter()
    tempSite = await listJs(PORT_NEW_SITE)
    site = next(x for x in tempSite['data'] if x['nojs'] == nojs)
    print(f"\n--- Get Single Data V3 APT2 ---")
    print(f"\n=> {site['nojs']} {site['site']}")

    print("\nProcessing...\nDon't turn off the application\n")

    async with aiohttp.ClientSession(headers=headerSite) as session:
        await asyncio.gather(getDataSite(PORT_NEW_SITE, session, site))

    elapsed = time.perf_counter() - start
    print(f"\nProgram completed in {elapsed:0.2f} seconds.\n")


def runSingleNewSite(nojs):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(nojs))
