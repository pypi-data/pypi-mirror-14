import requests

class PyScanii(object):

    key = ''
    secret = ''
    requests_session = None
    url = ''
    # EICAR test string. (Encoded to prevent host-OS false-positive)
    EICAR = 'WDVPIVAlQEFQWzRcUFpYNTQoUF4pN0NDKTd9JEVJQ0FSLVNUQU5E'.decode('base64') \
            + 'QVJELUFOVElWSVJVUy1URVNU\nLUZJTEUhJEgrSCo=\n'.decode('base64')
    # Use latency distributed endpoint by default.
    base_url = 'https://api.scanii.com'
    api_version = 'v2.1'
    verbose = False

    def __init__(self, key, secret, **kwargs):
        self.key = key
        self.secret = secret
        for key in kwargs:
            # Set kwargs to properties
            setattr(self, key, kwargs[key])

        self.requests_session = requests.Session()
        self.requests_session.auth = (self.key, self.secret)
        if self.api_version.startswith('v2'):
            self.scan_method = 'files'
        else:
            self.scan_method = 'scan'

    def _get_url(self, method):
        return '/'.join((self.base_url, self.api_version, method))

    def ping(self):
        url = self._get_url('ping')
        if self.verbose:
            print("Pinging: {}".format(url))

        r = self.requests_session.get(url)
        response = r.json()

        if self.verbose:
            print(response)

        return response

    def test(self):
        return self.scan(string=self.EICAR, filename='eicar.bin')

    def scan(self, path=None, string=None, filename='file.txt'):
        url = self._get_url(self.scan_method)
        if self.verbose:
            print("URL: {}".format(url))

        if path:
            if self.verbose:
                print("Scanning file at: {}".format(path))
            files = {'file': open(path, 'rb')}
        else:
            if self.verbose:
                print("Scanning string as filename: {}".format(filename))
            files = {'file': (filename, string)}

        r = self.requests_session.post(url, files=files)
        response = r.json()

        if self.verbose:
            print(response)

        return response
