import inspect

from ..pointer import Pointer


class IncidentLib:
    """
    A class designed to create a dummy reflection of a given module or class.
    Instead of executing the real operations, the mirrored functions, methods,
    and attributes will provide details about their 'path' and received arguments.
    """

    def __init__(self, module, broker):
        """Initializes the mirror by setting up a set to track processed classes."""
        self._processed_classes = set()  # Used to avoid infinite recursion
        self.broker = broker
        self.variable_names = []
        self._mirror_module_or_class(module)  # Start the mirroring process

    def _mirror_module_or_class(self, obj, parent_path=""):
        """
        Recursively mirror the provided module or class.

        Args:
        - obj: The object (module or class) to be mirrored.
        - parent_path (str): Current path for the member being processed.
        """
        for name, member in inspect.getmembers(obj):
            current_path = f"{parent_path}.{name}" if parent_path else name

            # Check if it's a function or a method
            if (
                inspect.isfunction(member)
                or inspect.ismethod(member)
                or inspect.isbuiltin(member)
            ):
                vars(self)[name] = IncidentLib._create_dummy_method(
                    current_path,
                    self.broker,
                )
            # Check if member is a class and member not added in already processed classes
            elif inspect.isclass(member) and member not in self._processed_classes:
                self._processed_classes.add(member)
                dummy_class = self._create_dummy_class(member, current_path)
                vars(self)[name] = dummy_class
            # Check if Member is a variable
            elif not name.startswith("__"):  # and not inspect.ismodule(member):
                vars(self)["variable_names"].append(
                    name,
                )  # self.variable_names.append(name)

    def __getattr__(self, name):
        if name in self.variable_names:
            ptr = Pointer(path=name, broker=self.broker)
            self.broker.send(ptr)
            return ptr.obj_pointer()

    def _create_dummy_class(self, cls, parent_path):
        """
        Constructs and returns a dummy class that mirrors the original one.

        Args:
        - cls: The class to be mirrored.
        - parent_path (str): Current path for the member being processed.

        Returns:
        - DummyClass: The mirrored dummy class.
        """

        attrs = {}
        for name, member in inspect.getmembers(cls):
            current_path = f"{parent_path}.{name}"
            if inspect.isfunction(member) or inspect.ismethod(member):
                attrs[name] = self._create_dummy_method(current_path, self.broker)
            elif inspect.isclass(member) and member not in self._processed_classes:
                self._processed_classes.add(member)
                dummy_nested_class = self._create_dummy_class(member, current_path)
                attrs[name] = dummy_nested_class
            # elif not name.startswith("__") and not callable(member):
            #    attrs[name] = self._create_dummy_variable(current_path, self.broker)
        DummyClass = type(cls.__name__, (Pointer,), attrs)
        return DummyClass

    @staticmethod
    def _create_dummy_method(path, broker):
        """
        Constructs a dummy method that returns details about its path and arguments.

        Args:
        - path (str): Path for the dummy method.

        Returns:
        - Function: The dummy method.
        """

        def dummy_method(*args, **kwargs):
            fun_ptr = Pointer(
                path=path,
                args=args,
                kwargs=kwargs,
                broker=broker,
            )  # f"Path: {path}, Args: {args}, Kwargs: {kwargs}"
            broker.send(fun_ptr)
            return fun_ptr.obj_pointer()

        def dummy_init_method(self, *args, **kwargs):
            vars(self)["path"] = path
            vars(self)["args"] = args
            vars(self)["kwargs"] = kwargs
            vars(self)["broker"] = broker
            broker.send(self)
            return None

        method = path.split(".")[-1]
        if method == "__init__":
            return dummy_init_method
        else:
            return dummy_method

    @staticmethod
    def _create_dummy_variable(path, broker):
        """
        Constructs a dummy variable (as a callable) that provides its path and arguments.

        Args:
        - path (str): Path for the dummy variable.

        Returns:
        - Function: The dummy variable (callable).
        """
        var_ptr = Pointer(path=path, broker=broker)
        return var_ptr.obj_pointer()
