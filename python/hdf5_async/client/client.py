
import asyncio
import json

class HDF5Client:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None

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

        message = json.dumps(request).encode('utf-8')
        self.writer.write(len(message).to_bytes(4, 'big'))
        self.writer.write(message)
        await self.writer.drain()

        # Read response length
        len_bytes = await self.reader.readexactly(4)
        response_len = int.from_bytes(len_bytes, 'big')

        # Read response message
        response_message = await self.reader.readexactly(response_len)
        response = json.loads(response_message.decode('utf-8'))
        return response

    async def create_group(self, path):
        return await self._send_request("create_group", path)

    async def write(self, path, data):
        return await self._send_request("write", path, data)

    async def read(self, path):
        return await self._send_request("read", path)

    async def close(self):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
            print("Connection closed.")

