try:
    import capnp

    from .capnp import *
except ImportError:
    # Handle the case where `some_package` or `mysubmodule` is not available
    pass
