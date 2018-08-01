import os
import json
import base64
import datetime
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
        self._config = {}
        self._logged = False

    def login(self):
        print("Login start\n")
        COMMAND = "gcloud auth application-default login"
        os.system(COMMAND)
        print("Login end\n")
        self._logged = True

    def is_logged(self):
        return self._logged

    def request(self,bytes):
        str_bytes = bytes.decode()

        structure = {
            "config": self._config,
            "audio": {
                "content": str_bytes
            }
        }
        key = self._token.get_key()
        if key =='':
            answer = "Can't get key"
        else:
            command = """
curl -s -H "Content-Type: application/json" -H "Authorization: Bearer {}" https://speech.googleapis.com/v1/speech:recognize -d @sync-request_base64.json""".format(key)
            json_file = os.path.dirname(os.path.abspath(__file__)) + "\sync-request_base64.json"
            with open(json_file, 'w') as json_file:
                req_dic = json.dump(structure, json_file, indent=2)

            print("A request is sent...")
            answer = os.system(command)
        return answer

    def load(self,file):
        try:
            if os.path.exists(file):
                if os.path.splitext(file)[1]=='.json':
                   with open(file,'r') as f:
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
            return False

    def check_log(self):
        file = os.popen('gcloud auth list')
        print(file.read())

    def settings(self):
        pass



TEXT = 'I love you'

structure = {
    'input': {
      'text': TEXT
    },
    'voice': {
      'languageCode': 'en-gb',
      'name': 'en-GB-Standard-A',
      'ssmlGender': 'FEMALE'
    },
    'audioConfig': {
      'audioEncoding': 'MP3'
    }
  }

token = Token()



hed = {'Authorization' : 'Bearer ' + token.get_token(), 'Content-Type' : 'application/json'}

url = 'https://texttospeech.googleapis.com/v1beta1/text:synthesize'

print("A request is sent...")

response = requests.post(url, json=structure, headers=hed)

dic = response.json()
content = dic['audioContent']
b = bytes(content,encoding="utf-8")
file = base64.b64decode(b)
with open('result.mp3','wb') as f:
    f.write(file)



