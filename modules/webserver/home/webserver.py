import os,sys,inspect,json, hashlib, socket
import tornado.ioloop
import tornado.web

from shutil import copyfile

# import from parent directory
root = os.path.dirname(__file__)
os.chdir(root)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

PORT=80

PASS=os.environ["WEATHER_SERVER_PWD"]
SALT=os.environ["WEATHER_SERVER_SALT"]

#MEMDB_PORT=os.environ["MEMDB_PORT"]
MEMDB_PORT=3030

#generate javascript salt file
file = open('js/salt.js', 'w')
file.write(" salt='"+SALT+"';")
file.close()

def DBConnect(TEXT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', MEMDB_PORT))
    s.send(TEXT)
    data = s.recv(1024)
    return data.strip()

def DBList(TABLE):
    return DBConnect('L '+TABLE)

def DBGet(TABLE, ITEM):
    return DBConnect('G '+TABLE + ' ' + ITEM)

def DBSet(TABLE, ITEM, VALUE):
    return DBConnect('S '+TABLE + ' ' + ITEM + ' ' + VALUE)


class ProjectorStatus(tornado.web.RequestHandler):
    def get(self):
        if CheckPass(self):
            self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            data = DBGet('ENABLED', 'Projector')
            print data
            self.write( data  )
            
            
class ProjectorSwitch(tornado.web.RequestHandler):
    def get(self):
        if CheckPass(self):
          if DBGet('ENABLED', 'Projector') == '1':
             DBSet('ENABLED', 'Projector', '0')
          else:
             DBSet('ENABLED', 'Projector', '1')
          self.write('ok')

def CheckPass(SELF):
  STR = SELF.get_secure_cookie("password")
  return CheckPassStr(STR)

def CheckPassStr(STR):
  return STR == hashlib.md5(PASS+SALT.encode('utf-8')).hexdigest()


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
    (r"/projector_status/", ProjectorStatus),
    (r"/projector/", ProjectorSwitch),
    (r"/", LoginHandler),
    (r"/(.*)",  NoCacheStaticFileHandler, {"path": root, "default_filename": "index.html"}),
], cookie_secret="MY_BIG_SECRET")

if __name__ == '__main__':
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
