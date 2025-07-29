
import asyncio
import msgpack_numpy as m
import configparser
import os
from common.serializers import get_serializer

m.patch()

class HDF5Client:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None
        self.serializer = get_serializer()

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        print(f"Connected to HDF5 server at {self.host}:{self.port}")

    async def _send_request(self, command, path, data=None):
        request = {
            "command": command,
            "path": path
        }
        if data is not None:
            request["data"] = data

        message_bytes = self.serializer.encode(request)
        self.writer.write(message_bytes)
        await self.writer.drain()

        # Read response length
        len_bytes = await self.reader.readexactly(4)
        response_len = int.from_bytes(len_bytes, 'big')

        # Read response message
        response_message = await self.reader.readexactly(response_len)
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

