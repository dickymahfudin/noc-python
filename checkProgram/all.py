from helpers import time, checkStatusProgramSite, listJs, aiohttp, asyncio, headerSite


async def main():
    start = time.perf_counter()
    site = await listJs()
    if site["status"] == "success":
        print(f"\nRunning")
        for data in site["data"]:
            print(f"=> {data['nojs']} {data['site']}")
        print("\nProcessing...\nDon't turn off the application\n")

        async with aiohttp.ClientSession(headers=headerSite) as session:
            tasks = [checkStatusProgramSite(session, js)
                     for js in site["data"]]
            await asyncio.gather(*tasks)
    else:
        print("\nOpps, Nojs Not Found :)\nHappy Programming :)\n")

    elapsed = time.perf_counter() - start
    print(f"\nProgram completed in {elapsed:0.2f} seconds.")


def runAllCheck():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
