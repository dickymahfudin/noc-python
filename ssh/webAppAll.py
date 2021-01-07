import time
import asyncio
from helpers import pushToSite, listJs
from variable import upload_path, DIR_HOME


async def main(port, temp):
    start = time.perf_counter()
    site = await listJs(port)
    file = f"{upload_path}/joulestore-web-app"
    to = DIR_HOME
    if site["status"] == "success":
        print(f"\n--- Update Program Webapp, All Site {temp} ---\n")
        for data in site["data"]:
            print(f"=> {data['nojs']} {data['site']}")
        print("\nProcessing...\nDon't turn off the application\n")
        print(f"dirr from => {file}")
        print(f"dirr to => {to}\n")

        for js in site['data']:
            pushToSite(js, file, to)
            print()

    else:
        print("\nOpps, Nojs Not Found :)\nHappy Programming :)\n")

    elapsed = time.perf_counter() - start
    print(f"\nProgram completed in {elapsed:0.2f} seconds.\n")


def webAppAll(port, temp):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(port, temp))
