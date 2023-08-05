import requests


class Echo():
    def doit(self, value):
        #print "Hello World"
        return value

    def do_request(self):
        r = requests.get("http://demo.jmbo.org/api/v1/listing/1/?format=json")
        # Prior to reauests 1.0 json was a property
        json = r.json
        if callable(json):
            return json()
        else:
            return json
