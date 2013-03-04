import urllib
import urllib2
import time
import os
import getpass
import thread
import sys
from hashlib import sha1, md5

class MatchBoxClient:

    def __init__(self):
        self.url = raw_input("URL: ")
        self.username = raw_input("Username: ")
        self.password = getpass.getpass("Password: ")
        self.password = sha1(self.password).hexdigest()
        self.url_mask = self.url+"/%s/"+self.username+"/"+self.password+"/%s"
        self.files = {}
        self.verify_username_password()
        thread.start_new_thread(self.shell, ())
        self.main_loop()

    def main_loop(self):
        while True:
            try:
                time.sleep(1)
                url = self.url_mask % ('list', '')
                this_dir = os.listdir(os.getcwd())
                that_dir = eval(urllib.urlopen(url).read())
                if str(this_dir) != str(that_dir):
                    for this in this_dir:
                        if this not in self.files and this != sys.argv[0]:
                            with open(this, 'rb') as md5file:
                                print "added", this
                                self.files[this] = md5(md5file.read()).hexdigest()
                        if this not in that_dir and this != sys.argv[0]:
                            thread.start_new_thread(self.upload, (this,))
                    for that in that_dir:
                        if that not in this_dir:
                            thread.start_new_thread(self.download, (that,))
                    for file in self.files:
                        try:
                            with open(file, 'rb') as check_file:
                                check = md5(check_file.read()).hexdigest()
                                if check != self.files[file]:
                                    print file, "changed"
                                    url = self.url_mask % ('delete', file)
                                    urllib.urlopen(url)
                                    self.files[file] = check
                                    thread.start_new_thread(self.upload, (file,))
                        except IOError:
                            pass
            except IOError:
                print "It seems as though your server is down, please check it."
                time.sleep(60)

    def upload(self, file):
        with open(file, 'rb') as upload:
            print "Uploading", file
            url = self.url_mask % ('upload', file)
            params = {'file': file, 'data': upload}
            request = urllib2.Request(url)
            request.add_data(params)
            urllib2.urlopen(request)
        print "Done uploading", file

    def download(self, file):
        with open(file, 'wb') as download:
            print "Downloading", file
            url = self.url_mask % ('download', file)
            download.write(url)
        print "Done downloading", file

    def delete(self, file):
        os.remove(file)
        del self.files[file]
        url = self.url_mask % ('delete', file)
        urllib.urlopen(url)

    def shell(self):
        while True:
            cmd = raw_input('> ')
            if cmd.startswith("rm"):
                cmd = cmd.split()
                if cmd[1] not in os.listdir(os.getcwd()):
                    print "File doesn't exist"
                elif cmd[1] == sys.argv[0]:
                    print "Don't delete MatchBox!"
                else:
                    thread.start_new_thread(self.delete, (cmd[1],))
            if cmd == "ls":
                print os.listdir(os.getcwd())

    def verify_username_password(self):
        url = self.url_mask % ('list', '')
        if urllib.urlopen(url).read() == "Login Failed":
            print "Username or password not correct."
            exit()
        
if __name__ == "__main__":
    MatchBoxClient()
