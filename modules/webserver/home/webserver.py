import os,sys,inspect,json, hashlib, socket, json
import tornado.ioloop
import tornado.web

from shutil import copyfile

split = sys.argv

MEMDB_PORT=int(split[1])
WEB_PORT=int(split[2])
PASS=os.environ["WEATHER_SERVER_PWD"]
SALT=os.environ["WEATHER_SERVER_SALT"]

#generate javascript salt file
file = open('js/salt.js', 'w')
file.write(" salt='"+SALT+"';")
file.close()

def DBSendText(text):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', MEMDB_PORT))
    s.send(text)
    data = s.recv(1024)
#    print text+ ':'+data
    s.close()
    return data.strip()

def DBList(table):
    return DBSendText('L '+table)

def DBGet(table, module, item):
    return DBSendText('G '+table + ' ' + module + ' ' + item)

def DBSet(table, module, item, value):
    return DBSendText('S '+table + ' ' +  module + ' ' + item + ' ' + value)


class ModulesGetValue(tornado.web.RequestHandler):
    #TODO: check modules.conf
    def get(self, modules, item):
#        print "get:" + modules + '|'+ item
        if CheckPass(self):
            data = DBGet('VALUES', modules, item )
            self.write( data  )

class ModulesSetStatus(tornado.web.RequestHandler):
    #TODO: check modules.conf
    def get(self, modules, item, status):
#        print "set:" + modules + '|'+ item+ '|' +status
        if CheckPass(self):
            if status == '1':
                action='web_servicemanager_start'
            else:
                action='web_servicemanager_stop'
                


            values=DBGet('VALUES', 'webserver', item)
            if modules == '0':
                self.write( DBSet('VALUES', 'webserver', action , modules+'/'+item ) )
            else:
                self.write(  DBSet('VALUES', 'webserver', action , modules+'/'+item+';'+values ) )


def CheckPass(SELF):
  str = SELF.get_secure_cookie("password")
  return CheckPassStr(str)

def CheckPassStr(str):
  return str == hashlib.md5(PASS+SALT.encode('utf-8')).hexdigest()


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


class ListHome(tornado.web.RequestHandler):
    def get(self):
        if CheckPass(self):
            with open('header.html', 'r') as f:
                header = f.read()
                
            with open('footer.html', 'r') as f:
                footer = f.read()
                
            header = header.replace('{header}', "- Home")
            header += '<div class="group"><ul id="horizontal-list">'
            footer = '</ul></div>'+footer
                
            f = open('../modules.conf')
            ln = f.readline()
            ar_items = []
            while ln:
                line=ln.strip()
                if not line == "":
#                    print line
                    if not line[:1] == "#":
                        menu_item=line.split(';')[0].split(':')[1]
#                        print "==="+menu_item+"==="
                        if menu_item not in ar_items:
                            ar_items.append(menu_item)
                ln = f.readline()
            f.close()
               

            data=""                   
            for item in ar_items:
                img='/icons/'+item+'.png'
                if not os.path.isfile("./"+img):
                    img='/icons/logo.png'
                data +='<li><span><a href="module/'+item+'"><img src="'+img+'" width="150" height="150"   /></a></span>'
                data +='<span>'+item+'</span></li>'



            self.write( header + data + footer  )
        else:
           self.redirect("/index.html")
          

class ListItem(tornado.web.RequestHandler):
    def get(self, menu):
        if CheckPass(self):
#            print menu

            with open('header.html', 'r') as f:
                header = f.read()
                
            with open('footer.html', 'r') as f:
                footer = f.read()
            header = header.replace('{header}', "- " + menu)
            data=""

            f = open('../modules.conf')
            ln = f.readline()
            ar_items = []
            ar_modules = []
            ar_values = []
            while ln:
                line=ln.strip()
                if not line == "":
#                    print line
                    if not line[:1] == "#":
                        info, module = line.split(';')
                        menuname=info.split(':')[1]
#                        print "==="+menuname+"==="
                        if menuname == menu:
                            if menuname not in ar_items:
                                ar_module = module.split(':')
                                ar_modules.append([ar_module[0],ar_module[1]])
                                if len(ar_module) == 2:
                                    val = DBGet('PIDS', ar_module[0], ar_module[1] )
                                    ar_items.append(info.split(':')[2])
                                    ar_values.append(not val in ["0", ""])
                                else:
                                    val = DBGet('VALUES', ar_module[0], ar_module[1] )
                                    if ar_module[2] == "R,Float":
                                        ar_items.append(info.split(':')[2])
                                        ar_values.append(float(val))
                                    elif ar_module[2] == "R,Bool":
                                        ar_items.append(info.split(':')[2])
                                        ar_values.append(bool(val))
                                    elif ar_module[2][0] == "F":
                                       filename=ar_module[2].split(',')[1]
                                       with open(filename, 'r') as fhtml:
                                            content= fhtml.read()
                                       ar_items.append(info.split(':')[2])
                                       ar_values.append(content)

                ln = f.readline()
            f.close()
            
#            print ar_items
#            print ar_values
            for n in range(0, len(ar_items)) :
                item=ar_items[n]
                module, moduleitem=ar_modules[n]
                patch=module+'/'+item
                if isinstance(ar_values[n], bool):
                    if ar_values[n] :
                        ischecked=" checked " 
                    else:
                        ischecked="" 
                    data += '<div id="checklist"><ul class="checklist"><li><label class="textleft" for="status">'+item+'</label><input type="checkbox" id="chk_status_'+item+'" data-on="ON" data-off="OFF" onchange="switchitem(this,"'+patch+'")" '+ischecked+'/></li></ul></div>'+"\n"
                if isinstance(ar_values[n], float):
                    integer, decimal =  str(round(ar_values[n], 2)).split('.')
                    data += '<div class="content"><div class="thermometers"><div class="de"><div class="den"><div class="dene"><div class="denem"><div class="deneme">'
                    data += '<label id="currenttemp_int">'+integer+'</label><span>. <label id="currenttemp_int_decimal">'+decimal+'</label></span><strong>&deg;</strong>'
                    data += '</div></div></div></div></div></div></div>'+"\n\n"
                    

                if isinstance(ar_values[n], str):
                    data += item+' '+ar_values[n]

            data = '<div id="page" class="page"><form method="post" action="./" id="frm"><div id="items" class="items">'+"\n"+data+'</div></form></div>'+"\n"


            self.write( header + data + footer  )
        else:
           self.redirect("/index.html")




class LoginHandler(BaseHandler):
    def get(self):
        if CheckPass(self):
           self.redirect("/home")
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
    (r"/getmodules/(.*)/(.*)", ModulesGetValue),
    (r"/setmodules/(.*)/(.*)/(.*)", ModulesSetStatus),
    (r"/module/(.*)", ListItem),
    (r"/home", ListHome),
    (r"/", LoginHandler),
    (r"/(.*)",  NoCacheStaticFileHandler, {"path": "./", "default_filename": "index.html"}),
], cookie_secret="MY_BIG_SECRET")

if __name__ == '__main__':
    application.listen(WEB_PORT)
    tornado.ioloop.IOLoop.instance().start()
