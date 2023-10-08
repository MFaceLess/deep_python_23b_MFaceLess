class CustomMeta(type):
    def __new__(cls, name, bases, dct):
        new_dct = {}

        for key, value in dct.items():
            if not key.startswith("__") and not key.endswith("__"):
                new_dct[f'custom_{key}'] = value
            else:
                new_dct[key] = value

        return super().__new__(cls, name, bases, new_dct)

    def __init__(cls, name, bases, classdict, **kwargs):
        cls.__setattr__ = cls.my_setattr
        super().__init__(name, bases, classdict, **kwargs)

    def my_setattr(cls, name, value):
        if not name.startswith("__") and not name.endswith("__"):
            return super().__setattr__(f'custom_{name}', value)
        return super().__setattr__(name, value)
