try:
    import capnp  # noqa: F401

    from .capnp import *  # noqa: F401, F403
except ImportError:
    # Handle the case where `some_package` or `mysubmodule` is not available
    pass
