import tkinter , usefull

class TKForm():
    def __init__(self,title=""):
        frm,cnv = usefull.CreateFrmCanvas([127,127,127])
        self.frm=frm
        self.cnv=cnv

    def setTitle(self,title=""):
        self.frm.wm_title(title)

    def getTitle(self):
        return  self.frm.title

    def setVisible(self,visibility=True):
        pass

    def setFormScreenCenter(self, _size=None):
        if _size == None:
            _size = str(self.frm.winfo_width()) + "x" + str(self.frm.winfo_height())
        else:
            self.frm.geometry(_size)
        self.frm.update()
        self.frm.geometry("+%s+%s" % (int(self.frm.winfo_screenwidth() // 2 - self.frm.winfo_width() // 2),
                                 int(self.frm.winfo_screenheight() // 2 - self.frm.winfo_height() // 2)))









