from melipayamak import Api


username = '09920970954'
password = 'Y$@M4'
api = Api(username, password)
sms = api.sms()
_from = '50004001970954'


def send_sms(phone, text):
    to = str(phone)
    text = text
    response = sms.send(to, _from, text)
    print(response)
