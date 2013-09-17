import unittest
import sys

sys.path.append("../")

from gotland.rabbit import api

class RabbitApiTests(unittest.TestCase):

    rabbit = api.api()

    def test_aliveness(self):
        alive = self.rabbit.check_aliveness()
        self.assertTrue(alive)

    def test_aliveness_fails(self):
        dead = self.rabbit.check_aliveness(vhost="failme")
        self.assertFalse(dead)

    def test_overview(self):
        alive = self.rabbit.get_overview()
        self.assertIsInstance(alive,dict)

    def test_overview_for_content(self):
        """This test will fail if youre not using 3.1.5"""
        info_dict = self.rabbit.get_overview()
        self.assertDictContainsSubset({"management_version":"3.1.5"},info_dict)

    def test_get_nodes(self):
        info_list = self.rabbit.get_nodes()
        self.assertIsInstance(info_list, list)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
