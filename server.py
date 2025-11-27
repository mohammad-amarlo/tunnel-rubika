import asyncio
import websockets
import os

RUBIKA_WS = os.getenv("RUBIKA_WS")

async def handler(client_ws, _path):
    try:
        async with websockets.connect(RUBIKA_WS) as rubika_ws:
            async def c2r():
                async for msg in client_ws:
                    await rubika_ws.send(msg)
            async def r2c():
                async for msg in rubika_ws:
                    await client_ws.send(msg)
            await asyncio.gather(c2r(), r2c())
    except Exception as e:
        print("Error:", e)

async def main():
    port = int(os.getenv("PORT", 8000))
    async with websockets.serve(handler, "0.0.0.0", port):
        print("Tunnel server running on port", port)
        await asyncio.Future()

asyncio.run(main())
