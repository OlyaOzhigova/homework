class FlatIterator:
    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        # ����� ��� ��������
        self.storage_list = list(self.list_of_list)

    def __iter__(self):
        return self

    def __next__(self):
        while self.storage_list:
            current = self.storage_list.pop(0)
            # print(current)
            if isinstance(current, list):
                self.storage_list = current + self.storage_list
            else:
                return current
        raise StopIteration


def test_3():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']


if __name__ == '__main__':
    test_3()