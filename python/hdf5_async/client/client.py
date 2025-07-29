
import asyncio
import msgpack_numpy as m
import configparser
import os
from common.serializers import MessagePackSerializer, JsonSerializer

m.patch()

class HDF5Client:
    def __init__(self, host=None, port=None):
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')
        config.read(config_path)

        self.host = host if host is not None else config.get('server', 'host', fallback='127.0.0.1')
        self.port = port if port is not None else config.getint('server', 'port', fallback=8888)
        self.reader = None
        self.writer = None
        self.serializer = None # Will be set after getting config from server

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        print(f"Connected to HDF5 server at {self.host}:{self.port}")

        # Request configuration from the server
        config_response = await self._send_request("get_config", "/")
        if config_response.get("status") == "success":
            serialization_format = config_response.get("serialization_format")
            # Dynamically set serializer based on server config
            if serialization_format == 'json':
                from common.serializers import JsonSerializer
                self.serializer = JsonSerializer()
            elif serialization_format == 'messagepack':
                from common.serializers import MessagePackSerializer
                self.serializer = MessagePackSerializer()
            else:
                raise ValueError(f"Unknown serialization format from server: {serialization_format}")
            print(f"Received server config: serialization_format={serialization_format}")
        else:
            raise Exception(f"Failed to get server config: {config_response.get('message')}")

    async def _send_request(self, command, path, data=None):
        request = {
            "command": command,
            "path": path
        }
        if data is not None:
            request["data"] = data

        # Use a temporary serializer if self.serializer is not yet initialized
        if self.serializer is None:
            from common.serializers import MessagePackSerializer
            temp_serializer = MessagePackSerializer()
            message_bytes = temp_serializer.encode(request)
        else:
            message_bytes = self.serializer.encode(request)

        self.writer.write(message_bytes)
        await self.writer.drain()

        # Read response length
        len_bytes = await self.reader.readexactly(4)
        response_len = int.from_bytes(len_bytes, 'big')

        # Read response message
        response_message = await self.reader.readexactly(response_len)
        
        # Use a temporary serializer if self.serializer is not yet initialized
        if self.serializer is None:
            response, _ = temp_serializer.decode(len_bytes + response_message)
        else:
            response, _ = self.serializer.decode(len_bytes + response_message)
        return response

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

    async def close(self):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
            print("Connection closed.")

