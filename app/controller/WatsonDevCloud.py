from watson_developer_cloud import VisualRecognitionV3,DocumentConversionV1
import json
#Watson Api's info:
#url": "https://gateway-a.watsonplatform.net/visual-recognition/api",
#note": "It may take up to 5 minutes for this key to become active",
#api_key": "c392d4ae18fbea3b94ffc0dc06e9247c5186cdb2"
#06/11/2017

#创建VisualRecognition类

class WatsonVisualRecognition:
    api_key='c392d4ae18fbea3b94ffc0dc06e9247c5186cdb2'    #替换
    version='2017-06-11'
    visual_Recognition = None

    def __init__(self):
        #初期设定api key, version
        self.visual_Recognition=VisualRecognitionV3(api_key=self.api_key,version=self.version)

    # 新创建classifier   用于让Watson 学习，可以不新创建，暂不使用，保留       只创建collection，用于find similar
    def creatClassifiar(self,positive_example_file,negative_example_file = None):
        classifiar_name = '!@#$%~^&**()'

        #Learning:classifiar 里读入正反向数据文件
        if negative_example_file == None:
            with open(positive_example_file,'rb') as positive_examples:
                response = self.visual_Recognition.create_classifier(name=classifiar_name,
                                                                     emp_positive_example=positive_examples)
        else:
            with open(positive_example_file,'rb') as positive_examples,\
                open(negative_example_file,'rb') as negative_examples:
                response = self.visual_Recognition.create_classifier(name=classifiar_name,
                                                                     emp_positive_example=positive_examples,
                                                                     emp_negative_example=negative_examples)
        return response

    #创建collection
    def createCollection(self,collection_name):
        response = self.visual_Recognition.create_collection(name=collection_name)
        return response

    #根据collection name 取得被创建的 collection_id
    def getCollectionID(self,collection_name):
        #获取所有已创建的collection
        collections = self.visual_Recognition.list_collections()['collections']
        collectionID = ""
        for collection in collections:
            if collection_name == collection['name']:
                collectionID = collection['collection_id']
        return collectionID

    #向collection 里件iamge及信息
    #def addImagetoCollection(self,collection_name,image,metadata=None):
    def addImagetoCollection(self,collection_name,image,metadata):
        collection_id = self.getCollectionID(collection_name=collection_name)
        with open(image,'rb') as image_file:
            response = self.visual_Recognition.add_image(collection_id=collection_id,
                                                         image_file=image_file,
                                                         metadata=metadata)
            return response

    #查找相似image
    def findSimilaImage(self,collection_name,image):
        collection_id = self.getCollectionID(collection_name=collection_name)
        with open(image,'rb') as image_file:
            response=self.visual_Recognition.find_similar(collection_id=collection_id,image_file=image_file,limit=1)

        return response

    #识别图片分类  暂不使用此方法（保留）
    def classifyImage(self,image):
        with open(image,'rb') as image_file:
            response = self.visual_Recognition.classify(images_file=image_file,
                                                    images_url=None,
                                                    classifier_ids=None,
                                                    owners=None,
                                                    threshold=0.1)
        return response

    #面部识别
    def detectFace(self,image):
        with open(image,'rb') as image_file:
            response = self.visual_Recognition.detect_faces(images_file=image_file,
                                                            images_url=None)
        return response

class WatsonDocumentConversion:
    username = '83079411-9348-4920-9b27-10cb54f72dc7'
    password = 'RKFy45gV1E4m'
    version = '2015-12-15'
    document_conversion = DocumentConversionV1(username=username,
                                               password=password,
                                               version=version)

    def document_convert(self,document_url):
        with open(document_url,encoding='utf8') as document:
            #config = {'conversion_target': DocumentConversionV1().NORMALIZED_TEXT}
            #response = DocumentConversionV1().convert_document(document=document,
            #                                                 config=config,
            #                                                 media_type='text/html')
            config = {'conversion_target': self.document_conversion.NORMALIZED_TEXT}
            response = self.document_conversion.convert_document(document=document,
                                                                 config=config,
                                                                 media_type='text/html').content
            print("##################")
            print(response)

        return response

#print (json.dumps(WatsonVisualRecognition().classifyImage("/Users/xiaolli/WorkSpace/WPC_Demo/tmp/uploadfiles/WechatIMG24.jpeg"),indent=2))
#print (json.dumps(WatsonVisualRecognition().detectFace("/Users/xiaolli/WorkSpace/WPC_Demo/tmp/uploadfiles/WechatIMG24.jpeg"),indent=2))