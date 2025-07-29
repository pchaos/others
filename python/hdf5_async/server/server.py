
import asyncio
import h5py
import msgpack
import msgpack_numpy as m
from concurrent.futures import ThreadPoolExecutor

m.patch()

class HDF5Server:
    def __init__(self, hdf5_file_path='my_async_hdf5_file.h5', host='127.0.0.1', port=8888):
        self.hdf5_file_path = hdf5_file_path
        self.host = host
        self.port = port
        self.executor = ThreadPoolExecutor(max_workers=4) # For blocking HDF5 operations

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
                request = msgpack.unpackb(message_data, raw=False)

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

                response_message = msgpack.packb(response, use_bin_type=True)
                writer.write(len(response_message).to_bytes(4, 'big'))
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
                del f[path] # Overwrite existing dataset
            f.create_dataset(path, data=data)

    def _read_data(self, path):
        with h5py.File(self.hdf5_file_path, 'r') as f:
            if path in f:
                return f[path][()] # Return numpy array directly
            return None

    def _delete_data(self, path):
        with h5py.File(self.hdf5_file_path, 'a') as f:
            if path in f:
                del f[path]

    async def start_server(self):
        server = await asyncio.start_server(
            self._handle_client, self.host, self.port)

        addr = server.sockets[0].getsockname()
        print(f"Serving on {addr}")

        async with server:
            await server.serve_forever()

