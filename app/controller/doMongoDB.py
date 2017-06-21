
from app.model.mongoDBoperate import Emp_info
#from app.controller.WatsonDevCloud import WatsonVisualRecognition


def add_file(SN,img_filename):
    with open(img_filename,'rb') as myimage:
        content = myimage.read()

        new_object = {"userSN":SN,"user_IMG":content}
        Emp_info().add_info(new_object)

def find_file(SN):
    query_object = {"userSN":SN}
    SN_OK = Emp_info().find_info(query_object)

    if SN_OK is None:
        print ("There is no userSN:" + SN)

    return SN_OK



