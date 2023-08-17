from ..pointer import Pointer


class ReflectedLib:
    """
    A class designed to reverse the operation of LibraryMirror using the Pointer object.
    Given a Pointer object,
    it invokes the actual method or function from the original library
    or retrieves the actual variable.
    """

    def __init__(self, module):
        """Initializes the reverse mirror by keeping a reference to the original module."""
        self._original_module = module

    @staticmethod
    def action_call(instance_or_class, path, args, kwargs):
        """
        Access (and possibly call if it's a method) the original attribute or method
        on an object instance or class based on a provided path.

        Args:
        - instance_or_class: The object instance or class itself.
        - path (str): Dot-separated path to the attribute or method.
        - *args: Arguments to pass to the method (if applicable).
        - **kwargs: Keyword arguments to pass to the method (if applicable).

        Returns:
        - Result of the attribute access or method execution.
        """

        # Split the path and navigate through object or class attributes
        attributes = path.split(".")
        for attr in attributes[:-1]:
            instance_or_class = getattr(instance_or_class, attr)

        # Get the final attribute or method from the object/class
        result = getattr(instance_or_class, attributes[-1])

        # If the result is callable (i.e., a method), call it
        if callable(result):
            try:
                return result(*args, **kwargs)
            except Exception as e:
                return None
        else:
            return result

    def call_original(self, pointer: Pointer):
        """
        Calls the original method, function, or retrieves the variable based on the path and arguments
        present in the Pointer object.

        Args:
        - pointer (Pointer): The Pointer object which contains path and arguments details.

        Returns:
        - Result of the called method or function or the value of the variable.
        """
        obj = self._original_module
        attributes = pointer.path.split(".")

        for idx, attr in enumerate(attributes):
            obj = getattr(obj, attr)

            # If this attribute is "__init__", it implies we're instantiating a class
            if attr == "__init__":
                return obj(*pointer.args, **pointer.kwargs)

            # If we haven't reached the last attribute and the object is callable (class constructor),
            # we call it to get the instance. This handles the case for dummy classes.
            elif idx < len(attributes) - 1 and callable(obj):
                obj = obj()

        if callable(obj):
            return obj(*pointer.args, **pointer.kwargs)
        else:
            return obj
