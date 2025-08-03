# tests/conftest.py
import asyncio
import os
import configparser
import pytest
import pytest_asyncio
from client.client import HDF5Client
from server.server import HDF5Server
from common.config_manager import config_manager

TEST_HDF5_FILE = "test_async_hdf5.h5"
TEST_CONFIG_FILE = "test_config.ini"

@pytest.fixture(scope="session", autouse=True)
def event_loop():
    """Create an instance of the default event loop for each test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session", autouse=True)
async def kill_existing_servers():
    """Ensure no orphaned server processes are running before tests."""
    try:
        # Use pgrep to find the PID of the server process directly
        proc = await asyncio.create_subprocess_shell(
            "pgrep -f 'run_server.py'",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=5.0)
        
        if proc.returncode == 0:
            pids = stdout.decode().strip().split('\n')
            pids = [pid for pid in pids if pid]
            if pids:
                print(f"Killing orphaned server processes: {pids}")
                kill_proc = await asyncio.create_subprocess_shell(f"kill -9 {' '.join(pids)}")
                await asyncio.wait_for(kill_proc.communicate(), timeout=5.0)
                await asyncio.sleep(0.5) # Give OS time to release ports
    except asyncio.TimeoutError:
        print("Warning: Timeout occurred while trying to kill existing server processes.")
    except Exception as e:
        print(f"An error occurred while killing existing servers: {e}")




@pytest_asyncio.fixture(scope="function")
async def hdf5_server():
    """
    Pytest fixture to set up and tear down the HDF5 server for a test module.
    """
    host = config_manager.get('server', 'host', fallback='127.0.0.1')
    server_instance = HDF5Server(hdf5_file_path=TEST_HDF5_FILE, host=host, port=0)
    
    await server_instance.start()
    
    assert server_instance.server is not None, "Server did not start correctly."
    actual_port = server_instance.server.sockets[0].getsockname()[1]
    
    server_task = asyncio.create_task(server_instance.serve_forever())
    
    try:
        yield server_instance, host, actual_port
    finally:
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass
        
        await server_instance.stop_server()
        
        if os.path.exists(TEST_HDF5_FILE):
            os.remove(TEST_HDF5_FILE)
        if os.path.exists(TEST_CONFIG_FILE):
            os.remove(TEST_CONFIG_FILE)

@pytest_asyncio.fixture
async def client(hdf5_server):
    """
    Pytest fixture to create and connect an HDF5Client for each test function.
    """
    _, host, port = hdf5_server
    client = HDF5Client(host=host, port=port)
    await client.connect()
    yield client
    await client.close()
