from random import randint


def generate_uuid():
    local_randint = randint

    # Generating a large random number
    large_rand = local_randint(0, (1 << 80) - 1)  # 80 bits should suffice

    parts = (
        f"{large_rand & 0xFFFF:04x}",
        f"{(large_rand >> 16) & 0xFFFF:04x}",
        f"{((large_rand >> 32) & 0x0FFF) | 0x4000:04x}",
        f"{((large_rand >> 44) & 0x3FFF) | 0x8000:04x}",
        f"{(large_rand >> 48) & 0xFFFFFFFFFFFF:012x}",
    )

    return "-".join(parts)
