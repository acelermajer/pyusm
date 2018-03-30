import os, time,threading, hashlib , socket , sys


def listDict2Table(d):

    rst=d
    fs = []
    header={}
    for r in rst:
        for f in r.keys():
            if f not in fs:
                fs+=[f]
                header[f]=len(f)
            if header[f] < len(str(r[f])):
                header[f] = len(str(r[f]))
    firstLine = 1
    for r in rst:
        if firstLine:
            firstLine=0
            s=""
            for f in fs:
                print(f.center(header[f], " "), end="|")
                s +="-" * (header[f])+"|"
            print("")
            #print(s)
        for f in fs:
            print(str(r.get(f,"")).ljust(header[f], " ").replace("\n", " "), end="|")
        print("")




def getchr():
    import tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        print(fd)
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def readln():
    ln = ""
    while 1:
        c = getchr()
        if c == 13:
            print("")
            return str
        str += c
        print(c, end="")



def printr(o,indent=0):
    if type(o) in [dict,tuple,list]:
        if type(o) == dict:
            for e in o:
                print(" "*indent,e)
                printr(o[e],indent+1)
        else:
            for e in o:
                printr(e, indent + 1)

    else :
        print(" "*indent,o)

class BaseCLI():
    def start(self):
        self.CLI_Loop=True
        self.prompt=">"
        while self.CLI_Loop:
            print(self.prompt,end="",flush=True)
            s=sys.stdin.readline().strip()
            if s=="":
                self.noCommand()
                continue
            cmdLine=s.split()
            cmdLine+=['']
            m = getattr(self,"cmd_"+cmdLine[0],
                        self.commandNotFound)
            m(cmdLine)
    def noCommand(self):
        pass
    def commandNotFound(self,cmdLine):
        print(cmdLine[0],": Command not found",sep="")
    def cmd_exit(self,cmdLine):
        self.CLI_Loop=False
        print("Bye.")

def isfloat(value):
    try:
        float(value)
        return True
    except:
        return False


class LiveDebug():
    def __init__(self,port):
        self.port = port
        self.conected = False
        setTimeOut(lambda : self.start(),0)
    def start(self):
        if self.conected :
            return
        self.srv = socket.socket()
        try:
            self.srv.bind(("127.0.0.1",self.port))
            self.conected=True
            print("Ready on port ", self.port)
        except Exception as eee:
            print(eee)
            time.sleep(1)
            self.port+=1
            self.start()
            return
        self.srv.listen(5)
        while 1:
            aclient = self.srv.accept()[0]
            aclient.send(b"Live Debug Active\n")
            while 1 :
                aclient.send(b"\n>")
                buff = aclient.recv(1024*5)
                if len(buff)==0:
                    break
                buff=buff.decode().strip()
                if buff != "":
                    cmds=buff.split(" ")
                    m = getattr(self, "cmd_" + cmds[0],
                                None)
                    if m!=None:
                        #setTimeOut(lambda :m(aclient , buff[len(cmds[0]):]),0)
                        #time.sleep(1)
                        m(aclient, buff[len(cmds[0]):])
                    else:
                        aclient.send((cmds[0]+" : command not found\n").encode())

    def cmd_info(self, soc, cmd):
        soc.send((b"Info \n"))

    def cmd_echo(self, soc, cmd):
        soc.send((b"echo \n\t"))
        soc.send(cmd.encode())
        soc.send((b"\n"))


    def cmd_eval(self, soc, cmd):
        soc.send((b"Avaluating :"+cmd.encode()+b"\n"))
        try:
            soc.send(str(eval(cmd.strip())).encode())
        except Exception as eee:
            soc.send(str(eee).encode())





def str_between(txt,sfrom,send):
    return (txt+sfrom).split(sfrom)[1].split(send)[0]
def sleep(a):
    time.sleep(a)

def openBrowser(url,timeout=0):
    import sys
    setTimeOut(lambda: os.system(sys.executable + ' -m webbrowser -t "'+url+'" '), timeout)

class ServerShell():
    def do_wellcome(self, cid):
        c=self.clients[cid]["client"]
        c.send(b"Wellcome\n")
    def proceedCommand(self,cid,command,bufs):
        cmds = command.strip().split(" ")
        cmd = cmds.pop(0)
        amethod=getattr(self,"cmd_"+cmd,None)
        print("Pour la commande ",cmd, "La methode est : " ,amethod)
        if callable(amethod):
            return amethod(cid,self.clients[cid]["client"],cmds)

    def __init__(self,port):
        self.socket=socket.socket()
        self.socket.bind(("",port))
        self.clients={}
        def server():
            self.socket.listen()
            while True:
                cc=self.socket.accept()
                print("New Client ",cc)
                aClient = cc[0]
                clientID = time.time()
                self.clients[clientID]={"id":clientID,"client":aClient,"buf":""}
                def processedClient():
                    print("WellCome ",clientID)
                    self.do_wellcome(clientID)
                    while True:
                        print("Wait for data for client",clientID)
                        buf = aClient.recv(1024*10).decode(errors="ignore") # type: str
                        print({"length": len(buf), "buf": buf})
                        if len(buf)==0:
                            break
                        bufs = buf.strip().split("\n")
                        while bufs !=[]:
                            s = bufs.pop(0) #type: str
                            print("Proceed",s)
                            self.proceedCommand(clientID,s,bufs)

                        if buf.startswith(("die","DIE")):
                            aClient.close()
                            self.socket.close()
                setTimeOut(processedClient,0)

        setTimeOut(server,0)

