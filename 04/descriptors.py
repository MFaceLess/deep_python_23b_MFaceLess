class RussianBeginning:
    def __set_name__(self, owner, name):
        self.name = f'rus_descr_{name}'

    def __set__(self, obj, val):
        if obj is None:
            return None

        if not isinstance(val, str):
            raise ValueError("string notation required")

        if not val.startswith("e4 e5 kf3 kf6"):
            raise ValueError("wrong opening")

        return setattr(obj, self.name, val)

    def __get__(self, obj, objtype):
        if obj is None:
            return None

        return getattr(obj, self.name)


class SicilianDefense:
    def __set_name__(self, owner, name):
        self.name = f'sic_descr_{name}'

    def __set__(self, obj, val):
        if obj is None:
            return None

        if not isinstance(val, str):
            raise ValueError("string notation required")

        if not val.startswith("e4 c5"):
            raise ValueError("wrong opening")

        return setattr(obj, self.name, val)

    def __get__(self, obj, objtype):
        if obj is None:
            return None

        return getattr(obj, self.name)


class FrenchDefense:
    def __set_name__(self, owner, name):
        self.name = f'fr_descr_{name}'

    def __set__(self, obj, val):
        if obj is None:
            return None

        if not isinstance(val, str):
            raise ValueError("string notation required")

        if not val.startswith("e4 e6"):
            raise ValueError("wrong opening")

        return setattr(obj, self.name, val)

    def __get__(self, obj, objtype):
        if obj is None:
            return None

        return getattr(obj, self.name)


class ChessOpeningsPrepare:
    rus_opening = RussianBeginning()
    sicilian_opening = SicilianDefense()
    fr_opening = FrenchDefense()

    def __init__(self, rus_opening, sicilian_opening, fr_opening):
        self.rus_opening = rus_opening
        self.sicilian_opening = sicilian_opening
        self.fr_opening = fr_opening
