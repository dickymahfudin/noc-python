from helpers import getDataSite, headerSite, listJs, asyncio, time, ceckProgramRunning, raspiId, VPN_NAME, updateQueue, aiohttp


async def main(nojs):
    start = time.perf_counter()
    tempSite = await listJs()
    site = next(x for x in tempSite['data'] if x['nojs'] == nojs)
    print(f"=> {site['nojs']} {site['site']}")
    async with aiohttp.ClientSession(headers=headerSite) as session:
        await asyncio.gather(getDataSite(session, site))

    elapsed = time.perf_counter() - start
    print(f"\nProgram completed in {elapsed:0.2f} seconds.")


def runSingle(nojs):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(nojs))
