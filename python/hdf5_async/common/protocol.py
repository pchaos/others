
import json

def encode_message(message):
    message_bytes = json.dumps(message).encode('utf-8')
    return len(message_bytes).to_bytes(4, 'big') + message_bytes

def decode_message(data):
    message_len = int.from_bytes(data[:4], 'big')
    message = json.loads(data[4:4+message_len].decode('utf-8'))
    return message, data[4+message_len:]
