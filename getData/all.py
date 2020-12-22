from helpers import getDataSite, headerSite, listJs, asyncio, time, ceckProgramRunning, raspiId, VPN_NAME, updateQueue, aiohttp


async def main():
    start = time.perf_counter()
    status = await ceckProgramRunning()
    if status["status"] == False:
        site = await listJs()
        if site["status"] == "success":
            print(f"\nRunning Raspi id {raspiId} -> {VPN_NAME}")
            await updateQueue(True)
            for data in site["data"]:
                print(f"=> {data['nojs']} {data['site']}")
            print("\nProcessing...\nDon't turn off the application\n")

            async with aiohttp.ClientSession(headers=headerSite) as session:
                tasks = [getDataSite(session, js) for js in site["data"]]
                await asyncio.gather(*tasks)
                await updateQueue(False)
        else:
            print("\nOpps, Nojs Not Found :)\n")

    else:
        print("\nOpps, The Program is Running\nHappy Programming :)\n")

    elapsed = time.perf_counter() - start
    print(f"\nProgram completed in {elapsed:0.2f} seconds.")


def runAll():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
