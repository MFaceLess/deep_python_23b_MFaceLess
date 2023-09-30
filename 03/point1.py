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

    def __init__(self, init_lst):
        super().__init__()
        self.lst = init_lst.copy()

    def __add__(self, other):
        if isinstance(other, CustomList):
            return self.sum_two_list(self.lst, other.lst)
        if isinstance(other, list):
            return self.sum_two_list(self.lst, other)
        raise TypeError("Неподходящий тип")

    def __sub__(self, other):
        if isinstance(other, CustomList):
            return self.sub_two_list(self.lst, other.lst)
        if isinstance(other, list):
            return self.sub_two_list(self.lst, other)
        raise TypeError("Неподходящий тип")

    def __radd__(self, other):
        return self.sum_two_list(other, self.lst)

    def __rsub__(self, other):
        return self.sub_two_list(other, self.lst)

    def __eq__(self, other):
        return sum(self.lst) == sum(other.lst)

    def __ne__(self, other):
        return sum(self.lst) != sum(other.lst)

    def __gt__(self, other):
        return sum(self.lst) > sum(other.lst)

    def __ge__(self, other):
        return sum(self.lst) >= sum(other.lst)

    def __lt__(self, other):
        return sum(self.lst) < sum(other.lst)

    def __le__(self, other):
        return sum(self.lst) <= sum(other.lst)

    def __str__(self):
        return f'Элементы: {self.lst}, sum = {sum(self.lst)}'
