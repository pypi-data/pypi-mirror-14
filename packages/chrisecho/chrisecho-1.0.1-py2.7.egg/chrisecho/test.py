import unittest
from chrisecho import Echo


class EchoTest(unittest.TestCase):

    def test(self):
        x = Echo()
        self.assertEqual(x.doit("Hello World"), "Hello World")

    def test_starting_out(self):
        self.assertEqual(1, 1)

    def test_2(self):
        self.assertGreater(2, 1)

    def test_json(self):
        x = Echo()
        self.assertEqual(x.do_request()["count"], 0)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
