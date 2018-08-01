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
    elif len(index) > 5:  # это файл
        if os.path.exists(index):
            file = index
            with open(file, 'rb') as f:
                str = f.read()
            print('Begin decod...', end=' ')
            enc = base64.b64encode(str)
            print('End decod')
            str_bytes = enc.decode()

            structure = {
                "config": conf,
                "audio": {
                    "content": str_bytes
                }
            }
            print(request.req_post('https://speech.googleapis.com/v1/speech:recognize',structure))
        else:
            print("File doesn't exist")
    elif index == '':
        pass
    else:
        print("wrong key")


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
