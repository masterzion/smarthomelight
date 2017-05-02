import os,sys,inspect
import tornado.ioloop
import tornado.web
import json
from shutil import copyfile

# import from parent directory
root = os.path.dirname(__file__)
os.chdir(root)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from models import Sensors

CRON_PREFIX="ROOMBA_"
ROOMBA_CRON_DIR=root+"/../roomba/cron/"
ETC_CRON_DIR="/etc/cron.d/"

print ROOMBA_CRON_DIR

port = 8889
class TempLast(tornado.web.RequestHandler):
    def get(self):
        data = Sensors().getLast();
        self.write(json.dumps(data))

class TempDay(tornado.web.RequestHandler):
    def get(self):
      data = Sensors().getDay()
      self.write(json.dumps(data))

class RoombaStatus(tornado.web.RequestHandler):
    def get(self):
        data=[]    
        for filename in os.listdir(ROOMBA_CRON_DIR):
            target_file=ETC_CRON_DIR+CRON_PREFIX + filename
            source_file=ROOMBA_CRON_DIR+filename

            if os.path.exists(target_file):
                 data.append([filename, True])
            else:
                 data.append([filename, False])

        self.write(json.dumps(data))


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



application = tornado.web.Application([
    (r"/roomba_status/", RoombaStatus),
    (r"/roomba_switch/", RoombaSwitch),
    (r"/last/", TempLast),
    (r"/day/", TempDay),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": root, "default_filename": "index.html"}),
])


if __name__ == '__main__':
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
