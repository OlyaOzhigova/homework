class FlatIterator:

    def __init__(self, list_of_lists):
        self.list_of_lists = list_of_lists
        self.all_el = 0  # общий счетчик
        self.el = 0  # счетчик
    def __iter__(self):
        return self

    def __next__(self):
        while self.all_el < len(self.list_of_lists):
            if self.el < len(self.list_of_lists[self.all_el]):
                item = self.list_of_lists[self.all_el][self.el]
                self.el += 1
                return item
            else:
                self.all_el += 1
                self.el = 0

        raise StopIteration


def test_1():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


if __name__ == '__main__':
    test_1()