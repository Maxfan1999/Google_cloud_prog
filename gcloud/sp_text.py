import os
import sys
import base64
from classes import Request
import json
from datetime import datetime

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
    global help_scr
    global conf
    global conf_file
    
    if index == "l":
        request.login()
    elif index == "h":
        print(help_scr)
    elif index == "c":
        request.check_log()
    elif index == "t":
        test()
    elif index == "r":
        try:
            if os.path.exists(conf_file):
                if os.path.splitext(conf_file)[1]=='.json':
                    with open(conf_file,'r') as f:
                        conf = json.load(f)
                    print("File {} is reloaded".format(conf_file))
                else:
                    print('WRONG FORMAT FILE')
            else:
                print("FILE DOESN'T EXIST")
        except Exception as e:
            print("ERROR WITH CONFIG FILE")
            print(e)
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
            dic = request.req_post('https://speech.googleapis.com/v1/speech:recognize',structure)
	    print(dic)
            name = os.path.split(index)[1]
            res_file = name[:name.index('.')] + '{}.json'.format(datetime.now().strftime("%m%d%H%M"))
            with open(res_file,'w') as f:
                json.dump(dic,f,indent=2)
        else:
            print("File doesn't exist")
    elif index == '':
        pass
    else:
        print("ERROR COMMAND")
        print(help_scr)


if __name__ == "__main__":
    name = os.path.split(__file__)[1].replace('.py','')
    request = Request()
    argv = sys.argv[1:]
    if argv != []:
        conf_file = argv[0]
    else:
        conf_file = name + ".config.json"
    try:
        if os.path.exists(conf_file):
            if os.path.splitext(conf_file)[1]=='.json':
                with open(conf_file,'r') as f:
                    conf = json.load(f)
    
                help_file = name + ".help.txt"
                with open(help_file,'r') as f:
                    help_scr = f.read()
                while True:
                    print("Logged", request.is_logged())
                    index = input("Enter command or filename to recognize: ")
                    if index == 'q':
                        break
                    else:
                        execute(index)
            else:
                print('WRONG FORMAT FILE')
        else:
            print("FILE DOESN'T EXIST")
    except Exception as e:
        print("ERROR")
        print(e)
