# HDF5 Async

HDF5 Async is a Python-based client-server application that provides asynchronous access to HDF5 files over a network. It allows multiple clients to interact with a central HDF5 file concurrently, performing operations like reading, writing, creating datasets, and more, without blocking.

## Features

- **Asynchronous I/O:** Built on Python's `asyncio` library for high-performance, non-blocking network communication.
- **Centralized HDF5 Server:** A single server manages access to the HDF5 file, ensuring data integrity.
- **Threaded HDF5 Operations:** The server uses a `ThreadPoolExecutor` to handle blocking HDF5 file operations, preventing the event loop from being blocked.
- **Simple Protocol:** A custom JSON-based protocol is used for communication between the client and server.
- **Basic HDF5 Operations:** The client supports creating groups and datasets, reading, writing, updating, listing, and deleting data.

## Project Structure

```
hdf5_async/
├── client/
│   └── client.py         # Asynchronous client for interacting with the server
├── common/
│   └── protocol.py       # Defines the communication protocol
├── server/
│   └── server.py         # Asynchronous server for handling HDF5 operations
├── tests/
│   └── test_basic.py     # Basic integration tests for the client-server interaction
└── run_server.py         # Script to run the HDF5 server
```

## How It Works

### Server

The server (`server/server.py`) listens for client connections on a specified host and port. When a client connects, the server handles requests in an asynchronous loop. Each request from a client is processed by a dedicated handler function.

To avoid blocking the `asyncio` event loop, all HDF5 file operations (which are inherently blocking) are run in a separate thread using a `ThreadPoolExecutor`. This allows the server to handle many client connections concurrently and efficiently.

### Client

The client (`client/client.py`) provides a simple async API for interacting with the server. It establishes a connection and sends requests to perform HDF5 operations. It listens for responses from the server in a separate `asyncio` task, allowing it to send and receive data without blocking.

### Protocol

The communication protocol (`common/protocol.py`) is straightforward. Messages are JSON objects, prefixed with a 4-byte header indicating the message length. This allows for easy and reliable message framing over a stream.

## Getting Started

### Prerequisites

- Python 3.7+
- `h5py`
- `numpy`
- `pytest` and `pytest-asyncio` (for running tests)

You can install the dependencies with:

```bash
pip install h5py numpy pytest pytest-asyncio
```

### Running the Server

To start the HDF5 server, run the `run_server.py` script:

```bash
python run_server.py
```

The server will start and create an HDF5 file named `my_async_hdf5_file.h5` in the project's root directory.

### Using the Client

You can use the `HDF5Client` in your own asynchronous Python applications. Here is a simple example of how to use it:

```python
import asyncio
from client.client import HDF5Client

async def main():
    client = HDF5Client()
    await client.connect()

    try:
        # Create a group
        await client.create_group("/my_group")

        # Write data to a new dataset
        data_to_write = [1, 2, 3, 4, 5]
        await client.write("/my_group/my_dataset", data_to_write)

        # Read the data back
        response = await client.read("/my_group/my_dataset")
        read_data = response.get("data")
        print(f"Read data: {read_data}")

    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### Running Tests

To run the integration tests, make sure the server is **not** running, and then execute `pytest`:

```bash
pytest
```

The test suite will automatically start and stop the server as needed.

## How to Contribute

Contributions are welcome! If you have ideas for improvements or find any issues, feel free to open an issue or submit a pull request.
