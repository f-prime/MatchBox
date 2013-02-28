from flask import Flask
import os, hashlib

app = Flask(__name__)

users = {

'username':'password',

        }

@app.route("/delete/<username>/<password>/<file>")
def delete(username, password, file):
    if login(username, password) is False:
        return "Login Failed"
    else:
        os.remove("files/"+file)
        return "Success"

@app.route("/upload/<username>/<password>/<file>/<data>")
def upload(username, password, file, data):
    if login(username, password) is False:
        return "Login Failed"
    else:
        if file not in os.listdir("files"):
            os.system("touch files/"+file)
        upload = open("files/"+file, 'ab')
        data = data.split()
        for data in data:
            upload.write(chr(int(data)))
        upload.close()
        return "Success"

@app.route("/download/<username>/<password>/<file>")
def download(username, password, file):
    if login(username, password) is False:
        return "Login Failed"
    else:
        with open("files/"+file, 'rb') as file:
            return file.read()
        
@app.route("/list/<username>/<password>")
def list(username, password):
    if login(username, password) is False:
        return "Login Failed"
    else:
        return str(os.listdir("files"))

def login(username, password):
    if username not in users:
        return False
    elif hashlib.sha1(users[username]).hexdigest() == password:
        return True
    else:
        return False

if __name__ == "__main__":
    if "files" not in os.listdir(os.getcwd()):
        os.system("mkdir files")
    app.run(host='0.0.0.0')
