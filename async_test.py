import asyncio
from datetime import datetime
def now():
    return datetime.now().strftime("%H:%M:%S")
async def cooking_pasta():
    print(f"{now()}cooking yummy pasta")
    await asyncio.sleep(3)
    print(f"{now()}pasta done")

async def making_tea():
    print(f"{now()}making chai")
    await asyncio.sleep(2)
    print(f"{now()}tea done")

async def main():
    task1=asyncio.create_task(cooking_pasta())
    task2=asyncio.create_task(making_tea())
    await task1
    await task2
asyncio.run(main())