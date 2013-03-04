from flask import Flask, request
from hashlib import sha1
import os

app = Flask(__name__)
users = {'username':'password'}

@app.route("/delete/<username>/<password>/<file>")
def delete(username, password, file):
    if login(username, password):
        os.remove("files/"+file)
        return "Success"
    return "Login Failed"

@app.route("/upload/<username>/<password>/<file>", methods=['POST'])
def upload(username, password, file, data):
    if login(username, password):
        f = request.files[file]
        if file not in os.listdir("files"):
            f.save("files/"+file)
        else:
            upload = open("files/"+file, 'ab')
            upload.write(f.read())
            upload.close()
        return "Success"
    return "Login Failed"

@app.route("/download/<username>/<password>/<file>")
def download(username, password, file):
    if login(username, password):
        with open("files/"+file, 'rb') as file:
            return file.read()
    return "Login Failed"
        
@app.route("/list/<username>/<password>")
def list(username, password):
    if login(username, password):
        return str(os.listdir("files"))
    return "Login Failed"

def login(username, password):
    if username in users and sha1(users[username]).hexdigest() == password:
        return True
    return False

if __name__ == "__main__":
    if "files" not in os.listdir(os.getcwd()):
        os.mkdir("files")
    app.run(host='0.0.0.0')
