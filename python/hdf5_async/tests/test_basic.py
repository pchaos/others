
import asyncio
import pytest
import os
import h5py
import configparser
import pytest_asyncio
import socket

from client.client import HDF5Client
from server.server import HDF5Server

# Define the HDF5 file path for testing
TEST_HDF5_FILE = "test_server_shutdown.h5"
TEST_CONFIG_FILE = "config.ini"

@pytest.fixture(scope="session", autouse=True)
async def kill_existing_servers():
    # Find and kill any existing run_server.py processes
    print("\nChecking for and terminating existing server processes...")
    process = await asyncio.create_subprocess_shell(
        "ps aux | grep run_server.py | grep -v grep | awk '{print $2}'",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    pids = stdout.decode().strip().split('\n')
    pids = [p for p in pids if p]

    if pids:
        print(f"Found existing server processes with PIDs: {pids}. Terminating...")
        for pid in pids:
            try:
                os.kill(int(pid), 9) # SIGKILL
                print(f"Killed PID {pid}")
            except OSError as e:
                print(f"Error killing PID {pid}: {e}")
        await asyncio.sleep(2) # Give time for ports to release
    else:
        print("No existing server processes found.")
    yield


@pytest.fixture(scope="module", autouse=True)
def setup_config_file():
    # Create a temporary config.ini for testing
    config = configparser.ConfigParser()
    config['server'] = {
        'shutdown_delay': '1',
        'serialization_format': 'json'  # Default to json for initial tests
    }
    with open(TEST_CONFIG_FILE, 'w') as f:
        config.write(f)
    yield
    # Clean up the config file after tests
    os.remove(TEST_CONFIG_FILE)

@pytest_asyncio.fixture(scope="module")
async def hdf5_server():
    # Ensure the test HDF5 file is clean before starting the server
    if os.path.exists(TEST_HDF5_FILE):
        os.remove(TEST_HDF5_FILE)

    server = HDF5Server(hdf5_file_path=TEST_HDF5_FILE, port=0)
    server_task = asyncio.create_task(server.start_server())
    
    # Wait for the server to start and get its actual address
    await asyncio.sleep(1) # Give server time to bind
    
    yield server, server.host, server.port
    
    # Clean up: stop the server and remove the HDF5 file
    await server.stop_server()
    await server_task # Ensure the task completes after stopping
    if os.path.exists(TEST_HDF5_FILE):
        os.remove(TEST_HDF5_FILE)

@pytest.mark.asyncio
async def test_json_serialization(hdf5_server):
    server_instance, host, port = hdf5_server
    # Ensure config is set to JSON
    config = configparser.ConfigParser()
    config.read(TEST_CONFIG_FILE)
    config['server']['serialization_format'] = 'json'
    with open(TEST_CONFIG_FILE, 'w') as f:
        config.write(f)
    
    # Reinitialize server to pick up new config (fixture will handle cleanup)
    # This is a bit hacky, ideally the server would reload config or be a function fixture
    # For now, we rely on the server fixture restarting for each test if needed, or manual restart
    # For this test, we assume the server is already running with the correct config from setup_config_file
    
    client = HDF5Client(host=host, port=port)
    await client.connect()
    
    try:
        path = "/json_test_group/data"
        data_to_write = {"key": "value", "number": 123, "list": [1, 2, 3]}
        await client.write(path, data_to_write)
        
        response = await client.read(path)
        read_data = response.get("data")
        
        assert response.get("status") == "success"
        assert read_data == data_to_write
        
    finally:
        await client.close()

@pytest.mark.asyncio
async def test_messagepack_serialization(hdf5_server):
    server_instance, host, port = hdf5_server
    # Ensure config is set to MessagePack
    config = configparser.ConfigParser()
    config.read(TEST_CONFIG_FILE)
    config['server']['serialization_format'] = 'messagepack'
    with open(TEST_CONFIG_FILE, 'w') as f:
        config.write(f)
    
    # Reinitialize server to pick up new config (fixture will handle cleanup)
    # For this test, we assume the server is already running with the correct config from setup_config_file
    
    client = HDF5Client(host=host, port=port)
    await client.connect()
    
    try:
        path = "/msgpack_test_group/data"
        data_to_write = {"binary_key": b"binary_value", "float": 3.14}
        await client.write(path, data_to_write)
        
        response = await client.read(path)
        read_data = response.get("data")
        
        assert response.get("status") == "success"
        assert read_data == data_to_write
        
    finally:
        await client.close()
