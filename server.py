import os
import asyncio
import websockets

RUBIKA_WS = os.environ.get("RUBIKA_WS")

async def tunnel(ws, path):
    try:
        async with websockets.connect(RUBIKA_WS) as rubika_ws:
            async def ws_to_rubika():
                async for message in ws:
                    await rubika_ws.send(message)

            async def rubika_to_ws():
                async for message in rubika_ws:
                    await ws.send(message)

            await asyncio.gather(ws_to_rubika(), rubika_to_ws())

    except Exception as e:
        print("Tunnel error:", e)

async def main():
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting WebSocket tunnel on port {port}")
    async with websockets.serve(tunnel, "0.0.0.0", port):
        await asyncio.Future()

asyncio.run(main())
