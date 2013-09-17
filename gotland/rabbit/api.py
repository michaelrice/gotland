import urllib2
import json


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
        path = self.end_point + "overview"
        data = {}
        try:
            response = urllib2.urlopen(path)
            data = json.loads(response.read())
        except:
            return None
        return data

    def get_nodes(self):
        path = self.end_point + "nodes"
        data = []
        try:
            response = urllib2.urlopen(path)
            data = json.loads(response.read())
        except:
            return None
        return data

if __name__ == "__main__":
    mytest = api()
    print mytest.check_aliveness()
    print mytest.get_overview()
    print mytest.get_nodes()
