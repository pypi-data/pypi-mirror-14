# oopyconnector : python framework for connecting to the Only Once API
#
#
# Author(s)     :   - Henri Kuiper
#
#
# Version       : 1.0beta

import requests
import datetime


class OO():

    apibase = ""

    baseurl  = "http://api.beta.onlyonce.com"
    version  = "v1"

    seckey   = None
    apisec   = None
    apikey   = None

    bearer   = None

    network  = []
    cardsReceived = []

    lastCardSync = None

    def connect(self):
        self.apibase  = self.baseurl + "/" +  self.version
        if not self.bearer:
            raise Exception, "No bearer token present, use register first"


    def cardsAge(self):
        '''Returns time since last cards-sync in seconds. Returns 9999 if no
        sync has been performed yet'''
        if lastCardSync == None:
            return 9999
        else:
            return (datetime.datetime.now() - lastCardSync).seconds

    def cards(self, maxAge=60):
        self.apibase  = self.baseurl + "/" +  self.version
        '''Returns all cards shared with me. Saves API calls by not refreshing
        within maxAge seconds'''


        if self.cardsAge > maxAge:
            headers = {
                'content-type': "application/json",
                'authorization': self.bearer,
                'cache-control': "no-cache"
            }

            response = requests.request("GET", self.apibase + "/cards" , headers=headers)
            j = response.json()
            self.cardsReceived = []
            for card in j['data']:
                c = {}
                c['owner'] = card['ownerId']
                c['name'] = card['name']
                c['id'] = card['id']
                self.cardsReceived.append(c)
            self.lastCardSync = datetime.datetime.now()

        return self.cardsReceived

    def connections(self):
        '''Returns a list of all unique users who have shared data with you.
        Returns empty list if no data shared with you, or you have not called 'cards' yet
        '''
        connections = []
        for card in self.cardsReceived:
            if card['owner'] not in connections:
                connections.append(card['owner'])
        return connections



    def card(self, cardid, seckey=None):
        '''Returns the full card JSON'''
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

    def parseFields(self, c):
        '''Recursive Parsing of all fields on a card'''
        fields = []
        for cc in c:
            if cc.has_key('components'):
                return (self.parseFields(cc['components']))
            else:
                fields.append(cc)
        return fields


    def cardFields(self, c):
        '''Return flat-JSON with all fields on card, their
        type and their value'''
        return self.parseFields(c['data']['model'])

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







