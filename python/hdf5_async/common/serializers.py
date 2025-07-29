
# common/serializers.py
import json
import msgpack
import msgpack_numpy as m
import configparser
import os

# --- NumPy anpassung für msgpack ---
m.patch()

# --- Abstrake Basisklasse für Serializer ---
class Serializer:
    def encode(self, data):
        raise NotImplementedError

    def decode(self, data):
        raise NotImplementedError

# --- Konkrete Implementierung für JSON ---
class JsonSerializer(Serializer):
    def encode(self, data):
        """
        Encodes data into a JSON byte string with a 4-byte length prefix.
        >>> serializer = JsonSerializer()
        >>> encoded_data = serializer.encode({"key": "value"})
        >>> len(encoded_data)
        20
        >>> encoded_data[4:].decode('utf-8')
        '{"key": "value"}'
        """
        # NumPy-Arrays müssen für JSON in Listen umgewandelt werden
        def default_encoder(obj):
            if hasattr(obj, 'tolist'):
                return obj.tolist()
            raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')
        
        message_bytes = json.dumps(data, default=default_encoder).encode('utf-8')
        return len(message_bytes).to_bytes(4, 'big') + message_bytes

    def decode(self, data):
        """
        Decodes a JSON byte string with a 4-byte length prefix.
        >>> serializer = JsonSerializer()
        >>> encoded_data = serializer.encode({"key": "value"})
        >>> decoded_message, remaining_data = serializer.decode(encoded_data)
        >>> decoded_message
        {'key': 'value'}
        >>> remaining_data
        b''
        """
        message_len = int.from_bytes(data[:4], 'big')
        message = json.loads(data[4:4+message_len].decode('utf-8'))
        return message, data[4+message_len:]

# --- Konkrete Implementierung für MessagePack ---
class MessagePackSerializer(Serializer):
    def encode(self, data):
        """
        Encodes data into a MessagePack byte string with a 4-byte length prefix.
        >>> serializer = MessagePackSerializer()
        >>> encoded_data = serializer.encode({"key": "value"})
        >>> len(encoded_data)
        15
        >>> import msgpack
        >>> msgpack.unpackb(encoded_data[4:], raw=False)
        {'key': 'value'}
        """
        message_bytes = msgpack.packb(data, use_bin_type=True)
        return len(message_bytes).to_bytes(4, 'big') + message_bytes

    def decode(self, data):
        """
        Decodes a MessagePack byte string with a 4-byte length prefix.
        >>> serializer = MessagePackSerializer()
        >>> encoded_data = serializer.encode({"key": "value"})
        >>> decoded_message, remaining_data = serializer.decode(encoded_data)
        >>> decoded_message
        {'key': 'value'}
        >>> remaining_data
        b''
        """
        message_len = int.from_bytes(data[:4], 'big')
        message = msgpack.unpackb(data[4:4+message_len], raw=False)
        return message, data[4+message_len:]

# --- Factory-Funktion ---
def get_serializer():
    """
    Liest die Konfigurationsdatei und gibt die entsprechende Serializer-Instanz zurück.
    """
    config = configparser.ConfigParser()
    # Der Pfad zur config.ini relativ zum aktuellen Skript
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')
    config.read(config_path)
    
    serialization_format = config.get('server', 'serialization_format', fallback='json').lower()
    
    if serialization_format == 'json':
        return JsonSerializer()
    elif serialization_format == 'messagepack':
        return MessagePackSerializer()
    else:
        raise ValueError(f"Unknown serialization format: {serialization_format}")

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

