import asyncio
import websockets

async def receive_messages(websocket, username):
    while True:
        try:
            message = await websocket.recv()
            if not message.startswith(f"{username}:"):
                print(message)
        except websockets.exceptions.ConnectionClosed:
            print("Disconnecting from the Server.")
            break

async def send_messages(websocket):
    while True:
        message = await asyncio.get_event_loop().run_in_executor(None, input)
        if message:
            await websocket.send(message)
            if message == "exit":
                break

async def main():
    ip = input("Input server IP: ")
    port = input("Input server Port: ")
    uri = f"ws://{ip}:{port}"

    async with websockets.connect(uri) as websocket:
        while True:
            name = input("Input a name to use: ")
            await websocket.send(name)
            response = await websocket.recv()
            if response == "Success":
                print(f"{name} Welcome to the chat room!")
                break
            else:
                print(response)

        receive_task = asyncio.create_task(receive_messages(websocket, name))
        send_task = asyncio.create_task(send_messages(websocket))

        await asyncio.gather(receive_task, send_task)

if __name__ == "__main__":
    asyncio.run(main())
