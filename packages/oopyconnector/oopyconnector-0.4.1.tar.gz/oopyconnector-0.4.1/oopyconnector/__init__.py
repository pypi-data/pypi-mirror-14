# oopyconnector : python framework for connecting to the Only Once API
#
#
# Author(s)     :   - Henri Kuiper
#
#
# Version       : 1.0beta

import requests


class OO():

    apibase = ""

    baseurl  = "http://api.beta.onlyonce.com"
    version  = "v1"

    seckey   = None
    apisec   = None
    apikey   = None

    bearer   = None

    def connect(self):
        self.apibase  = self.baseurl + "/" +  self.version
        if not self.bearer:
            raise Exception, "No bearer token present, use register first"


    def cards(self):
        self.apibase  = self.baseurl + "/" +  self.version
        '''Returns all cards shared with me'''

        headers = {
            'content-type': "application/json",
            'authorization': self.bearer,
            'cache-control': "no-cache"
        }

        response = requests.request("GET", self.apibase + "/cards" , headers=headers)
        j = response.json()
        cards = []
        for card in j['data']:
            c = {}
            c['owner'] = card['ownerId']
            c['name'] = card['name']
            c['id'] = card['id']
            cards.append(c)
        return cards

    def card(self, cardid, seckey=None):
        if not seckey:
            raise Exception, "You need to provide your secret key for us to decrypt your data"
        self.apibase  = self.baseurl + "/" +  self.version
        headers = {
            'content-type': "application/json",
            'authorization':  self.bearer,
            'Secret-Key': seckey,
            'cache-control': "no-cache"
            }

        response = requests.request("GET", self.apibase + "/cards/" + cardid, headers=headers)
        if response.status_code == 200:
            return response.json()


    def register(self):
        self.apibase  = self.baseurl + "/" +  self.version
        if not self.apikey:
            raise Exception, "Cannot connect without you API-key. Unable to register"
        if not self.apisec:
            raise Exception, "Cannot connect without you API-secret. Unable to register"

        payload = "{\"apiSecret\" : \"" + self.apisec + "\",\n \"apiKey\" : \"" + self.apikey + "\"\n}"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", self.apibase + "/token", data=payload, headers=headers)
        self.bearer = response.headers['Authorization']
        return True






