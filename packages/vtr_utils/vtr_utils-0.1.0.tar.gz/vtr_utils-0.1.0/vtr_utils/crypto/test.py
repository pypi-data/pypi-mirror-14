import unittest

class TestCrypto(unittest.TestCase):

    def test_random(self):

        from vtr_utils import crypto

        rnd1 = crypto.get_random_string()
        rnd2 = crypto.get_random_string()

        self.assertNotEqual(rnd1, rnd2)

        import random

        orig_system_random = random.SystemRandom

        class SystemRandom(object):
            def __init__(self):
                raise NotImplementedError('mock')

        random.SystemRandom = SystemRandom

        reload(crypto)


        rnd1 = crypto.get_random_string()
        rnd2 = crypto.get_random_string()

        self.assertNotEqual(rnd1, rnd2)

        random.SystemRandom = orig_system_random

        reload(crypto)
