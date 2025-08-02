import asyncio
from server.server import HDF5Server

async def main():
    server = HDF5Server()
    await server.start()
    try:
        await server.serve_forever()
    except asyncio.CancelledError:
        print("Server task cancelled.")
    finally:
        await server.stop_server()
        print("Server shutdown complete.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped by user.")
