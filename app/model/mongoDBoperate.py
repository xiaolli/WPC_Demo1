from app.model import db
import config

class Emp_info(object):
    coll = db['testupload']
    def add_info(self,object_info):
        #object_info=object_info
        self.coll.insert(object_info)
        print("save_info() is ok")

    def find_info(self,object_info):
        #object_info=object_info
        info= self.coll.find_one(object_info)
        print("query_info() is ok")
        return info

    def delete_info(self,object_info):
        #object_info=object_info
        self.coll.remove(object_info)
        print("remove_info() is ok")
