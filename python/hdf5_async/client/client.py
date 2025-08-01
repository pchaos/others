import asyncio
import numpy as np
from common.serializers import get_serializer
from common.config_manager import config_manager

class HDF5Client:
    def __init__(self, host=None, port=None):
        self.host = host if host is not None else config_manager.get('server', 'host', fallback='127.0.0.1')
        self.port = port if port is not None else config_manager.getint('server', 'port', fallback=8888)
        self.reader = None
        self.writer = None
        self.serializer = None
        self.debug = False # Default value

    async def connect(self):
        try:
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
            # The first request is to get the server's configuration
            server_config = await self._send_request("get_config")
            
            self.debug = server_config.get('debug', False)
            self.serializer = get_serializer()
            
            if self.debug:
                print(f"Connected to HDF5 server at {self.host}:{self.port}")
                print(f"Received server config: {server_config}")

        except ConnectionRefusedError:
            print(f"Connection refused. Is the server running at {self.host}:{self.port}?")
            raise

    def _log_debug(self, message):
        if self.debug:
            print(f"[DEBUG] {message}")

    async def _send_request(self, command, path=None, data=None, index=None):
        if not self.writer:
            raise ConnectionError("Client is not connected to the server.")

        request = {"command": command}
        if path:
            request["path"] = path
        if data is not None:
            request["data"] = data
        if index is not None:
            request["index"] = index
        
        self._log_debug(f"Sending request: {request}")

        # On the first connection, the serializer is not yet set
        if self.serializer:
            message = self.serializer.encode(request)
        else: # Fallback for the very first 'get_config' call
            from common.serializers import MessagePackSerializer
            message = MessagePackSerializer().encode(request)

        self.writer.write(message)
        await self.writer.drain()

        len_bytes = await self.reader.readexactly(4)
        message_len = int.from_bytes(len_bytes, 'big')
        response_data = await self.reader.readexactly(message_len)
        
        # The first response must be decoded with a default decoder
        if self.serializer:
            response, _ = self.serializer.decode(len_bytes + response_data)
        else:
            from common.serializers import MessagePackSerializer
            response, _ = MessagePackSerializer().decode(len_bytes + response_data)

        self._log_debug(f"Received response: {response}")

        if response.get("status") == "error":
            raise RuntimeError(f"Server error: {response.get('message')}")
        
        # The get_config command returns the full response, not just the 'data' field
        if command == "get_config":
            return response

        if response.get("status") == "not_found":
            return None
            
        return response.get("data")

    async def close(self):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
            if self.debug:
                print("Connection closed.")

    async def create_group(self, path):
        return await self._send_request("create_group", path)

    async def write(self, path, data):
        return await self._send_request("write", path, data)

    async def read(self, path):
        return await self._send_request("read", path)

    async def update(self, path, data):
        return await self._send_request("update", path, data)

    async def delete(self, path):
        return await self._send_request("delete", path)

    async def append(self, path, data):
        return await self._send_request("append", path, data)

    async def insert(self, path, index, data):
        return await self._send_request("insert", path, data=data, index=index)
