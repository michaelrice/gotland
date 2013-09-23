import urllib2
import json
import urllib

class Client(object):

    def __init__(self, end_point="http://localhost:15672/api/",
            user_name="guest", password="guest"):
        """Client connection info for the rabbitmq_management API

        Usage::
        myapi = api(user_name="sam",password="secure")

        """
        self.end_point = end_point
        passmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passmgr.add_password(None, end_point, user_name, password)
        authhandler = urllib2.HTTPBasicAuthHandler(passmgr)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)

    def _fetch_data(self,path):
        data = None
        try:
            response = urllib2.urlopen(path)
            data = json.loads(response.read())
        except:
            pass
        return data

    def check_aliveness(self, vhost="%2f"):
        """Check aliveness of a given vhost. By default / will be checked.
        Usage::
        myapi = api()
        if not myapi.check_aliveness():
            handle_down_event()
        """
        path = self.end_point + "aliveness-test/" + vhost
        data = self._fetch_data(path)
        if data is None:
            return False
        try:
            if data.get("status") != "ok":
                return False
            return True
        except KeyError:
            return False

    def get_overview(self):
        """Various random bits of information that describe the
        whole system."""
        path = self.end_point + "overview"
        data = self._fetch_data(path)
        return data

    def get_nodes(self):
        """A list of nodes in the RabbitMQ cluster."""
        path = self.end_point + "nodes"
        data = self._fetch_data(path)
        return data

    def get_node_info(self,node_name, get_memory=False):
        """An individual node in the RabbitMQ cluster. Add "get_memory=true"
        to get memory statistics."""
        path = self.end_point + "nodes/" + node_name
        if get_memory:
            vals = {"memory": "true"}
            data = urllib.urlencode(vals)
            path = path + '?' + data
        data = self._fetch_data(path)
        return data

    def get_extensions(self):
        """A list of extensions to the management plugin"""
        path = self.end_point + "extensions"
        data = self._fetch_data(path)
        return data

    def get_connections(self):
        """A list of all open connections."""
        path = self.end_point + "connections"
        data = self._fetch_data(path)
        return data

    def get_connections_name(self,name):
        """Gets info for an individual connection"""
        name = urllib.quote(name)
        path = self.end_point + "connections/{0}".format(name)
        data = self._fetch_data(path)
        return data

    def delete_connection(self,name=None,reason=None):
        """Removes a connection by name, with an optional reason"""
        pass
        #path = self.end_point + "connections/" + name
        #return data

    def get_channels(self):
        """List of all channels"""
        path = self.end_point + "channels"
        data = self._fetch_data(path)
        return data

    def get_channels_name(self, channel=None):
        """Info about a specific channel"""
        channel = urllib.quote(channel)
        path = self.end_point + "channels/{0}".format(channel)
        data = self._fetch_data(path)
        return data

    def get_exchanges(self):
        """List of all exchanges"""
        path = self.end_point + "exchanges"
        data = self._fetch_data(path)
        return data

    def get_exchanges_vhost(self,vhost="%2f"):
        """List of all exchanges on a given vhost"""
        path = self.end_point + "exchanges/{0}".format(vhost)
        data = self._fetch_data(path)
        return data

    def get_exchanges_name_vhost(self,vhost="%2f", exchange_name=None):
        """Gets info about a given echange (name) on a given vhost"""
        path = self.end_point + "exchanges/{0}/{1}".format(vhost,exchange_name)
        return self._fetch_data(path)

    def get_bindings_for_exchange(self,vhost="%2f",exchange_name=None,
            stype="source"):
        """A list of all bindings in which a given exchange is the source."""
        path = self.end_point + "exchanges/{0}/{1}/bindings/{2}"
        path = path.format(vhost,exchange_name,stype)
        return self._fetch_data(path)

    def get_queues(self):
        """A list of all queues on the server"""
        path = self.end_point + "queues"
        return self._fetch_data(path)

    def get_queues_by_vhost(self,vhost="%2f"):
        """A list of all queues in a given virtual host."""
        path = self.end_point + "queues/{0}".format(vhost)
        return self._fetch_data(path)

    def get_queue_by_name(self,queue_name=None,vhost="%2f"):
        """Inforation about an individual queue. Takes optional vhost param
        Checks / as the default vhost"""
        path = self.end_point + "queues/{0}/{1}".format(vhost,queue_name)
        return self._fetch_data(path)

    def get_bindings_by_queue(self,queue_name=None,vhost="%2f"):
        """A list of all bindings on a given queue. Takes an optional
        vhost param. The default vhost is /"""
        path = self.end_point + "queues/{0}/{1}/bindings"
        path = path.format(vhost,queue_name)
        return self._fetch_data(path)

    def get_bindings(self):
        """A list of all bindings."""
        path = self.end_point + "bindings"
        return self._fetch_data(path)

    def get_bindings_by_vhost(self,vhost="%2f"):
        """A list of all bindings in a given virtual host."""
        path =  self.end_point + "bindings/{0}".format(vhost)
        return self._fetch_data(path)

    def get_bindings_between_exchange_and_queue(self,queue_name=None,
            exchange_name=None,vhost=None):
        """A list of all bindings between an exchange and a queue.
        Remember, an exchange and a queue can be bound together many times!
        """
        path = self.end_point + "bindings/{0}/e/{1}/q/{2}"
        path = path.format(vhost,exchange_name,queue_name)
        return self._fetch_data(path)

    def update_bindings_between_exchange_and_queue(self):
        """A list of all bindings between an exchange and a queue.
        Remember, an exchange and a queue can be bound together many times!
        To create a new binding, POST to this URI. You will need a body looking
        something like this:
            {"routing_key":"my_routing_key","arguments":[]}

        All keys are optional. The response will contain a Location header
        telling you the URI of your new binding."""
        pass

if __name__ == "__main__":
    mytest = Client()
    print mytest.check_aliveness()
    #print mytest.get_overview()
    #print mytest.get_nodes()
    #print mytest.get_node_info((mytest.get_nodes()[0]).get("name"),
    #                             get_memory=True)
    #print mytest.get_extensions()
    #print (mytest.get_connections()[0]).get("name")
    #print mytest.get_channels()
    #print mytest.get_exchanges()
    #print mytest.get_exchanges_name_vhost(exchange_name="amq.rabbitmq.trace")
    #print mytest.get_bindings_for_exchange(exchange_name="amq.rabbitmq.trace")
    #print mytest.get_bindings_for_exchange(exchange_name="amq.rabbitmq.trace",
    #        stype="destination")
    #print mytest.get_queues()
    #print mytest.get_queues_vhost()
    print mytest.get_queue_name_vhost(queue_name="aliveness-test")
