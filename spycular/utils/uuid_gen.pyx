# uuid_gen.pyx
from cpython cimport PyLong_FromLong
from libc.stdlib cimport RAND_MAX, rand, srand


cdef unsigned long long large_rand() nogil:
    """
    Generates an 80-bit random number using C-level rand function.
    """
    # Since RAND_MAX is platform dependent, usually being 2^31-1,
    # we may need multiple calls to rand() to produce an 80-bit number.
    return (
        <unsigned long long>rand() |
        (<unsigned long long>rand() << 15) |
        (<unsigned long long>rand() << 30) |
        (<unsigned long long>rand() << 45) |
        (<unsigned long long>rand() << 60)
    )

def generate_uuid():
    cdef unsigned long long rand_val = large_rand()

    return (
        f"{rand_val & 0xFFFF:04x}-"
        f"{(rand_val >> 16) & 0xFFFF:04x}-"
        f"{((rand_val >> 32) & 0x0FFF) | 0x4000:04x}-"
        f"{((rand_val >> 44) & 0x3FFF) | 0x8000:04x}-"
        f"{(rand_val >> 48) & 0xFFFFFFFFFFFF:012x}"
    )
