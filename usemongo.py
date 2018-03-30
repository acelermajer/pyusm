import pymongo ,pymongo.database , usefull, json , bson, time


mainDatabase ={}


class NoConnection(Exception):
    def __str__(self):
        return """Set a mongoClient database by parametter or global like this usemongo.mainDatabase=pymongo.MongoClient().get_database("myDB")"""

class MGObject():
    def __init__(self,Collection=None,mongoDatabase={},data={}):
        global mainDatabase
        if mongoDatabase=={}:
            mongoDatabase=mainDatabase
        if mongoDatabase == {}:
            raise NoConnection()

        self.__dict__["_MGOinternalDatas"]=data
        if Collection == None:
            if self.__class__.__name__[:2]=="MG":
                Collection = self.__class__.__name__[2:]
            else:
                Collection = self.__class__.__name__

        self.__dict__["_MGODatabase"] = mongoDatabase
        """:type mongoDatabase:pymongo.database"""
        if type(Collection)==str:
            self.__dict__["_MGOCollection"] = mongoDatabase.get_collection(Collection)
        else:
            self.__dict__["_MGOCollection"] = Collection


    def __getattr__(self, item):
        return self._MGOinternalDatas.get(item,None)

    def __setattr__(self, key, value):
        self._MGOinternalDatas[key]=value
        self.update({key:value})
        return value

    def getData(self):
        return self._MGOinternalDatas

    def getCnx(self):
        """
        :rtype: pymongo.database.Database
        """
        return self._MGODatabase

    def getCollection(self):
        """
        :rtype: pymongo.collection.Collection
        """
        return self._MGOCollection

    def setCollection(self,Collection):
        self._MGOCollection = self.getCnx().get_collection(Collection)

    def update(self, data={}):
        if data == {}:
            data = self.getData()
        _id = data.get("_id", None)
        if _id == None:
            if self._id == None:
                return
            _id=self._id
        else:
            del (data["_id"])
        self.getCollection().update_one({"_id": _id}, {"$set": data})

    def insert(self, data={}):
        if data == {}:
            data = self.getData()
        else:
            self.__dict__["_MGOinternalDatas"]=data
        try:
            rst = self.getCollection().insert_one(data)
            self.__dict__["_MGOinternalDatas"]["_id"]=rst["insertedId"]
        except:
            pass

    def delete(self):
        _id = self._id
        if _id == None:
            self.getCollection().delete_one(self.getData())
            return
        self.getCollection().delete_one({"_id":_id})
    def find(self,*args,**kwargs):
        fs=self.getCollection().find(*args,**kwargs)
        rst=[]
        # def __init__(self,Collection=None,mongoDatabase={},data={}):
        for f in fs:
            rst+=[eval(self.__class__.__name__)(Collection=self.getCollection(),mongoDatabase=self.getCnx(),data=f)]
        return rst



