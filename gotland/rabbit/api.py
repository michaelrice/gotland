import urllib2
import json
import urllib

class Client(object):

    def __init__(self, end_point="http://localhost:15672/api/",
            username="guest", password="guest"):
        """Client connection info for the rabbitmq_management API

        Usage::
        myapi = api(username="sam",password="secure")

        """
        self.end_point = end_point
        passmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passmgr.add_password(None, end_point, username, password)
        authhandler = urllib2.HTTPBasicAuthHandler(passmgr)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)

    def _get_data(self,path):
        """Lots of work to do here. Literally doing the least possible
        to just get something functional. Need to add error handling,
        and raise proper exceptions"""
        data = None
        try:
            response = urllib2.urlopen(path)
            data = json.loads(response.read())
        except:
            pass
        return data

    def _send_data(self,path,data=None,request_type='PUT'):
        response_data = None
        data = json.dumps(data)
        if data == 'null':
            data = None
        headers = {"Content-type":"application/json",
                "Accept":"application/json"}
        try:
            request = urllib2.Request(path, data=data,headers=headers)
            request.get_method = lambda: request_type
            response = urllib2.urlopen(request)
            response_data = json.loads(response.read())
        except:
            pass
        return response_data

    def check_aliveness(self, vhost="%2f"):
        """Check aliveness of a given vhost. By default / will be checked.
        Usage::
        myapi = api()
        if not myapi.check_aliveness():
            handle_down_event()
        """
        path = self.end_point + "aliveness-test/" + vhost
        data = self._get_data(path)
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
        data = self._get_data(path)
        return data

    def get_nodes(self):
        """A list of nodes in the RabbitMQ cluster."""
        path = self.end_point + "nodes"
        data = self._get_data(path)
        return data

    def get_node_info(self,node_name, get_memory=False):
        """An individual node in the RabbitMQ cluster. Add "get_memory=true"
        to get memory statistics."""
        path = self.end_point + "nodes/" + node_name
        if get_memory:
            vals = {"memory": "true"}
            data = urllib.urlencode(vals)
            path = path + '?' + data
        data = self._get_data(path)
        return data

    def get_extensions(self):
        """A list of extensions to the management plugin"""
        path = self.end_point + "extensions"
        data = self._get_data(path)
        return data

    def get_connections(self):
        """A list of all open connections."""
        path = self.end_point + "connections"
        data = self._get_data(path)
        return data

    def get_connections_name(self,name):
        """Gets info for an individual connection"""
        name = urllib.quote(name)
        path = self.end_point + "connections/{0}".format(name)
        data = self._get_data(path)
        return data

    def get_channels(self):
        """List of all channels"""
        path = self.end_point + "channels"
        data = self._get_data(path)
        return data

    def get_channels_name(self, channel=None):
        """Info about a specific channel"""
        channel = urllib.quote(channel)
        path = self.end_point + "channels/{0}".format(channel)
        data = self._get_data(path)
        return data

    def get_exchanges(self):
        """List of all exchanges"""
        path = self.end_point + "exchanges"
        data = self._get_data(path)
        return data

    def get_exchanges_vhost(self,vhost="%2f"):
        """List of all exchanges on a given vhost"""
        path = self.end_point + "exchanges/{0}".format(vhost)
        data = self._get_data(path)
        return data

    def get_exchanges_name_vhost(self,vhost="%2f", exchange_name=None):
        """Gets info about a given echange (name) on a given vhost"""
        path = self.end_point + "exchanges/{0}/{1}".format(vhost,exchange_name)
        return self._get_data(path)

    def get_bindings_for_exchange(self,vhost="%2f",exchange_name=None,
            stype="source"):
        """A list of all bindings in which a given exchange is the source."""
        path = self.end_point + "exchanges/{0}/{1}/bindings/{2}"
        path = path.format(vhost,exchange_name,stype)
        return self._get_data(path)

    def get_queues(self):
        """A list of all queues on the server"""
        path = self.end_point + "queues"
        return self._get_data(path)

    def get_queues_by_vhost(self,vhost="%2f"):
        """A list of all queues in a given virtual host."""
        path = self.end_point + "queues/{0}".format(vhost)
        return self._get_data(path)

    def get_queue_by_name(self,queue_name=None,vhost="%2f"):
        """Inforation about an individual queue. Takes optional vhost param
        Checks / as the default vhost"""
        path = self.end_point + "queues/{0}/{1}".format(vhost,queue_name)
        return self._get_data(path)

    def get_bindings_by_queue(self,queue_name=None,vhost="%2f"):
        """A list of all bindings on a given queue. Takes an optional
        vhost param. The default vhost is /"""
        path = self.end_point + "queues/{0}/{1}/bindings"
        path = path.format(vhost,queue_name)
        return self._get_data(path)

    def get_bindings(self):
        """A list of all bindings."""
        path = self.end_point + "bindings"
        return self._get_data(path)

    def get_bindings_by_vhost(self,vhost="%2f"):
        """A list of all bindings in a given virtual host."""
        path =  self.end_point + "bindings/{0}".format(vhost)
        return self._get_data(path)

    def get_bindings_between_exchange_and_queue(self,queue_name=None,
            exchange_name=None,vhost=None):
        """A list of all bindings between an exchange and a queue.
        Remember, an exchange and a queue can be bound together many times!
        """
        path = self.end_point + "bindings/{0}/e/{1}/q/{2}"
        path = path.format(vhost,exchange_name,queue_name)
        return self._get_data(path)

    def update_bindings_between_exchange_and_queue(self):
        """A list of all bindings between an exchange and a queue.
        Remember, an exchange and a queue can be bound together many times!
        To create a new binding, POST to this URI. You will need a body looking
        something like this:
            {"routing_key":"my_routing_key","arguments":[]}

        All keys are optional. The response will contain a Location header
        telling you the URI of your new binding."""
        pass

    def get_binding_between_exchange_and_queue(self,queue_name=None,
            exchange_name=None,vhost="%2f"):
        """
        An individual binding between an exchange and a queue.
        The props part of the URI is a "name" for the binding composed of
        its routing key and a hash of its arguments.
        """
        path = self.end_point + "bindings/{0}/e/{1}/q/{2}/props"
        path = path.format(vhost,exchange_name,queue_name)
        return self._get_data(path)

    def get_bindings_between_exchanges(self,exchange_name_s=None,
            exchange_name_d=None,stype="destination",vhost="%2f"):
        """A list of all bindings between two exchanges. Similar to the list
        of all bindings between an exchange and a queue, above.
        stype can be either "destination" or "props"
        """
        path = self.end_point + "bindings/{0}/e/{1}/e/{2}/{3}"
        path = path.format(vhost,exchange_name_s,exchange_name_s,stype)
        return self._get_data(path)

    def get_vhosts(self):
        """Return a list of all vhosts"""
        path = self.end_point + "vhosts"
        return self._get_data(path)

    def get_vhost_by_name(self,vhost="%2f"):
        """An individual virtual host. As a virtual host only has a name,
        you do not need an HTTP body when PUTing one of these.
        """
        path = self.end_point + "vhosts/{0}".format(vhost)
        return self._get_data(path)

    def get_premissions_by_vhost(self,vhost="%2f"):
        """A list of all permissions for a given virtual host."""
        path = self.end_point + "vhosts/{0}/permissions".format(vhost)
        return self._get_data(path)

    def get_users(self):
        """A list of all users"""
        path = self.end_point + "users"
        return self._get_data(path)

    def get_user_by_name(self,username="guest"):
        """Info about an individual user"""
        path = self.end_point + "users/{0}".format(username)
        return self._get_data(path)

    def get_user_permissions(self,username="guest"):
        """A list of all permissions for a given user."""
        path = self.end_point + "users/{0}/permissions".format(username)
        return self._get_data(path)

    def whoami(self):
        """Details of the currently authenticated user."""
        path = self.end_point + "whoami"
        return self._get_data(path)

    def get_permissions(self):
        """A list of all permissions for all users."""
        path = self.end_point + "permissions"
        return self._get_data(path)

    def get_user_permissions_by_vhost(self,username="guest",vhost="%2f"):
        """An individual permission of a user and virtual host."""
        path = self.end_point + "permissions/{0}/{1}".format(vhost,username)
        return self._get_data(path)

    def get_parameters(self):
        """A list of all parameters."""
        path = self.end_point + "parameters"
        return self._get_data(path)

    def get_parameters_by_component(self,component=None):
        """A list of all parameters for a given component."""
        path = self.end_point + "parameters/{0}".format(component)
        return self._get_data(path)

    def get_parameters_by_component_by_vhost(self, component=None,
            vhost="%2f"):
        """A list of all parameters for a given component and virtual host"""
        path = self.end_point + "parameters/{1}/{0}".format(vhost,component)
        return self._get_data(path)

    def get_parameter_for_vhost_by_component_name(self,component=None,
            parameter_name=None,vhost="%2f"):
        """Get an individual parameter value from a given vhost & component"""
        path = self.end_point + "parameters/{1}/{0}/{2}"
        path = path.format(vhost,component,parameter_name)
        return self._get_data(path)

    def get_policies(self):
        """A list of all policies"""
        path = self.end_point + "policies"
        return self._get_data(path)

    def get_policies_by_vhost(self,vhost="%2f"):
        """A list of all policies in a given virtual host."""
        path = self.end_point + "policies/{0}".format(vhost)
        return self._get_data(path)

    def get_policy_for_vhost_by_name(self, name=None, vhost="%2f"):
        """Information about an individual policy"""
        path = self.end_point + "policies/{0}/{1}".format(vhost,name)
        return self._get_data(path)

    def create_exchange_on_vhost(self,exchange_name=None,
            body={},vhost="%2f"):
        """An individual exchange. To PUT an exchange, you will need a body
        looking something like this:
        {
            "type":"direct",
            "auto_delete":false,
            "durable":true,
            "internal":false,
            "name": "mytest",
            "arguments":[]
        }
        """
        path = self.end_point + "exchanges/{0}/{1}".format(vhost,exchange_name)
        return self._send_data(path,data=body)

    def create_queue_on_vhost(self,queue_name=None,body={},vhost="%2f"):
        """An individual queue. To PUT a queue, you will need a body looking
        something like this:
        {
            "auto_delete":false,
            "durable":true,
            "arguments":[],
            "node":"rabbit@localnode-1"
        }
        """
        path = self.end_point + "queues/{0}/{1}".format(vhost,queue_name)
        return self._send_data(path,data=body)

    def create_vhost(self,vhost=None):
        """An individual virtual host. As a virtual host only has a name,
        you do not need an HTTP body when PUTing one of these."""
        path = self.end_point + "vhosts/{0}".format(vhost)
        return self._send_data(path)

    def create_user(self,username,body={}):
        """An individual user. To PUT a user, you will need a body looking
        something like this:
        {
            "password":"secret",
            "tags":"administrator"
        }

        or:

        {
            "password_hash":"2lmoth8l4H0DViLaK9Fxi6l9ds8=",
            "tags":"administrator"
        }

        The tags key is mandatory. Either password or password_hash must be
        set. Setting password_hash to "" will ensure the user cannot use a
        password to log in. tags is a comma-separated list of tags for the
        user. Currently recognised tags are "administrator", "monitoring"
        and "management".
        """
        path = self.end_point + "users/{0}".format(username)
        return self._send_data(path,data=body)

    def grant_permissions_on_vhost(self,body={},username=None,
            vhost="%2f"):
        """An individual permission of a user and virtual host. To PUT a
        permission, you will need a body looking something like this:
        {
            "configure":".*",
            "write":".*",
            "read":".*"
        }
        All keys are mandatory.
        """
        path = self.end_point + "permissions/{0}/{1}".format(vhost,username)
        return self._send_data(path,data=body)

    def update_parameter(self,component=None,body={},parameter_name=None,
            vhost="%2f"):
        """An individual parameter. To PUT a parameter, you will need a body
        looking something like this:
        {
            "vhost": "/",
            "component":"federation",
            "name":"local_username",
            "value":"guest"
        }
        """
        path = "parameters/{1}/{0}/{2}".format(vhost,component,parameter_name)
        return self._send_data(path,data=body)

    def update_policies(self,policy_name=None,vhost="%2f"):
        """An individual policy. To PUT a policy, you will need a body
        looking something like this:
        {
            "pattern":"^amq.",
            "definition": {
                "federation-upstream-set":"all"
            },
            "priority":0
        }
        policies/vhost/name
        """
        pass

    def delete_connection(self,name=None,reason=None):
        """Removes a connection by name, with an optional reason"""
        pass
        #path = self.end_point + "connections/" + name
        #return data


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
    print mytest.get_queue_by_name(queue_name="aliveness-test")
    #print mytest.create_user("mike",{"password":"poop","tags":"administrator"})
    #print mytest.create_user("mike",{})
