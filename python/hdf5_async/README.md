# HDF5 Async: Asynchronous HDF5 Client/Server

HDF5 Async provides a high-performance, asynchronous client-server framework for network-based access to HDF5 files. It is designed to solve the challenge of concurrent write access to a single HDF5 file from multiple processes or machines, a scenario that typically leads to file corruption or requires complex, slow locking mechanisms.

This project is ideal for distributed systems, such as data acquisition pipelines, scientific computing clusters, or parallel simulations, where multiple data sources need to stream results into a central HDF5 file efficiently and safely.

---

## Table of Contents

- [Core Features](#core-features)
- [System Architecture](#system-architecture)
  - [Server](#server)
  - [Client](#client)
  - [Serialization](#serialization)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Configuration (`config.ini`)](#configuration-configini)
- [Running the Server](#running-the-server)
- [Client API Usage](#client-api-usage)
  - [Connecting and Disconnecting](#connecting-and-disconnecting)
  - [API Reference](#api-reference)
  - [Code Examples](#code-examples)
- [Running Tests](#running-tests)
- [How to Contribute](#how-to-contribute)

---

## Core Features

- **Asynchronous I/O:** Built on Python's `asyncio` to handle thousands of concurrent client connections with minimal overhead.
- **Safe Concurrency:** A single server manages all file I/O, serializing write operations to prevent data corruption from simultaneous access.
- **Non-Blocking Architecture:** The server uses a `ThreadPoolExecutor` to delegate blocking HDF5 file operations, ensuring the main network event loop remains responsive.
- **Efficient Serialization:** Uses **MessagePack** for fast, compact, binary serialization. It includes robust, built-in support for complex **NumPy arrays** (including structured arrays), which are handled transparently.
- **Flexible Per-Operation Compression:** Clients can specify a compression algorithm (e.g., `gzip`, `lzf`) for each individual `write`, `update`, `append`, or `insert` operation. This allows for fine-grained control over the trade-off between storage space and write speed.
- **Rich Data Type Support:** Natively handles Python scalars (`int`, `float`, `str`), lists, and a wide variety of NumPy array dtypes.
- **Comprehensive API:** The client supports `create_group`, `read`, `write`, `update`, `delete`, `append`, and `insert` operations.

## System Architecture

The system consists of a central server that manages the HDF5 file and multiple clients that connect to it over the network.

### Server
The server (`server/server.py`) is the core of the application.
1.  It listens for TCP connections on a configurable host and port.
2.  It uses `asyncio` to manage client connections efficiently.
3.  When a request arrives, it is decoded using the `MessagePackSerializer`.
4.  Because HDF5 file I/O is inherently blocking, the server immediately offloads the file operation to a worker thread in a `ThreadPoolExecutor`.
5.  This prevents the main `asyncio` event loop from stalling, allowing the server to remain responsive to other clients while the file operation completes.
6.  Once the operation is done, the result is sent back to the client.

### Client
The client (`client/client.py`) provides a user-friendly, asynchronous API that abstracts away all network communication.
1.  It connects to the server and sends requests encoded with MessagePack.
2.  Methods like `write()`, `read()`, etc., are `async` functions, so they can be easily integrated into modern Python applications.
3.  It handles the encoding and decoding of data, including complex NumPy arrays, automatically.

### Serialization
Data is serialized using **MessagePack**, a binary format that is faster and more compact than JSON. We extend it with `msgpack-numpy`, which provides a highly efficient mechanism for serializing NumPy arrays, including their shape and data type. This ensures that what you send from the client is exactly what gets written to the HDF5 file and what you get back when you read it.

## Getting Started

### Prerequisites

- Python 3.8 or newer
- A C compiler (required by `h5py` for building its dependencies)
- The HDF5 C library (on Debian/Ubuntu, install with `sudo apt-get install libhdf5-dev`)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/phaos/hdf5_async.git
    cd hdf5_async
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration (`config.ini`)

The behavior of the server and client is controlled by `config.ini`.

```ini
[server]
host = 0.0.0.0
port = 8888
hdf5_file_path = data.h5
use_compression = false
debug = false
serialization_format = messagepack

[client]
# This section is for client-specific settings if any were needed.
# Currently, the client reads the [server] section for connection info.
```

**Server Settings:**

| Key | Description | Default |
| :--- | :--- | :--- |
| `host` | The IP address for the server to listen on. `0.0.0.0` listens on all available interfaces. | `0.0.0.0` |
| `port` | The port for the server to listen on. | `8888` |
| `hdf5_file_path` | The path to the HDF5 file the server will manage. | `data.h5` |
| `use_compression`| The default compression to use if a client does not specify one. Set to `true` to enable `gzip` by default. | `false` |
| `debug` | If `true`, enables verbose logging on the server and client. | `false` |
| `serialization_format` | The serialization format to use. `messagepack` is recommended. | `messagepack`|

## Running the Server

To start the server, run the `run_server.py` script from the project's root directory:

```bash
python run_server.py
```

The server will start and listen for connections based on the settings in `config.ini`.

## Client API Usage

### Connecting and Disconnecting

All interactions must be wrapped in a `connect()` and `close()` block.

```python
import asyncio
from client.client import HDF5Client

async def main():
    client = HDF5Client()
    await client.connect()
    try:
        # ... perform operations here ...
        pass
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### API Reference

All methods are `async` and must be awaited.

- `client.create_group(path: str)`
  Creates a new group at the specified path if it doesn't exist.

- `client.write(path: str, data, compression: str = None)`
  Writes data to a dataset at `path`. If the dataset exists, it is overwritten.
  - `data`: Can be a scalar, list, or NumPy array.
  - `compression`: Optional. Can be `'gzip'`, `'lzf'`, or `None`. If `None`, the server's default is used.

- `client.read(path: str)`
  Reads and returns the data from the dataset at `path`. Decompression is handled automatically by the server.

- `client.update(path: str, data, compression: str = None)`
  An alias for `write`. Overwrites the dataset at `path`.

- `client.append(path: str, data, compression: str = None)`
  Appends data to an existing dataset along the first axis. If the dataset doesn't exist, it is created.
  - `compression` is only applied if the dataset is being created for the first time.

- `client.insert(path: str, index: int, data, compression: str = None)`
  Inserts data into an existing dataset at a specific `index` along the first axis. This is an expensive operation as it requires a full rewrite of the dataset.
  - `compression` is applied to the newly rewritten dataset.

- `client.delete(path: str)`
  Deletes the group or dataset at the specified path.

### Code Examples

**Example 1: Basic Operations**
```python
import asyncio
import numpy as np
from client.client import HDF5Client

async def main():
    client = HDF5Client()
    await client.connect()
    try:
        await client.create_group("/my_group")
        data_to_write = np.array([1, 2, 3, 4, 5])
        await client.write("/my_group/my_dataset", data_to_write)
        read_data = await client.read("/my_group/my_dataset")
        print(f"Read data: {read_data}")
    finally:
        await client.close()

asyncio.run(main())
```

**Example 2: Using Compression**
```python
import asyncio
import numpy as np
from client.client import HDF5Client

async def main():
    client = HDF5Client()
    await client.connect()
    try:
        # Write large data with gzip compression
        large_data = np.random.rand(1000)
        await client.write("/my_group/compressed_data", large_data, compression="gzip")
        print("Wrote data with compression.")

        # Write small data without compression
        small_data = np.array([1, 2, 3])
        await client.write("/my_group/uncompressed_data", small_data, compression=None)
        print("Wrote data without compression.")

        # Decompression is automatic on read
        read_compressed = await client.read("/my_group/compressed_data")
        print(f"Successfully read compressed data of shape: {read_compressed.shape}")
    finally:
        await client.close()

asyncio.run(main())
```

## Running Tests

To run the integration tests, ensure the server is **not** running, then execute `pytest` from the project root:

```bash
pytest
```

The test suite automatically manages starting and stopping a server instance for its tests.

## How to Contribute

Contributions are welcome! If you have ideas for improvements, new features, or find any issues, please feel free to open an issue or submit a pull request.