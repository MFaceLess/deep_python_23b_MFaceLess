class CustomList(list):
    @staticmethod
    def sum_two_list(lst1, lst2):
        res = list(map(lambda val1, val2: val1 + val2, lst1, lst2))
        if len(lst1) > len(lst2):
            res += lst1[len(res):]
        else:
            res += lst2[len(res):]
        return CustomList(res)

    @staticmethod
    def sub_two_list(lst1, lst2):
        res = list(map(lambda val1, val2: val1 - val2, lst1, lst2))
        if len(lst1) > len(lst2):
            res += lst1[len(res):]
        else:
            res += [-elem for elem in lst2[len(res):]]
        return CustomList(res)

    def __add__(self, other):
        if not isinstance(other, (CustomList, list)):
            raise TypeError("Неподходящий тип")
        return self.sum_two_list(self, other)

    def __sub__(self, other):
        if not isinstance(other, (CustomList, list)):
            raise TypeError("Неподходящий тип")
        return self.sub_two_list(self, other)

    def __radd__(self, other):
        return self.sum_two_list(other, self)

    def __rsub__(self, other):
        return self.sub_two_list(other, self)

    def __eq__(self, other):
        return sum(self) == sum(other)

    def __ne__(self, other):
        return sum(self) != sum(other)

    def __gt__(self, other):
        return sum(self) > sum(other)

    def __ge__(self, other):
        return sum(self) >= sum(other)

    def __lt__(self, other):
        return sum(self) < sum(other)

    def __le__(self, other):
        return sum(self) <= sum(other)

    def __str__(self):
        return f'Элементы: {super().__str__()}, sum = {sum(self)}'

    def compare_two_lists(self, other):
        if len(self) != len(other):
            return False
        for i in range(len(self)):
            if self[i] != other[i]:
                return False
        return True
