from melipayamak import Api
import requests


username = '09920970954'
password = 'Y$@M4'
api = Api(username, password)
sms = api.sms()
_from = '50004001970954'


def send_sms(data):
    response = requests.post('https://console.melipayamak.com/api/send/shared/8eeaefd8aff34b6d8b51e3f032bd99c9',
                             json=data)
    print(response.json())


