import os

#上传文件要储存的目录
upload_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),'tmp/uploadfiles')
download_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),'tmp/downloadfiles')

UPLOAD_FOLDER = upload_path
DOWNLOAD_FOLDER = download_path

#允许 上传的文件扩展名的集合
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
#ALLOWED_EXTENSIONS = set(['wav', 'flac'])

#限制文件大小
MAX_CONTENT_LENGTH = 2 * 1024 * 1024

#VisualRecognition的collection name
Image_collection_name_define ='emp_collection'

#MongoDB 的colllection
#DBcollection_name_define = set(['testupload'])

#MongoDB 定义 filed_name
def collection_field_define():
    emp_collection_def={'emp_name':'',
                        'emp_SN':'000000',
                        'emp_mail':'',
                        'emp_role':'',
                        'emp_project':'',
                        'emp_team':'',
                        'emp_onboard_date':'',
                        'emp_IBM joinDate':'',
                        'emp_Phone':'',
                        'emp_Skill':[''],
                        'emp_Language':[''],
                        'emp_Band':'',
                        'emp_Photo':[{'photo_title':'',
                                      'photo':'',
                                      'photo_creattime':'',
                                      'group_flag':''}],
                        'emp_video':[{'media_title':'',
                                      'media':'',
                                      'media_creattime':''}],
                        'emp_audio':[{'audio_title':'',
                                      'audio':'',
                                      'audio_creattime':''}]}

    #设定索引，升序，定义主键为emp_SN
    emp_collection_def.ensureIndex({'emp_SN':1},{'unique':True})

app_login_cer=[{'login_name':'lixiaoliang','login_password':''},
               {'login_name':'zhanghan','login_password':'zh'},
               {'login_name': 'huangsha', 'login_password': 'hs'},
               {'login_name': 'lihui', 'login_password': 'lh'},
               {'login_name': 'lihongquan', 'login_password': 'lhq'},
               {'login_name': 'xuxiaochuan', 'login_password': 'xxc'},
               {'login_name': 'xiaojinpeng', 'login_password': 'xjp'},
               {'login_name': 'weizhenyuan', 'login_password': 'wzy'},
               {'login_name': 'test', 'login_password': 'test'}]


