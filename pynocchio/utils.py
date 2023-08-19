import hashlib
import random


def generate_uuid():
    # Generate random values for each section of a UUID
    parts = [
        random.randint(0, 0xFFFF),  # 4 hex digits
        random.randint(0, 0xFFFF),  # 4 hex digits
        random.randint(0, 0x0FFF) | 0x4000,  # 4 hex digits, version 4
        random.randint(0, 0x3FFF)
        | 0x8000,  # 4 hex digits, two most significant bits set to 10
        random.randint(0, 0xFFFFFFFFFFFF),  # 12 hex digits
    ]

    # Convert to a string and format as a UUID
    return "{:04x}-{:04x}-{:04x}-{:04x}-{:012x}".format(*parts)


def generate_uuid_from_string(input_string, namespace="puppet"):
    # Generate a SHA-1 hash
    hash_obj = hashlib.sha1(namespace.bytes + input_string.encode())
    hash_bytes = hash_obj.digest()

    # Convert the hash bytes to UUID format
    time_low = int.from_bytes(hash_bytes[0:4], byteorder="big")
    time_mid = int.from_bytes(hash_bytes[4:6], byteorder="big")
    time_hi_version = (
        int.from_bytes(hash_bytes[6:8], byteorder="big") & 0x0FFF
    ) | (5 << 12)
    clock_seq_hi_variant = (hash_bytes[8] & 0x3F) | 0x80
    clock_seq_low = hash_bytes[9]
    node = int.from_bytes(hash_bytes[10:], byteorder="big")

    # Return formatted UUID string
    return f"{time_low:08x}-\
        {time_mid:04x}-{time_hi_version:04x}-\
        {clock_seq_hi_variant:02x}{clock_seq_low:02x}-\
        {node:012x}"
