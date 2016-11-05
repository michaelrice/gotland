import unittest
import vcr
from gotland.rabbit import api
import tests


class RabbitApiTests(tests.VCRBasedTests):

    rabbit = api.Client(end_point='http://localhost:55672/api/')

    @vcr.use_cassette('test_aliveness.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_aliveness(self):
        alive = self.rabbit.check_aliveness()
        self.assertTrue(alive)

    @vcr.use_cassette('test_aliveness_fails.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_aliveness_fails(self):
        """Call the check with a vhost that isnt real"""
        dead = self.rabbit.check_aliveness("fail")
        self.assertFalse(dead)

    @vcr.use_cassette('test_overview.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_overview(self):
        alive = self.rabbit.get_overview()
        self.assertIsInstance(alive, dict)

    @vcr.use_cassette('test_overview_for_content.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_overview_for_content(self):
        """This test will fail if youre not using 3.1.5"""
        info_dict = self.rabbit.get_overview()
        self.assertDictContainsSubset(
            {"management_version": "0.0.0"},
            info_dict
        )

    @vcr.use_cassette('test_get_nodes.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_nodes(self):
        info_list = self.rabbit.get_nodes()
        self.assertIsInstance(info_list, list)

    @vcr.use_cassette('test_get_node_info.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_node_info(self):
        node_list = self.rabbit.get_nodes()
        node_info_dict = self.rabbit.get_node_info(node_list[0]["name"],
                                                   get_memory=True)
        self.assertIsInstance(node_info_dict, dict)

    @vcr.use_cassette('test_get_extensions.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_extensions(self):
        extension_list = self.rabbit.get_extensions()
        self.assertIsInstance(extension_list, list)

    @vcr.use_cassette('test_get_connections.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_connections(self):
        connection_list = self.rabbit.get_connections()
        self.assertIsInstance(connection_list, list)

    @vcr.use_cassette('test_get_connections_name.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_connections_name(self):
        connection_list = self.rabbit.get_connections()
        connection_dict = self.rabbit.get_connections_name(
            connection_list[-1]["name"])
        self.assertIsInstance(connection_dict, dict)

    @vcr.use_cassette('test_get_channels.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_channels(self):
        channel_list = self.rabbit.get_channels()
        self.assertIsInstance(channel_list, list)

    @vcr.use_cassette('test_get_channels_name.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_channels_name(self):
        channel_info_dict = self.rabbit.get_channels_name(
            channel=self.rabbit.get_channels()[0]["name"])
        self.assertIsInstance(channel_info_dict, dict)

    @vcr.use_cassette('test_get_exchanges.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_exchanges(self):
        exchange_list = self.rabbit.get_exchanges()
        self.assertIsInstance(exchange_list, list)

    @vcr.use_cassette('test_get_exchanges_by_vhost.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_exchanges_by_vhost(self):
        exchange_list = self.rabbit.get_exchanges_vhost()
        self.assertIsInstance(exchange_list, list)

    @vcr.use_cassette('test_get_exchanges_name_vhost.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_exchanges_name_vhost(self):
        exchange_dict = self.rabbit.get_exchanges_name_vhost(
            exchange_name=self.rabbit.get_exchanges_vhost()[-1]["name"])
        self.assertIsInstance(exchange_dict, dict)

    @vcr.use_cassette('test_get_bindings_for_exchange.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_bindings_for_exchange(self):
        binding_list = self.rabbit.get_bindings_for_exchange(
            exchange_name=self.rabbit.get_exchanges_vhost()[-1]["name"])
        self.assertIsInstance(binding_list, list)

    @vcr.use_cassette('test_get_queues.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_queues(self):
        queues = self.rabbit.get_queues()
        self.assertIsInstance(queues, list)

    @vcr.use_cassette('test_get_queues_by_vhost.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_queues_by_vhost(self):
        queues = self.rabbit.get_queues_by_vhost()
        self.assertIsInstance(queues, list)

    @vcr.use_cassette('test_get_queue_by_name.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_queue_by_name(self):
        qname = self.rabbit.get_queues_by_vhost()[0]["name"]
        queue = self.rabbit.get_queue_by_name(queue_name=qname)
        self.assertIsInstance(queue, dict)

    @vcr.use_cassette('test_get_bindings_by_queue.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_bindings_by_queue(self):
        qname = self.rabbit.get_queues_by_vhost()[0]["name"]
        bindings = self.rabbit.get_bindings_by_queue(queue_name=qname)
        self.assertIsInstance(bindings, list)

    @vcr.use_cassette('test_get_bindings.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_bindings(self):
        bindings = self.rabbit.get_bindings()
        self.assertIsInstance(bindings, list)

    @vcr.use_cassette('test_get_bindings_by_vhost.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_bindings_by_vhost(self):
        bindings = self.rabbit.get_bindings_by_vhost()
        self.assertIsInstance(bindings, list)

    @vcr.use_cassette('test_create_user.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_create_user(self):
        no_content = self.rabbit.create_user('alice', {"password": "password", "tags": ""})
        self.assertIsNone(no_content)

    @vcr.use_cassette('test_delete_user.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_delete_user(self):
        no_content = self.rabbit.delete_user('alice')
        self.assertIsNone(no_content)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
