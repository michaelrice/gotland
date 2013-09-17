import unittest
import sys

sys.path.append("../")

from gotland.rabbit import api

class RabbitApiTests(unittest.TestCase):

    def test_aliveness(self):
        rabbit = api.api()
        alive = rabbit.check_aliveness()
        self.failUnless(alive)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
