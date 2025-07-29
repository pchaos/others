
import asyncio
import signal
from server.server import HDF5Server

async def main():
    server = HDF5Server()
    loop = asyncio.get_running_loop()

    stop_event = asyncio.Event()

    def signal_handler():
        print("Ctrl+C detected. Shutting down server...")
        stop_event.set()

    loop.add_signal_handler(signal.SIGINT, signal_handler)

    try:
        # 启动服务器任务
        server_task = loop.create_task(server.start_server())
        # 等待停止事件被设置
        await stop_event.wait()
        # 取消服务器任务
        server_task.cancel()
        # 等待服务器任务完成取消
        await server_task
    except asyncio.CancelledError:
        print("Server task cancelled.")
    finally:
        print("Server shutdown complete.")

if __name__ == "__main__":
    asyncio.run(main())
