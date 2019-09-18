import urllib

from annoncestracker import settings
import urllib.request as ur
import urllib.parse



class Verify(object):
    '''builds result, results, response'''

    def __init__(self, tx):
        post = dict()
        post['cmd'] = '_notify-synch'
        post['tx'] = tx
        post['at'] = settings.PAYPAL_PDT_TOKEN
        with ur.urlopen(settings.PAYPAL_PDT_URL, urllib.parse.urlencode(post).encode("utf-8")) as url:
            self.response = url.read()
        # self.response = ur.urlopen(settings.PAYPAL_PDT_URL, urllib.parse.urlencode(post)).read()
        self.response = self.response.decode()
        print("++++++++++++++++")
        print(self.response)
        print("++++++++++++++++")

        lines = self.response.split('\n')
        self.result = lines[0].strip()
        self.results = dict()
        for line in lines:
            print(line)
        for line in lines[1:]:  # skip first line
            linesplit = line.split('=', 2)
            if len(linesplit) == 2:
                self.results[linesplit[0].strip()] = ur.unquote(linesplit[1].strip())

    def success(self):
        return self.result == 'SUCCESS' and self.results['payment_status'] == 'Completed'