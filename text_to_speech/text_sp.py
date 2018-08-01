import os
import sys
import base64
from classes import Request
import json


def test():
    print("Testing mode...\n")

    print("Testing Google SDK...")
    command = "gcloud --help"
    file = os.popen(command)
    if file.read() == '':
        print("Problem with Google SDK!\n")
    else:
        print("Good!\n")

    print("Testing environment variable ...")
    command = "echo %GOOGLE_APPLICATION_CREDENTIALS%"
    file = os.popen(command)
    path = file.read().replace("\n", '')
    print('GOOGLE_APPLICATION_CREDENTIALS=' + path)
    if "%GOOGLE_APPLICATION_CREDENTIALS%" in file.read():
        print("Problem with environment variable\n")
    else:
        print("Good!\n")
    print("Testing is over")


def execute(index):
    global request
    with open('config.json', 'r') as f:
        conf = json.load(f)
    if index == "l":
        request.login()
    elif index == "c":
        request.check_log()
    elif index == "t":
        test()
    elif index == '':
        pass
    else:
        structure = {
        "input": {
                "text": index
            }
        }
        structure.update(conf)
        dic = request.req_post('https://texttospeech.googleapis.com/v1beta1/text:synthesize',structure)
        content = dic['audioContent']
        b = bytes(content, encoding="utf-8")
        file = base64.b64decode(b)
        with open('result.mp3', 'wb') as f:
            f.write(file)


if __name__ == "__main__":
    request = Request()
    conf = sys.argv[1]
    if True:
        while True:
            print("Logged", request.is_logged())
            index = input("Enter key: ")
            if index == 'q':
                break
            else:
                execute(index)
