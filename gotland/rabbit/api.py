import urllib2
import json


class api():

    def __init__(self, end_point="http://localhost:15672/api/",
            user_name="guest", password="guest"):
        """foo"""
        self.end_point = end_point
        passmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passmgr.add_password(None, end_point, user_name, password)
        authhandler = urllib2.HTTPBasicAuthHandler(passmgr)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)

    def check_aliveness(self, vhost="%2f"):
        path = self.end_point + "aliveness-test/" + vhost
        data = None
        try:
            response = urllib2.urlopen(path)
            data = json.loads(response.read())

        except urllib2.URLError as e:
            print e.reason
            print e.code

        if data.get("status") != "ok":
            return False
        return True

if __name__ == "__main__":
    mytest = api()
    mytest.check_aliveness()
