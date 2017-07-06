'''
from pymongo import MongoClient,DESCENDING,ASCENDING
import ssl,config


db_url = '####################¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥'          ##替换
client = MongoClient(db_url,ssl_cert_reqs = ssl.CERT_NONE)
db = client['testDB1']

coll = db['emp_info_collection']
coll.remove({'emp_SN':'000000'})
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

coll_id=coll.insert(emp_collection_def)
if coll_id:
    print ('OK')
else:
    print ('NG')

#设定索引，升序，定义主键为emp_SN

coll_uni =coll.ensure_index('emp_SN',unique=True)
if coll_uni:
    print('uni is ok')
else:
    print('uni is ng')

for monster in coll.find():
    print (monster)

print (coll.index_information())'''