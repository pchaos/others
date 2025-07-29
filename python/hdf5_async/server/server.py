
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import asyncio
import h5py
import msgpack_numpy as m
from concurrent.futures import ThreadPoolExecutor
from common.serializers import get_serializer
import configparser

m.patch()

class HDF5Server:
    def __init__(self, hdf5_file_path='my_async_hdf5_file.h5', host=None, port=None):
        self.hdf5_file_path = hdf5_file_path

        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')
        config.read(config_path)

        self._host = host if host is not None else config.get('server', 'host', fallback='127.0.0.1')
        self._port = port if port is not None else config.getint('server', 'port', fallback=8888)

        self.executor = ThreadPoolExecutor(max_workers=4) # For blocking HDF5 operations
        self.serializer = get_serializer()
        self.server = None # To store the server instance
        self.host = None # Actual host after binding
        self.port = None # Actual port after binding

    async def _handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Client connected from {addr}")

        try:
            while True:
                # Read message length
                len_bytes = await reader.readexactly(4)
                message_len = int.from_bytes(len_bytes, 'big')

                # Read message
                message_data = await reader.readexactly(message_len)
                request, _ = self.serializer.decode(len_bytes + message_data)

                command = request.get("command")
                path = request.get("path")
                data = request.get("data")

                response = {}
                if command == "create_group":
                    await self._run_blocking_io(self._create_group, path)
                    response = {"status": "success", "message": f"Group {path} created"}
                elif command == "write":
                    await self._run_blocking_io(self._write_data, path, data)
                    response = {"status": "success", "message": f"Data written to {path}"}
                elif command == "read":
                    read_data = await self._run_blocking_io(self._read_data, path)
                    response = {"status": "success", "data": read_data}
                elif command == "update":
                    await self._run_blocking_io(self._write_data, path, data)
                    response = {"status": "success", "message": f"Data updated at {path}"}
                elif command == "delete":
                    await self._run_blocking_io(self._delete_data, path)
                    response = {"status": "success", "message": f"Data deleted from {path}"}
                else:
                    response = {"status": "error", "message": "Unknown command"}

                response_message = self.serializer.encode(response)
                writer.write(response_message)
                await writer.drain()

        except asyncio.IncompleteReadError:
            print(f"Client {addr} disconnected.")
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
        finally:
            writer.close()
            await writer.wait_closed()

    async def _run_blocking_io(self, func, *args, **kwargs):
        return await asyncio.get_event_loop().run_in_executor(self.executor, func, *args, **kwargs)

    def _create_group(self, path):
        """
        Creates a group in the HDF5 file.
        >>> import os
        >>> test_file = "test_doctest.h5"
        >>> if os.path.exists(test_file): os.remove(test_file)
        >>> server = HDF5Server(hdf5_file_path=test_file, host="127.0.0.1", port=8888)
        >>> server._create_group("/test_group")
        >>> with h5py.File(test_file, 'r') as f:
        ...     "test_group" in f
        True
        >>> if os.path.exists(test_file): os.remove(test_file)
        """
        with h5py.File(self.hdf5_file_path, 'a') as f:
            if path not in f:
                f.create_group(path)

    def _write_data(self, path, data):
        """
        Writes data to the HDF5 file.
        >>> import os
        >>> import numpy as np
        >>> test_file = "test_doctest.h5"
        >>> if os.path.exists(test_file): os.remove(test_file)
        >>> server = HDF5Server(hdf5_file_path=test_file, host="127.0.0.1", port=8888)
        >>> server._write_data("/test_dataset", np.array([1, 2, 3]))
        >>> with h5py.File(test_file, 'r') as f:
        ...     np.array_equal(f["/test_dataset"][:], np.array([1, 2, 3]))
        True
        >>> if os.path.exists(test_file): os.remove(test_file)
        """
        with h5py.File(self.hdf5_file_path, 'a') as f:
            if path in f:
                del f[path] # Overwrite existing dataset
            f.create_dataset(path, data=data)

    def _read_data(self, path):
        """
        Reads data from the HDF5 file.
        >>> import os
        >>> import numpy as np
        >>> test_file = "test_doctest.h5"
        >>> if os.path.exists(test_file): os.remove(test_file)
        >>> server = HDF5Server(hdf5_file_path=test_file, host="127.0.0.1", port=8888)
        >>> server._write_data("/test_dataset", np.array([1, 2, 3]))
        >>> np.array_equal(server._read_data("/test_dataset"), np.array([1, 2, 3]))
        True
        >>> server._read_data("/non_existent_dataset") is None
        True
        >>> if os.path.exists(test_file): os.remove(test_file)
        """
        with h5py.File(self.hdf5_file_path, 'r') as f:
            if path in f:
                return f[path][()] # Return numpy array directly
            return None

    def _delete_data(self, path):
        """
        Deletes data from the HDF5 file.
        >>> import os
        >>> import numpy as np
        >>> test_file = "test_doctest.h5"
        >>> if os.path.exists(test_file): os.remove(test_file)
        >>> server = HDF5Server(hdf5_file_path=test_file, host="127.0.0.1", port=8888)
        >>> server._write_data("/test_dataset", np.array([1, 2, 3]))
        >>> with h5py.File(test_file, 'r') as f:
        ...     "test_dataset" in f
        True
        >>> server._delete_data("/test_dataset")
        >>> with h5py.File(test_file, 'r') as f:
        ...     "test_dataset" in f
        False
        >>> if os.path.exists(test_file): os.remove(test_file)
        """
        with h5py.File(self.hdf5_file_path, 'a') as f:
            if path in f:
                del f[path]

    async def start_server(self):
        server = await asyncio.start_server(
            self._handle_client, self._host, self._port)

        addr = server.sockets[0].getsockname()
        self.host = addr[0]
        self.port = addr[1]
        print(f"Serving on {self.host}:{self.port}")

        self.server = server
        async with self.server:
            await self.server.serve_forever()

    async def stop_server(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            print("Server stopped.")

if __name__ == "__main__":
    import doctest
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    doctest.testmod(verbose=True)

