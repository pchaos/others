import asyncio
import signal
import time
from server.server import HDF5Server
from common.config_manager import config_manager

class CtrlCHandler:
    def __init__(self, loop, main_task):
        self.loop = loop
        self.main_task = main_task
        self.debug_mode = config_manager.getboolean('server', 'debug', fallback=False)
        self.last_ctrl_c_time = 0
        self.shutdown_scheduled = False

    def __call__(self, signum, frame):
        if self.shutdown_scheduled:
            return

        if self.debug_mode:
            print("\nCtrl+C detected in debug mode. Shutting down server...")
            self.schedule_shutdown()
        else:
            current_time = time.time()
            if current_time - self.last_ctrl_c_time < 3:
                print("\nSecond Ctrl+C detected. Shutting down server...")
                self.schedule_shutdown()
            else:
                self.last_ctrl_c_time = current_time
                print("\nPress Ctrl+C again within 3 seconds to shut down.")

    def schedule_shutdown(self):
        self.shutdown_scheduled = True
        self.loop.call_soon_threadsafe(self.main_task.cancel)

async def main():
    server = HDF5Server()
    server_task = asyncio.create_task(server.start_server())

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

    # Setup Ctrl+C handler
    ctrl_c_handler = CtrlCHandler(loop, main_task)
    signal.signal(signal.SIGINT, ctrl_c_handler)

    try:
        loop.run_until_complete(main_task)
    except asyncio.CancelledError:
        # This is expected when the task is cancelled by the handler
        pass
    finally:
        # Ensure all tasks are cancelled before closing the loop
        tasks = asyncio.all_tasks(loop=loop)
        for task in tasks:
            task.cancel()
        
        # Gather all tasks to ensure they are finished cancelling
        async def gather_cancelled_tasks():
            await asyncio.gather(*tasks, return_exceptions=True)

        # Run the gathering task until it's complete
        loop.run_until_complete(gather_cancelled_tasks())
        
        loop.close()
        print("Event loop closed.")