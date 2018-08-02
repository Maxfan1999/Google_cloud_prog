import datetime
import os
import base64
import json
import requests

class Token:
    def __init__(self):
        self._data = None   # time getting key (token)
        # this field get from google cloud by command: gcloud auth application-default print-access-token
        # token is not valid after 60 min
        self._token = ''
        # defining feature of token for reply
        self._mask = 'ya29.'   # prefix of token
        self._len = 130   # len of token

        self._message = None   # Not used
        self._code = None     # Not used
        self._reply = None   # Not used

    def new_token(self):
        print("Getting new key...")  # debug message
        answer = os.popen("gcloud auth application-default print-access-token")
        key = answer.read().replace('\n', '')
        if self._mask in key and len(key) == self._len:
            self._token = key
            self._data = datetime.datetime.now()
            return True
        else:
            self._token = ''
            return False

    def valid(self):   # return true if token valid, not old, return false other and empty token other ways
        if self._token != '':
            if datetime.datetime.now() - self._data < datetime.timedelta(minutes=60):
                return True
            else:
                self._token = ''
                return False
        else:
            return False

    def get_token(self):   # return valid token, empty string else
        if self.valid():
            return self._token
        else:
            self.new_token()
            return self._token


class Request:
    def __init__(self):
        self._token = Token()
        self._logged = False
        self._headers = {'Authorization': 'Bearer ', 'Content-Type': 'application/json'}

    def _insert_token(self,token):
        self._headers["Authorization"] = 'Bearer ' + token

    def login(self):
        print("Login start\n")
        os.system("gcloud auth application-default login")
        print("Login end\n")
        self._logged = True

    def is_logged(self):
        return self._logged

    def req_post(self,url,structure):
        key = self._token.get_token()
        if key == '':
            answer = "Can't get key"
        else:
            self._insert_token(key)
            print("A request is sent...")
            response = requests.post(url, json=structure, headers=self._headers)
            answer = response.json()
        return answer

    """def load(self, file):
        try:
            if os.path.exists(file):
                if os.path.splitext(file)[1] == '.json':
                   with open(file, 'r') as f:
                       conf = json.load(f)
                   self._config = conf
                   return True
                else:
                    print("Uncorect file")
                    return False
            else:
                print("File doesn't exist")
                return False
        except Exception as e:
            print(e)
            print("Uncorect values in json-file")
            return False"""

    def check_log(self):
        file = os.popen('gcloud auth list')
        print(file.read())

    def settings(self):
        pass





if __name__ == "__main__":
    file = 'E:\p2.flac'
    with open(file, 'rb') as f:
        str = f.read()
    print('Begin decod...', end=' ')
    enc = base64.b64encode(str)
    print('End decod')

    sptext = Request()
    sptext.load('config.json')
    print(sptext.request(enc))



