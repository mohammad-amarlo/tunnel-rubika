import os
import asyncio
import websockets

RUBIKA_WS = os.environ.get("RUBIKA_WS")

async def handler(client, path):
    try:
        async with websockets.connect(RUBIKA_WS) as rubika:
            async def forward_to_rubika():
                async for message in client:
                    await rubika.send(message)

            async def forward_to_client():
                async for message in rubika:
                    await client.send(message)

            await asyncio.gather(forward_to_rubika(), forward_to_client())

    except Exception as e:
        print("Error:", e)

async def main():
    port = int(os.environ.get("PORT", 8080))
    print("Tunnel running on port", port)
    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future()

asyncio.run(main())
