import requests


class smsGateway(object):

    __baseUrl = 'https://smsgateway.me'

    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    def __makeRequest(self, url, method, fields={}):
        fields['email'] = self.__username
        fields['password'] = self.__password

        url = ''.join([self.__baseUrl,url])

        if method=='GET':
            result = {}
            r = requests.get(url, params=fields)
            result['status'] = r.status_code
            result['response'] = r.json()

            return result

        elif method=='POST':
            result = {}
            r = requests.post(url, data=fields)
            result['status'] = r.status_code
            result['response'] = r.json()

            return result

    def getDevices(self, page=1):
        return self.__makeRequest('/api/v3/devices', 'GET', {'page':page})

    def getDevice(self, id):
        url = ''.join(['/api/v3/devices/view/',str(id)])
        return self.__makeRequest(url , 'GET')

    def getContacts(self, page=1):
        return self.__makeRequest('/api/v3/contacts', 'GET', {'page':page})

    def getContact(self, id):
        url = ''.join(['/api/v3/contacts/view/', str(id)])
        return self.__makeRequest(url, 'GET')

    def getMessages(self, page=1):
        return self.__makeRequest('/api/v3/messages', 'GET', {'page':page})

    def getMessage(self, id):
        url = ''.join(['/api/v3/messages/view/', str(id)])
        return self.__makeRequest(url, 'GET')

    def createContact(self, name, number):
        return self.__makeRequest('/api/v3/contacts/create', 'POST', {'name':name, 'number':number})

    def sendMessageToNumber(self, to, message, device, options={}):
        options.update({'number':to,
                        'message':message,
                        'device':device})
        return self.__makeRequest('/api/v3/messages/send', 'POST', options)

    def sendMessageToManyNumbers(self, to, message, device, options={}):
        options.update({'number':to,
                        'message':message,
                        'device':device})
        return self.__makeRequest('/api/v3/messages/send', 'POST', options)

    def sendMessageToContact(self, to, message, device, options={}):
        options.update({'contact':to,
                        "message":message,
                        'device':device})
        return self.__makeRequest('/api/v3/messages/send', 'POST', options)

    def sendMessageToManyContact(self, to, message, device, options={}):
        options.update({'contact':to,
                        "message":message,
                        'device':device})
        return self.__makeRequest('/api/v3/messages/send', 'POST', options)