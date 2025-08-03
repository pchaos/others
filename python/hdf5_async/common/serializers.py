
# common/serializers.py
import json
import msgpack
import msgpack_numpy as m
import numpy as np
from .config_manager import config_manager

# --- NumPy support for msgpack ---
m.patch()

# --- Abstract base class for Serializer ---
class Serializer:
    def encode(self, data):
        raise NotImplementedError

    def decode(self, data):
        raise NotImplementedError

# --- Concrete implementation for JSON ---
class JsonSerializer(Serializer):
    def encode(self, data):
        """
        Encodes data into a JSON byte string with a 4-byte length prefix.
        """
        def default_encoder(obj):
            if hasattr(obj, 'tolist'):
                return obj.tolist()
            raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')
        
        message_bytes = json.dumps(data, default=default_encoder).encode('utf-8')
        return len(message_bytes).to_bytes(4, 'big') + message_bytes

    def decode(self, data):
        """
        Decodes a JSON byte string with a 4-byte length prefix.
        """
        message_len = int.from_bytes(data[:4], 'big')
        message = json.loads(data[4:4+message_len].decode('utf-8'))
        return message, data[4+message_len:]

# --- Concrete implementation for MessagePack ---
class MessagePackSerializer(Serializer):
    def encode(self, data):
        """
        Encodes data into a MessagePack byte string with a 4-byte length prefix.
        """
        message_bytes = msgpack.packb(data, use_bin_type=True)
        return len(message_bytes).to_bytes(4, 'big') + message_bytes

    def decode(self, data):
        """
        Decodes a MessagePack byte string. Assumes the length prefix has already been handled.
        """
        def _object_hook(dct):
            if b'__ndarray__' in dct:
                shape = dct[b'shape']
                dtype_descr = dct[b'dtype']
                if isinstance(dtype_descr, list) and all(isinstance(i, list) for i in dtype_descr):
                    dtype_descr = [tuple(item) for item in dtype_descr]
                dtype = np.dtype(dtype_descr)
                data = dct[b'__ndarray__']
                
                if isinstance(data, list):
                    return np.array([tuple(row) for row in data], dtype=dtype)
                
                return np.frombuffer(data, dtype=dtype).reshape(shape)
            return dct

        message = msgpack.unpackb(data, object_hook=_object_hook, raw=False)
        return message, b''

# --- Factory function ---
def get_serializer():
    """
    Reads the configuration and returns the corresponding serializer instance.
    """
    serialization_format = config_manager.get('server', 'serialization_format', fallback='json').lower()
    
    if serialization_format == 'json':
        return JsonSerializer()
    elif serialization_format == 'messagepack':
        return MessagePackSerializer()
    else:
        raise ValueError(f"Unknown serialization format: {serialization_format}")

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

