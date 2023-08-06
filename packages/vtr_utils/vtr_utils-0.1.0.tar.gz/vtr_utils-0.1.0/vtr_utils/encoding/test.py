# coding: utf8
import unittest

class TestTextUtils(unittest.TestCase):

    def test_is_protected(self):
        import six
        import datetime
        import types
        from decimal import Decimal
        from vtr_utils.encoding import is_protected_type

        protected_types = six.integer_types + (type(None), float, Decimal,
            datetime.datetime, datetime.date, datetime.time)
        for t in protected_types:
            if t == types.NoneType:
                obj = None
            elif t == datetime.datetime or t == datetime.date:
                obj = t(1970, 1, 2)
            else:
                obj = t()
            res = is_protected_type(obj)
            self.assertTrue(res)

        obj = lambda : None
        res = is_protected_type(obj)
        self.assertFalse(res)

    def test_force_text_exception(self):
        """
        Check that broken __unicode__/__str__ actually raises an error.
        """
        import six
        from vtr_utils.encoding import force_text
        class MyString(object):
            def __str__(self):
                return b'\xc3\xb6\xc3\xa4\xc3\xbc'

            __unicode__ = __str__

        # str(s) raises a TypeError on python 3 if the result is not a text type.
        # python 2 fails when it tries converting from str to unicode (via ASCII).
        exception = TypeError if six.PY3 else UnicodeError
        with self.assertRaises(exception):
            force_text(MyString())

        try:
            force_text(MyString())
        except exception as e:
            res = e.__str__()
            self.assertTrue('ascii' in res)

        s = force_text('a')
        self.assertEqual(s, 'a')

        s = force_text(u'a')
        self.assertEqual(s, u'a')

        res = force_text(None, strings_only=True)
        self.assertEqual(res, None)

        class MyBytes(bytes):
            pass


        s = force_text(MyBytes())
        self.assertEqual(s, '')

        s = force_text(bytes())
        self.assertEqual(s, '')

        class MyClass(object):
            pass

        a = MyClass()
        s = force_text(a)
        self.assertEqual(str(a), s)

        six.PY3 = True

        s = force_text(MyBytes())
        self.assertEqual(s, '')

        s = force_text(bytes())
        self.assertEqual(s, '')

        a = MyClass()
        s = force_text(a)
        self.assertEqual(str(a), s)

        reload(six)

        e = Exception(b'\xc3\xb6\xc3\xa4\xc3\xbc')

        s = force_text(e)
        self.assertEqual(s, u'\xf6\xe4\xfc')