def delFromCanvas(canvas,points):
    for p in points:
        canvas.delete(p)
def propo(a,b,c):
    return a*c+b*(1-c)
def bornInt(ival,imin=0,imax=100):
    return imin if ival<imin else imax if ival>imax else ival
def sha1(s):
    return hashlib.sha1(s.encode()).hexdigest()
def sha512(s):
    return hashlib.sha512(s.encode()).hexdigest()
def MD5(s):
    if type(s) is bytes:
        return hashlib.md5(s).hexdigest()

    return hashlib.md5(str(s).encode()).hexdigest()

def searchInFile(aFilename,search,context = 25):
    if type(search) is str:
        search=(search,)
    bigs =0;
    sr=[]
    for s in search:
        sr.append(s.upper())
        if bigs<len(s):
            bigs=len(s)+1
    f = open(aFilename,errors="ignore")
    while True:
        buff=f.read(context*2).upper()
        for s in sr:
            if buff.find(s)!=-1:
                print(s,": ",buff)

        f.seek(f.seek(0,1)-bigs)

        if len(buff)!=context*2:
            break
    f.close()

def CreateFrmCanvas(bg=[255,255,255]):
    import tkinter
    frm=tkinter.Toplevel()
    c=tkinter.Canvas(frm,bg=rgb(bg[0],bg[1],bg[2]))
    c.pack(fill=tkinter.BOTH,expand=tkinter.YES)
    return (frm,c)
