import unittest

from pyswing.HelloWorld import helloWorld


class TestHelloWorld(unittest.TestCase):

    def test_HelloWorld(self):

        args = "-n Gary".split()
        helloWorld(args)
        pass


if __name__ == '__main__':
    unittest.main()


