import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import asyncio
import h5py
import numpy as np
import msgpack
from concurrent.futures import ThreadPoolExecutor
from common.serializers import get_serializer
from common.config_manager import config_manager

class HDF5Server:
    def __init__(self, hdf5_file_path=None, host=None, port=None):
        print("[SERVER INIT]")
        self.hdf5_file_path = hdf5_file_path or config_manager.get('server', 'hdf5_file_path')
        self._host = host or config_manager.get('server', 'host')
        self._port = port if port is not None else config_manager.getint('server', 'port')
        self.use_compression = config_manager.getboolean('server', 'use_compression')
        self.debug = config_manager.getboolean('server', 'debug')
        
        if self.debug:
            print(f"Server starting with config: host={self._host}, port={self._port}, compression={self.use_compression}, debug={self.debug}")
        
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.serializer = get_serializer()
        self.server = None
        self.client_tasks = set()

    def _log_debug(self, message):
        if self.debug:
            print(f"[DEBUG] {message}")

    async def _handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        self._log_debug(f"Client connected from {addr}")
        print(f"[SERVER HANDLE_CLIENT START] from {addr}")
        task = asyncio.current_task()
        self.client_tasks.add(task)
        
        try:
            while True:
                command = None
                try:
                    len_bytes = await reader.readexactly(4)
                    message_len = int.from_bytes(len_bytes, 'big')
                    message_data = await reader.readexactly(message_len)
                    
                    request, _ = self.serializer.decode(message_data)
                    print(f"[SERVER RECV] {request}")

                    command = request.get("command")
                    path = request.get("path")
                    data = request.get("data")
                    index = request.get("index")
                    compression = request.get("compression")

                    log_info = {"command": command, "path": path, "data_type": str(type(data))}
                    if isinstance(data, np.ndarray):
                        log_info["data_shape"] = data.shape
                        log_info["data_dtype"] = str(data.dtype)
                    if index is not None:
                        log_info["index"] = index
                    if compression is not None:
                        log_info["compression"] = compression
                    self._log_debug(f"Client {addr} request: {log_info}")

                    response = {}
                    if command == "get_config":
                        response = {
                            "status": "success", 
                            "serialization_format": config_manager.get('server', 'serialization_format'),
                            "use_compression": self.use_compression,
                            "debug": self.debug
                        }
                    elif command == "create_group":
                        await self._run_blocking_io(self._create_group, path)
                        response = {"status": "success"}
                    elif command == "write":
                        await self._run_blocking_io(self._write_data, path, data, compression)
                        response = {"status": "success"}
                    elif command == "read":
                        found, read_data = await self._run_blocking_io(self._read_data, path)
                        response = {"status": "success", "data": read_data} if found else {"status": "not_found"}
                    elif command == "update":
                        await self._run_blocking_io(self._write_data, path, data, compression)
                        response = {"status": "success"}
                    elif command == "delete":
                        await self._run_blocking_io(self._delete_data, path)
                        response = {"status": "success"}
                    elif command == "append":
                        await self._run_blocking_io(self._append_data, path, data, compression)
                        response = {"status": "success"}
                    elif command == "insert":
                        await self._run_blocking_io(self._insert_data, path, index, data, compression)
                        response = {"status": "success"}
                    else:
                        response = {"status": "error", "message": "Unknown command"}

                    print(f"[SERVER SEND] {response}")
                    response_message = self.serializer.encode(response)
                    writer.write(response_message)
                    await writer.drain()
                except asyncio.IncompleteReadError:
                    self._log_debug(f"Client {addr} disconnected.")
                    break
                except Exception as e:
                    print(f"Error handling client {addr} for command '{command}': {e}")
                    error_response = self.serializer.encode({"status": "error", "message": str(e)})
                    writer.write(error_response)
                    await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()
            self.client_tasks.remove(task)
            self._log_debug(f"Client task for {addr} removed.")
            print(f"[SERVER HANDLE_CLIENT END] from {addr}")

    async def _run_blocking_io(self, func, *args, **kwargs):
        return await asyncio.get_event_loop().run_in_executor(self.executor, func, *args, **kwargs)

    def _create_group(self, path):
        with h5py.File(self.hdf5_file_path, 'a') as f:
            if path not in f:
                f.create_group(path)

    def _write_data(self, path, data, compression=None):
        with h5py.File(self.hdf5_file_path, 'a') as f:
            if path in f:
                del f[path]

            original_data = data
            is_scalar = isinstance(data, (int, float, str, bytes))

            if is_scalar:
                if isinstance(data, str):
                    data = np.array([data.encode('utf-8')])
                else:
                    data = np.array([data])
            elif isinstance(data, list):
                try:
                    data = np.array(data)
                except (TypeError, ValueError):
                    serialized_data = self.serializer.encode(original_data)
                    f.create_dataset(path, data=np.frombuffer(serialized_data, dtype=np.uint8))
                    return

            if isinstance(data, np.ndarray):
                dt = data.dtype
                if dt.kind == 'U':
                    data = data.astype(h5py.string_dtype(encoding='utf-8'))
                    dt = data.dtype
                elif h5py.check_string_dtype(dt) or dt.kind == 'S':
                    dt = h5py.string_dtype(encoding='utf-8')
                
                maxshape = (None,) + data.shape[1:] if data.ndim > 0 else (None,)
                
                # Determine compression
                comp_to_use = compression
                if comp_to_use is None and self.use_compression:
                    comp_to_use = 'gzip' # Default compression
                
                f.create_dataset(path, data=data, dtype=dt, chunks=True, maxshape=maxshape, compression=comp_to_use)
            else:
                f.create_dataset(path, data=original_data)

    def _read_data(self, path):
        with h5py.File(self.hdf5_file_path, 'r') as f:
            if path not in f:
                return (False, None)
            dset = f[path]
            data = dset[()]
            
            if data.dtype.names:
                descr = []
                for name in data.dtype.names:
                    dt = data.dtype[name]
                    if dt.kind == 'S':
                        descr.append((name, f'S{dt.itemsize}'))
                    else:
                        descr.append((name, dt.str))
                
                return (True, {
                    b'__ndarray__': data.tolist(),
                    b'dtype': descr,
                    b'shape': data.shape
                })

            if dset.dtype == np.uint8:
                try:
                    decoded_data, _ = self.serializer.decode(data.tobytes())
                    return (True, decoded_data)
                except Exception:
                    pass

            if h5py.check_string_dtype(dset.dtype):
                if isinstance(data, np.ndarray):
                    data = np.char.decode(data.astype(np.bytes_), 'utf-8')
                elif isinstance(data, bytes):
                    data = data.decode('utf-8')
            
            return (True, data)

    def _delete_data(self, path):
        with h5py.File(self.hdf5_file_path, 'a') as f:
            if path in f:
                del f[path]

    def _append_data(self, path, data_to_append, compression=None):
        with h5py.File(self.hdf5_file_path, 'a') as f:
            if path not in f:
                self._write_data(path, data_to_append, compression=compression)
                return
            
            dset = f[path]
            if not isinstance(data_to_append, (list, np.ndarray)):
                data_to_append = [data_to_append]
            
            if isinstance(data_to_append, list):
                data_to_append = np.array(data_to_append, dtype=dset.dtype)

            dset.resize(dset.shape[0] + data_to_append.shape[0], axis=0)
            dset[-data_to_append.shape[0]:] = data_to_append

    def _insert_data(self, path, index, data_to_insert, compression=None):
        with h5py.File(self.hdf5_file_path, 'a') as f:
            if path not in f:
                self._write_data(path, data_to_insert if isinstance(data_to_insert, list) else [data_to_insert], compression=compression)
                return

            current_data = list(f[path][()])
            
            if isinstance(data_to_insert, (list, np.ndarray)):
                elements_to_insert = list(data_to_insert)
            else:
                elements_to_insert = [data_to_insert]
            
            new_data = current_data[:index] + elements_to_insert + current_data[index:]
            
            del f[path]
            self._write_data(path, new_data, compression=compression)

    async def start(self):
        """Initializes the server and gets it ready to accept connections."""
        print("[SERVER START]")
        self.server = await asyncio.start_server(self._handle_client, self._host, self._port)
        addr = self.server.sockets[0].getsockname()
        print(f"Serving on {addr[0]}:{addr[1]}")

    def is_serving(self):
        """Check if the server is currently serving."""
        if self.server:
            return self.server.is_serving()
        return False

    async def serve_forever(self):
        """Starts accepting connections. This method runs forever."""
        if not self.server:
            raise RuntimeError("Server not started. Call start() before serving.")
        print("[SERVER SERVE_FOREVER]")
        await self.server.serve_forever()

    async def stop_server(self):
        if self.server:
            print("[SERVER STOP_SERVER]")
            self._log_debug("Stopping server...")
            for task in list(self.client_tasks):
                task.cancel()
            await asyncio.sleep(0)  # Allow cancellations to be processed
            
            self.server.close()
            await self.server.wait_closed()
            self.executor.shutdown(wait=True)
            self._log_debug("Server stopped.")

if __name__ == "__main__":
    server = HDF5Server()
    async def main():
        await server.start()
        await server.serve_forever()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        if server.debug:
            print("\nServer shutting down.")
        asyncio.run(server.stop_server())
        server.executor.shutdown(wait=True)
        if server.debug:
            print("Server shutdown complete.")