import uasyncio as asyncio

event = asyncio.Event()

async def producer():
    print("Producteur : je prépare quelque chose…")
    await asyncio.sleep(5)
    print("Producteur : événement déclenché !")
    event.set()

async def consumer():
    print("Consommateur : j'attends l'événement…")
    await event.wait()
    print("Consommateur : événement reçu !")

async def main():
    asyncio.create_task(consumer())
    await producer()

asyncio.run(main())
