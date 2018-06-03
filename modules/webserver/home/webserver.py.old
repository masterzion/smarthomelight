import os,sys,inspect,json, hashlib
import tornado.ioloop
import tornado.web

from shutil import copyfile

# import from parent directory
root = os.path.dirname(__file__)
os.chdir(root)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from models import Sensors

PORT=80
CRON_PREFIX="ROOMBA_"
ROOMBA_CRON_DIR=root+"/../roomba/cron/"
ETC_CRON_DIR="/etc/cron.d/"

PASS=os.environ["WEATHER_SERVER_PWD"]
SALT=os.environ["WEATHER_SERVER_SALT"]
FILE_CINEMAMODE=os.environ["FILE_CINEMAMODE"]



#generate javascript salt file
file = open('js/salt.js', 'w')
file.write(" salt='"+SALT+"';")
file.close()

def CheckPass(SELF):
  STR = SELF.get_secure_cookie("password")
  return CheckPassStr(STR)

def CheckPassStr(STR):
  return STR == hashlib.md5(PASS+SALT.encode('utf-8')).hexdigest()

class TempLast(tornado.web.RequestHandler):
    def get(self):
        if CheckPass(self):
           data = Sensors().getLast();
           self.write(json.dumps(data))

class TempDay(tornado.web.RequestHandler):
    def get(self):
        if CheckPass(self):
           data = Sensors().getDay()
           self.write(json.dumps(data))

class RoombaStatus(tornado.web.RequestHandler):
    def get(self):
        if CheckPass(self):
            self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            data=[]    
            for filename in os.listdir(ROOMBA_CRON_DIR):
                target_file=ETC_CRON_DIR+CRON_PREFIX + filename
                source_file=ROOMBA_CRON_DIR+filename

                if os.path.exists(target_file):
                     data.append([filename, True])
                else:
                     data.append([filename, False])
            self.write(json.dumps(data))

class ProjectorStatus(tornado.web.RequestHandler):
    def get(self):
        if CheckPass(self):
            self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            if os.path.exists(FILE_CINEMAMODE):
               self.write('1')
            else:
               self.write('0')
            
            
class ProjectorSwitch(tornado.web.RequestHandler):
    def get(self):
        if CheckPass(self):
          if os.path.exists(FILE_CINEMAMODE):
             os.remove(FILE_CINEMAMODE)
          else:
             open(FILE_CINEMAMODE, 'w').close()
          self.write('ok')

class RoombaSwitch(tornado.web.RequestHandler):
    def get(self):
        data=[]
        filename = self.get_argument('filename', '')
        
        if filename == '':
            self.write('error')        
        else :
            target_file=ETC_CRON_DIR+CRON_PREFIX + filename
            source_file=ROOMBA_CRON_DIR+filename

            if os.path.exists(target_file):
                 os.remove(target_file)
            else:
                 copyfile(source_file, target_file)

            self.write('done')


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("password")

class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        PARAM=tornado.escape.xhtml_escape(self.password)
        if CheckPass(self):
           self.redirect("/index.html")        
        else:
            self.redirect("/login")


class LoginHandler(BaseHandler):
    def get(self):
        if CheckPass(self):
           self.redirect("/home.html")
        else:
           self.redirect("/index.html")

    def post(self):
        PARAM=self.get_argument("password")
        if CheckPassStr(PARAM):
           self.set_secure_cookie("password", PARAM)
           self.redirect("/home.html")
        else:
           self.set_secure_cookie("password", '')
           self.redirect("/index.html")


class NoCacheStaticFileHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
      self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

application = tornado.web.Application([
    (r"/roomba_status/", RoombaStatus),
    (r"/roomba_switch/", RoombaSwitch),
    (r"/projector_status/", ProjectorStatus),
    (r"/projector/", ProjectorSwitch),
    (r"/last/", TempLast),
    (r"/day/", TempDay),
    (r"/", LoginHandler),
    (r"/(.*)",  NoCacheStaticFileHandler, {"path": root, "default_filename": "index.html"}),
], cookie_secret="MY_BIG_SECRET")


if __name__ == '__main__':
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
