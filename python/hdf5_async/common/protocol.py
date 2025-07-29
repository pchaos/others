
import msgpack
import msgpack_numpy as m

m.patch()

def encode_message(message):
    message_bytes = msgpack.packb(message, use_bin_type=True)
    return len(message_bytes).to_bytes(4, 'big') + message_bytes

def decode_message(data):
    message_len = int.from_bytes(data[:4], 'big')
    message = msgpack.unpackb(data[4:4+message_len], raw=False)
    return message, data[4+message_len:]
