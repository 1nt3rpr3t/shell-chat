import argparse
import asyncio
import socket
import websockets

class ChatServer:
    def __init__(self):
        self.clients = {}

    async def register(self, websocket, name):
        if name in self.clients:
            return False
        self.clients[name] = websocket
        print(f"{name} has join!")
        return True

    async def unregister(self, name):
        del self.clients[name]
        await self.broadcast(f"{name} has leave...")
        print(f"{name} has leave...")

    async def broadcast(self, message):
        for client in self.clients.values():
            await client.send(message)

    async def handle_client(self, websocket, path):
        name = None
        try:
            while True:
                name = await websocket.recv()
                if await self.register(websocket, name):
                    await websocket.send("Success")
                    await self.broadcast(f"{name} has join!")
                    break
                else:
                    await websocket.send("This name already exists. Please enter a different name.")

            async for message in websocket:
                if message == "exit":
                    break
                await self.broadcast(f"{name}: {message}")
                print(f"{name}: {message}")
        except websockets.exceptions.ConnectionClosedError:
            print(f"{name} has leave...")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if name:
                await self.unregister(name)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

async def main(port):
    server = ChatServer()
    async with websockets.serve(server.handle_client, "0.0.0.0", port):
        print(f"It started with an {get_local_ip()}:{port}...")
        await asyncio.Future()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat server")
    parser.add_argument("--port", type=int, help="Input server Port: ")
    args = parser.parse_args()

    asyncio.run(main(args.port))
