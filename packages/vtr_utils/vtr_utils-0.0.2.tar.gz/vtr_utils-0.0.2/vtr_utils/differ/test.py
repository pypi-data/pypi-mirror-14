import unittest

class TestDiffer(unittest.TestCase):

    def test_differs(self):

        from vtr_utils.differ import DictDiffer, ListDiffer

        # was
        past = {
            '1': 1,
            '2': 2,
            '4': 5,
            '5': {'1': 1, '2': 2},
            '6': [1, 2, 3],
            '7': 7,
        }

        # new
        curr = {
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': {'1': 1, '2': 2, '3': 3},
            '6': [1, 2, 3, 4]
        }

        dd = DictDiffer(current_dict=curr, past_dict=past)

        self.assertEqual(dd.added(), set(['3']))
        self.assertEqual(dd.changed(), set(['4', '5', '6']))
        self.assertEqual(dd.removed(), set(['7']))
        self.assertEqual(dd.unchanged(), set(['1', '2']))

        # was
        past = ['0', '2', '1', '4', '5', '8', '7', '3']
        # new
        curr = ['1', '2', '3', '4', '5', '6']

        ld = ListDiffer(current_list=curr, past_list=past)

        self.assertEqual(ld.list_to_dict(['1', '2']), {0: '1', 1: '2'})

        self.assertEqual(ld.unchanged(), set([1, 3, 4]))
        self.assertEqual(ld.changed(), set([0, 2, 5]))
        self.assertEqual(ld.removed(), set([6, 7]))

        curr = ['1', '2', '3', '4', '5', '6', '10', '3', '123', '321']

        ld = ListDiffer(current_list=curr, past_list=past)

        self.assertEqual(ld.unchanged(), set([1, 3, 4, 7]))
        self.assertEqual(ld.changed(), set([0, 2, 5, 6]))
        self.assertEqual(ld.added(), set([8, 9]))
