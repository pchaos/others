
import asyncio
import signal
from server.server import HDF5Server

async def main():
    server = HDF5Server()
    server_task = asyncio.create_task(server.start_server())

    # Keep the server running until interrupted
    try:
        await server_task
    except asyncio.CancelledError:
        print("Server task cancelled.")
    finally:
        await server.stop_server()
        print("Server shutdown complete.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    main_task = loop.create_task(main())

    try:
        loop.run_until_complete(main_task)
    except KeyboardInterrupt:
        print("\nCtrl+C detected. Shutting down server...")
        main_task.cancel()
        # Wait for the main_task to complete its cancellation
        loop.run_until_complete(main_task)
    finally:
        loop.close()
