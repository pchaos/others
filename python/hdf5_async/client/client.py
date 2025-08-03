import asyncio
import numpy as np
from common.serializers import get_serializer, MessagePackSerializer
from common.config_manager import config_manager

class HDF5Client:
    def __init__(self, host=None, port=None):
        print("[CLIENT INIT]")
        self.host = host if host is not None else config_manager.get('server', 'host', fallback='127.0.0.1')
        self.port = port if port is not None else config_manager.getint('server', 'port', fallback=8888)
        self.reader = None
        self.writer = None
        self.serializer = MessagePackSerializer()  # Use a consistent serializer
        self.debug = False

    async def connect(self):
        print("[CLIENT CONNECT START]")
        try:
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
            server_config = await self._send_request("get_config")
            
            self.debug = server_config.get('debug', False)
            # The serializer can be updated based on server config if needed
            # For now, we stick to the default for consistency.
            
            if self.debug:
                print(f"Connected to HDF5 server at {self.host}:{self.port}")
                print(f"Received server config: {server_config}")
            print("[CLIENT CONNECT END]")

        except ConnectionRefusedError:
            print(f"Connection refused. Is the server running at {self.host}:{self.port}?")
            raise

    def is_connected(self):
        """Check if the client is connected."""
        return self.writer is not None and not self.writer.is_closing()

    def _log_debug(self, message):
        if self.debug:
            print(f"[DEBUG] {message}")

    async def _send_request(self, command, path=None, data=None, index=None, compression=None):
        if not self.writer:
            raise ConnectionError("Client is not connected to the server.")

        request = {
            "command": command,
            "path": path,
            "data": data,
            "index": index,
            "compression": compression,
        }
        
        print(f"[CLIENT SEND] {request}")
        self._log_debug(f"Sending request: {request}")

        message = self.serializer.encode(request)
        self.writer.write(message)
        await self.writer.drain()

        len_bytes = await self.reader.readexactly(4)
        message_len = int.from_bytes(len_bytes, 'big')
        response_data = await self.reader.readexactly(message_len)
        
        response, _ = self.serializer.decode(response_data)
        print(f"[CLIENT RECV] {response}")

        self._log_debug(f"Received response: {response}")

        if response.get("status") == "error":
            raise RuntimeError(f"Server error: {response.get('message')}")
        
        if command == "get_config":
            return response

        if response.get("status") == "not_found":
            return None
            
        return response.get("data")

    async def close(self):
        print("[CLIENT CLOSE]")
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
            if self.debug:
                print("Connection closed.")

    async def create_group(self, path):
        return await self._send_request("create_group", path)

    async def write(self, path, data, compression=None):
        return await self._send_request("write", path, data, compression=compression)

    async def read(self, path):
        return await self._send_request("read", path)

    async def update(self, path, data, compression=None):
        return await self._send_request("update", path, data, compression=compression)

    async def delete(self, path):
        return await self._send_request("delete", path)

    async def append(self, path, data, compression=None):
        return await self._send_request("append", path, data, compression=compression)

    async def insert(self, path, index, data, compression=None):
        return await self._send_request("insert", path, data=data, index=index, compression=compression)