def setFormScreenCenter(frm ,_size=None):

    if _size==None:
        _size=str(frm.winfo_width())+"x"+str(frm.winfo_height())
    else :
        frm.geometry(_size)
    frm.update()
    frm.geometry("+%s+%s" % (int(frm.winfo_screenwidth()//2- frm.winfo_width()//2),int(frm.winfo_screenheight()//2- frm.winfo_height()//2)))



def uf_test():
    print("usefull Test")



def dict_set(aDict , keys,val):
    cc = aDict
    for k in keys[:-1]:
        tmp = cc.get(k,None)
        if tmp==None:
            cc[k]={}
            tmp =  cc[k]
        cc = tmp
    cc[keys[-1]] = val

def dict_del(aDict,akey):
    if akey in aDict:
        del(aDict[akey])

def dict_get(aDict,akey,default=None):
    if type(akey) is list:
        dd = aDict
        for k in akey[:-1]:
            dd = dd.get(k,{})
        return dd.get(akey[-1],default)
    else:
        return aDict.get(akey,default)

def dict_add(aDict,akey,aval):
    if akey in aDict:
        aDict[akey]+=aval
    else:
        aDict[akey] = aval


def dict_inc(adict,path):
    cc = adict
    for p in path[:-1]:
        tmp = cc.get(p,None)
        if tmp == None:
            cc[p]={}
            tmp = cc[p]
        cc = tmp
    cc[path[-1]] = cc.get(path[-1],0)+1

def incDict(adict,path):
    cc = adict
    for p in path[:-1]:
        tmp = cc.get(p,None)
        if tmp == None:
            cc[p]={}
            tmp = cc[p]
        cc = tmp
    cc[path[-1]] = cc.get(path[-1],0)+1



def baseN2int(str_Num, base="0123456789"):
    str_Num=str_Num.lstrip(base[0])[::-1]
    pos=0
    rst=0
    for i in str_Num:
        rst+=base.find(i)*len(base)**pos
        pos+=1
    return rst

def int2baseN(val, b="0123456789"):
    nb = len(b)
    rst = ""
    if val == 0:
        return b[0]
    while val > 0:
        rst = b[val % nb] + rst
        val //= nb
    return rst

def showmessage(message,title="MessageBox"):
    import tkinter, threading,time
    msg = tkinter.Tk()
    msg.title(title)

    lb=tkinter.Label(msg,text=str(message))
    lb.pack(fill=tkinter.BOTH,expand=tkinter.YES)
    btn = tkinter.Button(msg,text="OK",command=lambda :msg.destroy())
    btn.pack()
    def posit():
        time.sleep(0.2)
        w = 256 if msg.winfo_width()<256 else msg.winfo_width()
        h = msg.winfo_screenheight()
        t = h / 4 if msg.winfo_height() < (h - (h/4)) else (((h - (h/4))-msg.winfo_height()))

        geo= "%dx%d+%d+%d" % (w,
                              100 if msg.winfo_height() < 100 else msg.winfo_height(),
                              (msg.winfo_screenwidth()/2)-(w/2),
                              t)
        msg.geometry(geo)

    threading.Thread(target=posit).start()
    msg.mainloop()
def rgb(r,g,b):
    return "#%02X%02X%02X" % (int(r)%256,int(g)%256,int(b)%256)
def die():
    os._exit(0)
intervalList={}
def setTimeOut(method, secodes = 1, params={}) -> object:
    def threadJob():
        if secodes!=0:
            time.sleep(secodes)
        if callable(method):
            if params!={}:
                method(params)
            else:
                method()
    threading.Thread(target=threadJob).start()
def dict2txt(dt,tab=" "):
    if type(dt)==dict:
        st=""
        for k in dt:
            st+=tab+str(k)+":\n"+dict2txt(dt[k],tab+tab[0])+"\n"
        return st
    if type(dt)==list:
        st = ""
        for k in dt:
            st+=tab+dict2txt(k,tab+tab[0])+"\n"
        return st
    return tab+str(dt)

def setInterval(method,secodes  = 1):
    if not callable(method):
        return False
    idThread = time.time()
    intervalList[idThread]=secodes
    def threadJob():
        while True:
            if idThread in intervalList:
                if method() == False:
                    break
                time.sleep(intervalList[idThread])
            else:
                break
    threading.Thread(target=threadJob).start()
    return idThread

def StopInterval(idInterval):
    dict_del(intervalList,idInterval)



def sec2hms(sec):
    sec = int(sec)
    ssec=sec % 60
    smin = (sec % (60*60))//60
    sh = (sec)//3600
    rst = "%02dH %02dm %02ds"%(sh,smin,ssec)
    return rst

def fileMD5trunk(afile,block=1024):

    f = open(afile,"rb")

    rst = []
    while True :
        b = f.read(block)

        if len(b)==0:
            break
        rst+=[MD5(b)]
    return rst
#readXlsx( "mysheet.xlsx", sheet = 1, header = True )
def readXlsx( fileName, **args ):

    import zipfile
    from xml.etree.ElementTree import iterparse

    if "sheet" in args:
       sheet=args["sheet"]
    else:
       sheet=1
    if "header" in args:
       isHeader=args["header"]
    else:
       isHeader=False

    rows   = []
    row    = {}
    header = {}

    z      = zipfile.ZipFile( fileName )

    # Get shared strings
    strings = [ el.text for e, el
                        in  iterparse( z.open( 'xl/sharedStrings.xml' ) )
                        if el.tag.endswith( '}t' )
                        ]
    value = ''

    # Open specified worksheet
    for e, el in iterparse( z.open( 'xl/worksheets/sheet%d.xml'%( sheet ) ) ):
       # get value or index to shared strings
       if el.tag.endswith( '}v' ):                                   # <v>84</v>
           value = el.text
       if el.tag.endswith( '}c' ):                                   # <c r="A3" t="s"><v>84</v></c>

           # If value is a shared string, use value as an index
           if el.attrib.get( 't' ) == 's':
               value = strings[int( value )]

           # split the row/col information so that the row leter(s) can be separate
           letter = el.attrib['r']                                   # AZ22
           while letter[-1].isdigit():
               letter = letter[:-1]

           # if it is the first row, then create a header hash for the names
           # that COULD be used
           if rows ==[]:
               header[letter]=value
           else:
               if value != '':

                   # if there is a header row, use the first row's names as the row hash index
                   if isHeader == True and letter in header:
                       row[header[letter]] = value
                   else:
                       row[letter] = value

           value = ''
       if el.tag.endswith('}row'):
           rows.append(row)
           row = {}
    z.close()
    return rows
def dict_print(adict,indent=4):
    import collections
    def intp(obj,ind=0,doIdn = 1):
        rst = ""
        if isinstance(obj,str):
            return rst + "_" * (indent * ind * doIdn) + str(obj)
        if type(obj) == list:
            rst="\n"
            doIdn=1
            for i in len(obj):
                rst +="_"*(indent*ind*doIdn)+str(i)+": "+intp(obj[i],ind+1,0)+"\n"
            return rst

        if hasattr(obj,"__getitem__"):
            rst = "\n"
            doIdn = 1
            for i in obj:
                rst += "_" * (indent * ind * doIdn) + str(i) + ": " + intp(obj[i], ind + 1, 0) + "\n"
            return rst

        return rst + "_" * (indent * ind * doIdn) + str(obj)

    print(intp(adict))


if __name__=="__main__":
    showmessage(MD5("nonohome"))


