import time,tornado.web,tornado.ioloop , json,usefull , tornado.autoreload

tornadoSessions={}


def clearSession():
    try:
        tt = time.time()
        skeys = tornadoSessions.keys()
        for i in skeys:
            print(i, "last activity", tt - tornadoSessions[i]["SessionTime"])
            if tt - tornadoSessions[i]["SessionTime"] > 60*60:
                del (tornadoSessions[i])
    except:
        pass

usefull.setInterval(clearSession,60*60)



class TornaRoute(tornado.web.RequestHandler):
    def initialize(self , level = 0):
        self.level=level+1

    def _findRoute(self,method="get"):
        global tornadoSession
        tt = time.time()
        self.sessionid=self.get_secure_cookie("_tornadoSession")
        if self.sessionid == None:
            self.sessionid=str(tt)
        else:
            self.sessionid=self.sessionid.decode()
        self.set_secure_cookie("_tornadoSession", self.sessionid)
        tornadoSession = tornadoSessions.get(self.sessionid,{})
        if tornadoSession=={}:
            tornadoSessions[self.sessionid]={"SessionTime":tt}
        else:
            tornadoSessions[self.sessionid]["SessionTime"]=tt



        uris = self.request.uri.split("/")
        para = {}
        for p in self.request.arguments:
            para[p] = self.get_argument(p)
        if len(uris)<=self.level:
            meth = "index"
        else:
            meth = uris[self.level].split("?")[0]

        if meth == "":
            meth = "index"
        meth = getattr(self, "route_" + meth, self.route_404)
        if (self.route_404 == meth):
            def job():
                meth(method, [] if len(uris) < (self.level + 1) else uris[self.level:], para)
                if not self._finished:
                    self.finish()
        else:
            def job():
                meth(method, [] if len(uris) < (self.level+1) else uris[self.level+1:], para)
                if not self._finished:
                    self.finish()
        usefull.setTimeOut(job,0)

    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        self._findRoute()

    def SESSION(self):
        return tornadoSessions[self.sessionid]

    def SESSION_set(self,key,val):
        tornadoSessions[self.sessionid][key]=val
        return val

    def SESSION_get(self,key,val=None):
        rst = tornadoSessions[self.sessionid].get(key,None)
        if rst == None:
            self.SESSION_set(key,val)
            return val
        return rst

    @tornado.web.asynchronous
    def post(self, *args, **kwargs):
        self._findRoute("post")

    @tornado.web.asynchronous
    def head(self, *args, **kwargs):
        self._findRoute("head")

    @tornado.web.asynchronous
    def put(self, *args, **kwargs):
        self._findRoute("put")

    @tornado.web.asynchronous
    def delete(self, *args, **kwargs):
        self._findRoute("delete")


    def route_404(self,method,restParams,params):
        self.send_error(404)


    def route_index(self, method, restParams,params):
        self.write("Declare :<br>def route_index(self, method, restParams,params):<br><dir>self.write('Your code here')</dir>")



def InstallLibs(spectre=False):
    import os.path, requests
    os.makedirs("./rs/js/", exist_ok=True)
    os.makedirs("./rs/fonts/", exist_ok=True)
    os.makedirs("./rs/css/", exist_ok=True)
    os.makedirs("./tp", exist_ok=True)
    if not os.path.exists("./rs/js/jquery.js"):
        open("./rs/js/jquery.js","wb").write(requests.get("https://code.jquery.com/jquery-3.2.1.min.js").content)
        open("./rs/js/jquery-ui.js", "wb").write(requests.get("https://code.jquery.com/ui/1.12.1/jquery-ui.min.js").content)
        open("./rs/css/font-awesome.min.css", "wb").write(
            requests.get("https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css").content)
        open("./rs/fonts/fontawesome-webfont.woff2", "wb").write(requests.get(
            "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/fonts/fontawesome-webfont.woff2").content)
        open("./rs/fonts/fontawesome-webfont.woff", "wb").write(requests.get(
            "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/fonts/fontawesome-webfont.woff").content)
        open("./rs/fonts/fontawesome-webfont.ttf", "wb").write(requests.get(
            "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/fonts/fontawesome-webfont.ttf").content)
        if spectre:
            open("./rs/css/spectre.min.css", "wb").write(requests.get("https://unpkg.com/spectre.css/dist/spectre.min.css").content)
            open("./rs/css/spectre-exp.min.css", "wb").write(requests.get("https://unpkg.com/spectre.css/dist/spectre-exp.min.css").content)
            open("./rs/css/spectre-icons.min.css", "wb").write(requests.get("https://unpkg.com/spectre.css/dist/spectre-icons.min.css").content)
        else:
            open("./rs/js/bootstrap.min.js", "wb").write(
                requests.get("https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js").content)
            open("./rs/css/bootstrap.min.css", "wb").write(
                requests.get("https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css").content)
            open("./rs/css/bootstrap.min.css.map", "wb").write(
                requests.get("https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css.map").content)
            open("./rs/js/bootbox.min.js", "wb").write(
                requests.get("https://cdnjs.cloudflare.com/ajax/libs/bootbox.js/4.4.0/bootbox.min.js").content)

    if not os.path.exists("./tp/base.html"):

        if spectre:
            thelib = """
            <link rel="stylesheet" href="/rs/css/spectre.min.css">
<link rel="stylesheet" href="/rs/css/spectre-exp.min.css">
<link rel="stylesheet" href="/rs/css/spectre-icons.min.css">
            """
        else:
            thelib="""
    <script type="text/javascript" src="/rs/js/bootstrap.min.js"></script>
    <script type="text/javascript" src="/rs/js/bootbox.min.js"></script>
    
    <link href="/rs/css/bootstrap.min.css" rel="stylesheet">
    """


        open("./tp/index.html", "w").write("""
{%extends base.html%}
{%block title%}Index{%end%}
{%block body%}<i class="fa fa-bullseye" aria-hidden="true"></i>
Index{%end%}""")
        open("./tp/base.html","w").write("""
<html>
  <head>
    <meta charset="UTF-8">
    <script type="text/javascript" src="/rs/js/jquery.js"></script>
    <script type="text/javascript" src="/rs/js/jquery-ui.js"></script>"""+thelib+"""
    <link href="/rs/css/font-awesome.min.css" rel="stylesheet">
    <title>{%block title%}base{%end%}</title>
  </head>
  <body>
  {%block body%}
    body
  {%end%}
  <body>
</html>
        """)


def startTornado():
    tornado.ioloop.IOLoop.current().start()
def addRestartWatch(o):
    tornado.autoreload.add_reload_hook(o)
def createWebApp(iPort,aTornaRoute,aStaticPath="rs",debug=True, StartApp=True):
    import usefull
    code = usefull.MD5(str(aTornaRoute)+str(type(aTornaRoute)))
    code+=usefull.MD5(code)
    if type(aTornaRoute) != list:
        aTornaRoute=[("(.*)",aTornaRoute)]
    confApp=[]
    for aroute in aTornaRoute:
        if aroute[0]=="" :
            host="(.*)"
        else :
            host=aroute[0]
        confApp += [(tornado.web.HostMatches(host), [("/rs/(.*)", tornado.web.StaticFileHandler, {"path": aStaticPath}),
                                                     ("/(.*)", aroute[1])])]


    tornado.web.Application(
       confApp,debug=debug,cookie_secret=code).listen(iPort)
    if StartApp:
        startTornado()