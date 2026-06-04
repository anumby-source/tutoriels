import uasyncio as asyncio
import time

tick = asyncio.Event()

async def timer():
    while True:
        await asyncio.sleep(3.34)
        tick.set()

async def task():
    t0 = time.time()
    i = 0
    while i < 10:
        await tick.wait()
        tick.clear()
        print("Tick reçu ! #", i)        
        print(f"started at {time.time()-t0}")
        i += 1

async def main():
    asyncio.create_task(timer())
    await task()

asyncio.run(main())
