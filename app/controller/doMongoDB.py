
from app.model.mongoDBoperate import Emp_info
#from app.controller.WatsonDevCloud import WatsonVisualRecognition

'''
def add_object_info(key_info,img_filename):
    with open(img_filename,'rb') as myimage:
        content = myimage.read()
        new_object = {"userSN":key_info,"user_IMG":content}
        #new_object = key_info
        Emp_info().add_info(new_object)'''
def add_object_info(key_info):
        new_object = key_info
        Emp_info().add_info(new_object)

def find_object_info(key_info):
    #query_object = {"userSN":key_info}
    query_object = key_info
    find_yes = Emp_info().find_info(query_object)
    print ("~~~~~~~~~~~~~")
    print(find_yes)
    print("~~~~~~~~~~~~~")
    if find_yes is None:
        find_result= key_info
    else:
        find_result = find_yes

    return find_result

def update_object_info(key_info,object_key,new_object_value):
    query_object_info =key_info
    set_object_info = {object_key:new_object_value}
    Emp_info().update_info(query_object_info,set_object_info)

def update_object_info_push(key_info,object_key,new_object_value):
    query_object_info = key_info
    set_object_info = {object_key:new_object_value}
    Emp_info().update_info_push(query_object_info,set_object_info)



