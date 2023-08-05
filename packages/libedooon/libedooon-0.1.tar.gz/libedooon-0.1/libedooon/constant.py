default_header = {
    'AppVersion': '3.1.5',
    'Accept': '*/*',
    'Accept-Language': 'zh-cn',
    'Accept-Encoding': 'gzip, deflate',
    'App': 1,
    'Content-Type': 'application/json',
    'User-Agent': 'EdooonGPS/18 CFNetwork/758.2.8 Darwin/15.0.0',
    'Connection': 'keep-alive',
    'authCode': ''
}


client_token = '2bae4e33aa2798564867886ef854fea84c466241105b079cde03a9abd53dd599'


class Endpoint:
    base = 'http://edooon.com'
    login = base + '/commInterface/v1/user/login'
    register = base + '/commInterface/v1/user/register'

    def __init__(self, auth_code):
        self.user_token = self.base + '/clientInterface/v1_1/user/{}/usertoken'.format(auth_code)
        self.update_info = self.base + '/commInterface/v1/user/userUpdate'
        self.get_info = self.base + '/commInterface/v1/user/userInfo'
        self.get_map_offset = self.base + '/commInterface/v1/lbs/mapoffset'
        self.post_comment = self.base + '/clientInterface/v1_1/sport/{}/postComment'.format(auth_code)
        self.new_activity = self.base + '/clientInterface/v1_1/sport/{}/report'.format(auth_code)
