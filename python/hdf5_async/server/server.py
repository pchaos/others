import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import asyncio
import h5py
import msgpack_numpy as m
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from common.serializers import get_serializer
import configparser
from common.config_manager import config_manager

m.patch()

class HDF5Server:
    def __init__(self, hdf5_file_path=None, host=None, port=None):
        self.hdf5_file_path = hdf5_file_path if hdf5_file_path is not None else config_manager.get('server', 'hdf5_file_path', fallback='my_async_hdf5_file.h5')

        self._host = host if host is not None else config_manager.get('server', 'host', fallback='127.0.0.1')
        self._port = port if port is not None else config_manager.getint('server', 'port', fallback=8888)
        self.use_compression = config_manager.getboolean('server', 'use_compression', fallback=False)
        print(f"Server initialized with host: {self._host}, port: {self._port}, compression: {self.use_compression}")

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
                index = request.get("index")

                response = {}
                if command == "get_config":
                    response = {"status": "success", 
                                "serialization_format": self.serializer.__class__.__name__.replace("Serializer", "").lower(),
                                "use_compression": self.use_compression}
                elif command == "create_group":
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
                elif command == "append":
                    await self._run_blocking_io(self._append_data, path, data)
                    response = {"status": "success", "message": f"Data appended to {path}"}
                elif command == "insert":
                    await self._run_blocking_io(self._insert_data, path, index, data)
                    response = {"status": "success", "message": f"Data inserted into {path} at index {index}"}
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
        with h5py.File(self.hdf5_file_path, 'a') as f:
            if path not in f:
                f.create_group(path)

    def _write_data(self, path, data):
        with h5py.File(self.hdf5_file_path, 'a') as f:
            if path in f:
                del f[path]
            
            is_serialized = False
            if isinstance(data, np.ndarray) and (data.dtype.kind == 'U' or data.dtype.kind == 'S'):
                data = data.tolist()
            
            if not isinstance(data, (int, float, str, bytes, bool)) and not isinstance(data, np.ndarray):
                data = self.serializer.encode(data)
                is_serialized = True

            if is_serialized:
                if self.use_compression:
                    f.create_dataset(path, data=np.frombuffer(data, dtype=np.uint8), compression='gzip')
                else:
                    f.create_dataset(path, data=np.frombuffer(data, dtype=np.uint8))
            else:
                maxshape = None
                chunks = None
                if hasattr(data, 'shape'):
                    maxshape = (None,) + data.shape[1:]
                    chunks = True

                if self.use_compression and isinstance(data, (np.ndarray, list)):
                    f.create_dataset(path, data=data, compression='gzip', maxshape=maxshape, chunks=chunks)
                else:
                    f.create_dataset(path, data=data, maxshape=maxshape, chunks=chunks)

    def _read_data(self, path):
        with h5py.File(self.hdf5_file_path, 'r') as f:
            if path in f:
                dset = f[path]
                data = dset[()]

                # Decode bytes to string for individual elements or arrays
                if isinstance(data, bytes):
                    data = data.decode('utf-8')
                elif isinstance(data, np.ndarray):
                    if dset.dtype.kind in ('O', 'S', 'U'):
                        # Decode each element if it's bytes
                        data = [item.decode('utf-8') if isinstance(item, bytes) else item for item in data.tolist()]
                    elif data.dtype == np.uint8:
                        # Handle serialized data
                        try:
                            decoded_data, _ = self.serializer.decode(data.tobytes())
                            data = decoded_data
                        except Exception:
                            pass # Keep as numpy array if deserialization fails
                return data
            return None

    def _delete_data(self, path):
        with h5py.File(self.hdf5_file_path, 'a') as f:
            if path in f:
                del f[path]

    def _append_data(self, path, data_to_append):
        with h5py.File(self.hdf5_file_path, 'a') as f:
            # --- 1. Normalize data_to_append to a list ---
            if isinstance(data_to_append, np.ndarray):
                append_list = data_to_append.tolist()
            elif isinstance(data_to_append, list):
                append_list = data_to_append
            else:  # Handles scalars (int, float, str, bytes)
                append_list = [data_to_append]

            # --- 2. Handle existing dataset ---
            if path in f and isinstance(f[path], h5py.Dataset):
                dset = f[path]
                
                # Read existing data and normalize to a list
                if dset.shape == ():
                    original_data = dset[()]
                    if isinstance(original_data, bytes):
                        original_list = [original_data.decode('utf-8')]
                    else:
                        original_list = [original_data]
                else:
                    original_list = dset[:].tolist()

                # Combine the lists
                new_data_list = original_list + append_list
                
                # Determine dtype for recreation
                is_string = any(isinstance(item, (str, bytes)) for item in new_data_list)
                
                del f[path]
                
                if is_string:
                    # Ensure all items are strings for h5py
                    new_data_list = [item.decode() if isinstance(item, bytes) else str(item) for item in new_data_list]
                    f.create_dataset(path, data=new_data_list, dtype=h5py.string_dtype(encoding='utf-8'), maxshape=(None,), chunks=True)
                else:
                    f.create_dataset(path, data=np.array(new_data_list), maxshape=(None,), chunks=True)

            # --- 3. Handle new dataset ---
            else:
                is_string = any(isinstance(item, (str, bytes)) for item in append_list)
                if is_string:
                    # Ensure all items are strings for h5py
                    new_data_list = [item.decode() if isinstance(item, bytes) else str(item) for item in append_list]
                    f.create_dataset(path, data=new_data_list, dtype=h5py.string_dtype(encoding='utf-8'), maxshape=(None,), chunks=True)
                else:
                    f.create_dataset(path, data=np.array(append_list), maxshape=(None,), chunks=True)

    def _insert_data(self, path, index, data_to_insert):
        with h5py.File(self.hdf5_file_path, 'a') as f:
            if path in f and isinstance(f[path], h5py.Dataset):
                dset = f[path]
                original_shape = dset.shape
                insert_len = len(data_to_insert)
                new_shape = (original_shape[0] + insert_len,) + original_shape[1:]
                dset.resize(new_shape)
                
                # Shift existing data to make space for new data
                dset[index + insert_len:] = dset[index:-insert_len]
                
                # Insert the new data
                dset[index:index + insert_len] = data_to_insert
            else:
                # If dataset doesn't exist, this is equivalent to a write operation
                self._write_data(path, data_to_insert)

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
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    doctest.testmod(verbose=True)