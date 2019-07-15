# Copyright 2014 Michael Rice <michael@michaelrice.org>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from __future__ import absolute_import

import json
try:
    from urllib import quote, quote_plus
except ImportError:
    from urllib.parse import quote, quote_plus

import requests
from requests.auth import HTTPBasicAuth


class Client(object):

    def __init__(self, end_point="http://localhost:15672/api/",
                 username="guest", password="guest"):
        """Client connection info for the rabbitmq_management API

        Usage::
        myapi = api(username="sam",password="secure")

        """
        self.end_point = end_point
        self.auth = HTTPBasicAuth(username, password)

    def _get_data(self, path, **kwargs):
        """Lots of work to do here. Literally doing the least possible
        to just get something functional. Need to add error handling,
        and raise proper exceptions"""
        params = None
        if 'params' in kwargs:
            params = kwargs.get("params")
        response = requests.get(path, auth=self.auth, params=params)
        if response.status_code != 200:
            return
        return response.json()

    def _send_data(self, path, data=None, request_type='PUT'):
        data = json.dumps(data)
        if data == 'null':
            data = None
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json"
        }
        if request_type is 'PUT':
            response = requests.put(path, data, headers=headers, auth=self.auth)
        elif request_type is 'DELETE':
            response = requests.delete(path, auth=self.auth, headers=headers,
                                       data=data)
        else:
            response = requests.post(path, data=data, headers=headers,
                                     auth=self.auth)
        if response.status_code == 204:
            return
        return response.json()

    def check_aliveness(self, vhost='/'):
        """Check aliveness of a given vhost. By default / will be checked.
        Usage::
        myapi = api()
        if not myapi.check_aliveness():
            handle_down_event()
        """
        path = self.end_point + "aliveness-test/" + quote_plus(vhost)
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

    def get_node_info(self, node_name, get_memory=False):
        """An individual node in the RabbitMQ cluster. Add "get_memory=true"
        to get memory statistics."""
        path = self.end_point + "nodes/" + node_name
        params = None
        if get_memory:
            params = {"memory": "true"}

        data = self._get_data(path, params=params)
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

    def get_connections_name(self, name):
        """Gets info for an individual connection"""
        name = quote(name)
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
        channel = quote(channel)
        path = self.end_point + "channels/{0}".format(channel)
        data = self._get_data(path)
        return data

    def get_exchanges(self):
        """List of all exchanges"""
        path = self.end_point + "exchanges"
        data = self._get_data(path)
        return data

    def get_exchanges_vhost(self, vhost='/'):
        """List of all exchanges on a given vhost"""
        path = self.end_point + "exchanges/{0}".format(quote_plus(vhost))
        data = self._get_data(path)
        return data

    def get_exchanges_name_vhost(self, vhost='/', exchange_name=None):
        """Gets info about a given echange (name) on a given vhost"""
        vhost = quote_plus(vhost)
        path = self.end_point + "exchanges/{0}/{1}".format(vhost, exchange_name)
        return self._get_data(path)

    def get_bindings_for_exchange(self, vhost='/', exchange_name=None,
            stype="source"):
        """A list of all bindings in which a given exchange is the source."""
        path = self.end_point + "exchanges/{0}/{1}/bindings/{2}"
        path = path.format(quote_plus(vhost), exchange_name, stype)
        return self._get_data(path)

    def get_queues(self):
        """A list of all queues on the server"""
        path = self.end_point + "queues"
        return self._get_data(path)

    def get_queues_by_vhost(self, vhost='/'):
        """A list of all queues in a given virtual host."""
        path = self.end_point + "queues/{0}".format(quote_plus(vhost))
        return self._get_data(path)

    def get_queue_by_name(self, queue_name=None, vhost='/'):
        """Inforation about an individual queue. Takes optional vhost param
        Checks / as the default vhost"""
        vhost = quote_plus(vhost)
        path = self.end_point + "queues/{0}/{1}".format(vhost, queue_name)
        return self._get_data(path)

    def get_bindings_by_queue(self, queue_name=None, vhost='/'):
        """A list of all bindings on a given queue. Takes an optional
        vhost param. The default vhost is /"""
        path = self.end_point + "queues/{0}/{1}/bindings"
        path = path.format(quote_plus(vhost), queue_name)
        return self._get_data(path)

    def get_bindings(self):
        """A list of all bindings."""
        path = self.end_point + "bindings"
        return self._get_data(path)

    def get_bindings_by_vhost(self, vhost='/'):
        """A list of all bindings in a given virtual host."""
        path =  self.end_point + "bindings/{0}".format(quote_plus(vhost))
        return self._get_data(path)

    def get_bindings_between_exchange_and_queue(self, queue_name=None,
            exchange_name=None, vhost='/'):
        """A list of all bindings between an exchange and a queue.
        Remember, an exchange and a queue can be bound together many times!
        """
        path = self.end_point + "bindings/{0}/e/{1}/q/{2}"
        path = path.format(quote_plus(vhost), exchange_name, queue_name)
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

    def get_binding_between_exchange_and_queue(self, queue_name=None,
            exchange_name=None, vhost='/'):
        """
        An individual binding between an exchange and a queue.
        The props part of the URI is a "name" for the binding composed of
        its routing key and a hash of its arguments.
        """
        path = self.end_point + "bindings/{0}/e/{1}/q/{2}/props"
        path = path.format(quote_plus(vhost), exchange_name, queue_name)
        return self._get_data(path)

    def get_bindings_between_exchanges(self, exchange_name_s=None,
            exchange_name_d=None, stype="destination", vhost='/'):
        """A list of all bindings between two exchanges. Similar to the list
        of all bindings between an exchange and a queue, above.
        stype can be either "destination" or "props"
        """
        path = self.end_point + "bindings/{0}/e/{1}/e/{2}/{3}"
        vhost = quote_plus(vhost)
        path = path.format(vhost, exchange_name_s, exchange_name_d, stype)
        return self._get_data(path)

    def get_vhosts(self):
        """Return a list of all vhosts"""
        path = self.end_point + "vhosts"
        return self._get_data(path)

    def get_vhost_by_name(self, vhost='/'):
        """An individual virtual host. As a virtual host only has a name,
        you do not need an HTTP body when PUTing one of these.
        """
        path = self.end_point + "vhosts/{0}".format(quote_plus(vhost))
        return self._get_data(path)

    def get_premissions_by_vhost(self, vhost='/'):
        """A list of all permissions for a given virtual host."""
        vhost = quote_plus(vhost)
        path = self.end_point + "vhosts/{0}/permissions".format(vhost)
        return self._get_data(path)

    def get_users(self):
        """A list of all users"""
        path = self.end_point + "users"
        return self._get_data(path)

    def get_user_by_name(self, username="guest"):
        """Info about an individual user"""
        path = self.end_point + "users/{0}".format(username)
        return self._get_data(path)

    def get_user_permissions(self, username="guest"):
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

    def get_user_permissions_by_vhost(self, username="guest", vhost='/'):
        """An individual permission of a user and virtual host."""
        vhost = quote_plus(vhost)
        path = self.end_point + "permissions/{0}/{1}".format(vhost, username)
        return self._get_data(path)

    def get_parameters(self):
        """A list of all parameters."""
        path = self.end_point + "parameters"
        return self._get_data(path)

    def get_parameters_by_component(self, component=None):
        """A list of all parameters for a given component."""
        path = self.end_point + "parameters/{0}".format(component)
        return self._get_data(path)

    def get_parameters_by_component_by_vhost(self, component=None,
            vhost='/'):
        """A list of all parameters for a given component and virtual host"""
        vhost = quote_plus(vhost)
        path = self.end_point + "parameters/{1}/{0}".format(vhost, component)
        return self._get_data(path)

    def get_parameter_for_vhost_by_component_name(self, component=None,
            parameter_name=None, vhost='/'):
        """Get an individual parameter value from a given vhost & component"""
        path = self.end_point + "parameters/{1}/{0}/{2}"
        path = path.format(quote_plus(vhost), component, parameter_name)
        return self._get_data(path)

    def get_policies(self):
        """A list of all policies"""
        path = self.end_point + "policies"
        return self._get_data(path)

    def get_policies_by_vhost(self, vhost='/'):
        """A list of all policies in a given virtual host."""
        path = self.end_point + "policies/{0}".format(quote_plus(vhost))
        return self._get_data(path)

    def get_policy_for_vhost_by_name(self, name=None, vhost='/'):
        """Information about an individual policy"""
        vhost = quote_plus(vhost)
        path = self.end_point + "policies/{0}/{1}".format(vhost, name)
        return self._get_data(path)

    def create_exchange_on_vhost(self, exchange_name=None,
            body={}, vhost='/'):
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
        vhost = quote_plus(vhost)
        path = self.end_point + "exchanges/{0}/{1}".format(vhost, exchange_name)
        return self._send_data(path, data=body)

    def create_queue_on_vhost(self, queue_name=None, body={}, vhost='/'):
        """An individual queue. To PUT a queue, you will need a body looking
        something like this:
        {
            "auto_delete":false,
            "durable":true,
            "arguments":[],
            "node":"rabbit@localnode-1"
        }
        """
        vhost = quote_plus(vhost)
        path = self.end_point + "queues/{0}/{1}".format(vhost, queue_name)
        return self._send_data(path, data=body)

    def create_vhost(self, vhost):
        """An individual virtual host. As a virtual host only has a name,
        you do not need an HTTP body when PUTing one of these."""
        path = self.end_point + "vhosts/{0}".format(quote_plus(vhost))
        return self._send_data(path)

    def create_user(self, username, body={}):
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
        return self._send_data(path, data=body)

    def grant_permissions_on_vhost(self, body={}, username=None,
            vhost='/'):
        """An individual permission of a user and virtual host. To PUT a
        permission, you will need a body looking something like this:
        {
            "configure":".*",
            "write":".*",
            "read":".*"
        }
        All keys are mandatory.
        """
        vhost = quote_plus(vhost)
        path = self.end_point + "permissions/{0}/{1}".format(vhost, username)
        return self._send_data(path, data=body)

    def update_parameter(self, component=None, body={}, parameter_name=None,
            vhost='/'):
        """An individual parameter. To PUT a parameter, you will need a body
        looking something like this:
        {
            "vhost": "/",
            "component":"federation",
            "name":"local_username",
            "value":"guest"
        }
        """
        vhost = quote_plus(vhost)
        path = "parameters/{1}/{0}/{2}".format(vhost, component, parameter_name)
        return self._send_data(path, data=body)

    def update_policies(self, policy_name=None, body={}, vhost='/'):
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
        vhost = quote_plus(vhost)
        path = self.end_point + "policies/{0}/{1}".format(vhost, policy_name)
        return self._send_data(path, data=body)

    def delete_connection(self, name=None, reason=None):
        """Removes a connection by name, with an optional reason"""
        path = self.end_point + "connections/" + name
        self._send_data(path, request_type='DELETE')

    def delete_exchange(self, exchange_name=None, vhost='/'):
        """Delete an exchange from a vhost"""
        vhost = quote_plus(vhost)
        path = self.end_point + "exchanges/{0}/{1}".format(vhost, exchange_name)
        self._send_data(path, request_type='DELETE')

    def delete_queue(self, queue_name=None, vhost='/'):
        """Delete a queue from a vhost"""
        vhost = quote_plus(vhost)
        path = self.end_point + "queues/{0}/{1}".format(vhost, queue_name)
        self._send_data(path, request_type='DELETE')

    def delete_contents_from_queue(self, queue_name=None, vhost='/'):
        """Delete the contents of a queue. If no vhost name is given the
        defult / will be used"""
        path = self.end_point + "queues/{0}/{1}/contents"
        path = path.format(quote_plus(vhost), queue_name)
        self._send_data(path, request_type='DELETE')

    #def delete_thing(self):
    #    """An individual binding between an exchange and a queue. The props
    #    part of the URI is a "name" for the binding composed of its routing
    #    key and a hash of its arguments."""

    def delete_vhost(self, vhost):
        """Delete a given vhost"""
        path = self.end_point + "vhosts/{0}".format(quote_plus(vhost))
        self._send_data(path, request_type='DELETE')

    def delete_user(self, user=None):
        """Delete a given user"""
        path = self.end_point + "users/{0}".format(user)
        self._send_data(path, request_type='DELETE')
