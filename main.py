import rumps
import requests
import os
import urllib.request

def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

class QBotCheckerApp(object):
    def __init__(self):
        self.isCrashed = 0
        self.app = rumps.App("Q-Bot Watcher", "◽️")
        self.status_title = rumps.MenuItem(title="Q-Bot Status :", callback=None)
        self.status = rumps.MenuItem(title="---", callback=None)
        self.app.menu = [self.status_title, self.status]
        self.refresh_status
        self.refresh_loop = rumps.Timer(self.refresh_status, 20)
        self.refresh_loop.start()

    def refresh_status(self, sender):
        if connect():
            r = requests.get('https://iwa.sh/qbot')
            if r.status_code == 200:
                self.status.title = "online"
                self.app.title = "🔷"
                if(self.isCrashed == 1):
                    self.isCrashed = 0
                    #os.system('pm2 del qbot-fallback')
            elif r.status_code == 404:
                self.status.title = "crashed"
                self.app.title = "🔶"
                if(self.isCrashed == 0):
                    self.isCrashed = 1
                    rumps.notification(title="Q-Bot Crashed!", subtitle="Fallback version launched", message='')
                    #os.system('cd /Users/iwa/dev/node/Q-Bot-fallback && pm2 start . -n qbot-fallback')
            else:
                self.status.title = "there's a problem"
                self.app.title = "🛑"
        else:
            self.status.title = "no connection"
            self.app.title = "◽️"

    def run(self):
        self.app.run()

if __name__ == '__main__':
    QBotCheckerApp().run()