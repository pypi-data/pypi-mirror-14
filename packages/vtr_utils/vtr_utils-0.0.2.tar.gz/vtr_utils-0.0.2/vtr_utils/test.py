import unittest

class TestDictUpdate(unittest.TestCase):

    def test_dict_update(self):

        from vtr_utils import dict_update
        import addict

        d = addict.Dict()

        d.d1.d2.d3 = 1
        d.d1.d3 = 2
        d.d2 = 3

        d2 = addict.Dict()

        d2.d1.d3 = 2
        d2.d2 = 4

        d3 = dict_update(d, d2)

        self.assertEqual(d3.d1.d3, 2)
        self.assertEqual(d3.d2, 4)
        self.assertEqual(d3.d1.d2.d3, 1)

