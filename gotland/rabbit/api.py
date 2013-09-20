import urllib2
import json
import urllib

class api(object):

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

    def check_aliveness(self, vhost="%2f"):
        """Check aliveness of a given vhost. By default / will be checked.
        Usage::
        myapi = api()
        if not myapi.check_aliveness():
            handle_down_event()
        """
        path = self.end_point + "aliveness-test/" + vhost
        data = None
        try:
            response = urllib2.urlopen(path)
            data = json.loads(response.read())
        except urllib2.URLError:
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
        data = {}
        try:
            response = urllib2.urlopen(path)
            data = json.loads(response.read())
        except:
            return None
        return data

    def get_nodes(self):
        """A list of nodes in the RabbitMQ cluster."""
        path = self.end_point + "nodes"
        data = []
        try:
            response = urllib2.urlopen(path)
            data = json.loads(response.read())
        except:
            return None
        return data

    def get_node_info(self,node_name, get_memory=False):
        """An individual node in the RabbitMQ cluster. Add "get_memory=true" 
        to get memory statistics."""
        path = self.end_point + "nodes/" + node_name
        data = {}
        if get_memory:
            vals = {"memory": "true"}
            data = urllib.urlencode(vals)
            path = path + '?' + data
        try:
            response = urllib2.urlopen(path)
            data = json.loads(response.read())
        except:
            return None
        return data

    def get_extensions(self):
        """A list of extensions to the management plugin"""
        path = self.end_point + "extensions"
        data = []
        try:
            response = urllib2.urlopen(path)
            data = json.loads(response.read())
        except:
            return None
        return data

    def get_connections(self):
        """A list of all open connections."""
        path = self.end_point + "connections"
        data = []
        try:
            response = urllib2.urlopen(path)
            data = json.loads(response.read())
        except:
            return None
        return data

    def get_connections_name(self,name):
        """Gets info for an individual connection"""
        path = self.end_point + "connections/" + name
        data = []
        return data

    def delete_connection(self,name=None,reason=None):
        """Removes a connection by name, with an optional reason"""
        path = self.end_point + "connections/" + name
        pass

    def get_channels(self):
        """List of all channels"""
        return []

    def get_channels_name(self, channel=None):
        """Info about a specific channel"""
        return []

    def get_exchanges(self):
        """List of all exchanges"""
        return []

    def get_exchanges_vhost(self,vhost=None):
        """List of all exchanges on a given vhost"""
        return []

    def get_exchanges_name_vhost(self,vhost=None, name=None):
        """Gets info about a given echange (name) on a given vhost"""
        return {}

    def get_bindings_for_exchange(self,vhost=None,exchange_name=None):
        """A list of all bindings in which a given exchange is the source."""
        return []


if __name__ == "__main__":
    mytest = api()
    #print mytest.check_aliveness()
    #print mytest.get_overview()
    #print mytest.get_nodes()
    #print mytest.get_node_info((mytest.get_nodes()[0]).get("name"),get_memory=True)
    #print mytest.get_extensions()
    print (mytest.get_connections()[0]).get("name")
