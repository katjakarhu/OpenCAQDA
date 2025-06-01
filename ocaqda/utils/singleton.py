# Source: https://stackoverflow.com/a/63483209

class Singleton(type):
    # Inherit from "type" in order to gain access to method __call__
    def __init__(cls, *args, **kwargs):
        cls.__instance = None  # Create a variable to store the object reference
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            # if the object has not already been created
            cls.__instance = super().__call__(*args,
                                              **kwargs)  # Call the __init__ method of the subclass and save the reference
            return cls.__instance

        # if object reference already exists; return it
        return cls.__instance
