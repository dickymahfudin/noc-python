import time
import asyncio
from helpers import pushToSite, listJs
from variable import upload_path, DIR_HOME


async def main(nojs, port, temp):
    start = time.perf_counter()
    tempSite = await listJs(port)
    file = f"{upload_path}/joulestore-web-app"
    to = DIR_HOME
    site = next(x for x in tempSite['data'] if x['nojs'] == nojs)
    print(f"\n--- Update Program Webapp, Single {temp} ---\n")
    print(f"\n=> {site['nojs']} {site['site']}")

    print("\nProcessing...\nDon't turn off the application\n")
    pushToSite(site, file, to)

    elapsed = time.perf_counter() - start
    print(f"\nProgram completed in {elapsed:0.2f} seconds.\n")


def webAppSingle(nojs, port, temp):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(nojs, port, temp))
