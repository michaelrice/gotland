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
        """Call the check with a vhost that isnt real"""
        dead = self.rabbit.check_aliveness("fail")
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

    def test_get_node_info(self):
        node_list = self.rabbit.get_nodes()
        node_info_dict = self.rabbit.get_node_info(node_list[0]["name"],
                get_memory=True)
        self.assertIsInstance(node_info_dict,dict)

    def test_get_extensions(self):
        extension_list = self.rabbit.get_extensions()
        self.assertIsInstance(extension_list, list)

    def test_get_connections(self):
        connection_list = self.rabbit.get_connections()
        self.assertIsInstance(connection_list, list)

    def test_get_connections_name(self):
        connection_list = self.rabbit.get_connections()
        connection_dict = self.rabbit.get_connections_name(connection_list[-1]["name"])
        self.assertIsInstance(connection_dict,dict)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
