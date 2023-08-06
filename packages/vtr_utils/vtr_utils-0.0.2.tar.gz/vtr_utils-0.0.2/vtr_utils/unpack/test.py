import tempfile
import unittest
import pytz




class TestUnpack(unittest.TestCase):

    def test_unpack(self):

        from vtr_utils.unpack import Unpack
        import os

        unp = Unpack(os.path.join(os.path.dirname(__file__), 'testfile.txt.ARJ'))
        result = unp.get_file('testfile.txt')
        self.assertEqual('OK', result)

        unp = Unpack(os.path.join(os.path.dirname(__file__), 'testfile.txt.ARJ'), tempdir=tempfile.mkdtemp())
        result = unp.get_file('testfile.txt')
        self.assertEqual('OK', result)
        result = unp.get_file('*.txt')
        self.assertEqual('OK', result)
        self.assertRaises(ValueError, unp.get_file, 'notfile.txt')

        modify_datetime = unp.get_file_modify_datetime('testfile.txt')

        self.assertEqual(modify_datetime.year, 2016)
        self.assertEqual(modify_datetime.month, 2)
        self.assertEqual(modify_datetime.day, 3)
        self.assertEqual(modify_datetime.hour, 14)
        self.assertEqual(modify_datetime.minute, 24)
        self.assertEqual(modify_datetime.second, 31)
        self.assertEqual(modify_datetime.tzinfo, pytz.utc)

