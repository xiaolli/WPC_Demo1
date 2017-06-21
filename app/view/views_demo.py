from app import app
import config
from werkzeug.utils import secure_filename
from flask import request,send_from_directory,url_for,render_template
import os,json
from app.controller.upload import save_file,query_file
from app.controller.WatsonDevCloud import WatsonVisualRecognition


app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = config.DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH


#检查上传文件合法性
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1] in config.ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    #return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
    return send_from_directory(app.config['DOWNLOAD_FOLDER'],filename)

@app.route('/')
def index():
    return render_template('VisualRecognition.html')

@app.route('/findSimilar',methods=['GET','POST'])
def similar_index():
    return render_template('findSimilar.html')

@app.route('/find',methods=['GET','POST'])
def findSimilar():
    if request.method == 'POST':

        file = request.files['imagefile']

        if file and allowed_file(file.filename):
            filename =secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_file_url= os.path.join(app.config['UPLOAD_FOLDER'], filename)

            #print(json.dumps(WatsonVisualRecognition().detectFace(image_file_url),indent=2))
            collection_name = 'emp_collection'
            find_similar = WatsonVisualRecognition().findSimilaImage(collection_name=collection_name,
                                                                     image=image_file_url)

            print(json.dumps(find_similar,indent=2))
            get_emp_SN = find_similar['similar_images'][0]['metadata']['emp_SN']

            print('$$$$'+ get_emp_SN)

            img=query_file(get_emp_SN)

            down_filename=os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
            with open(down_filename,'wb') as downimage:
                downimage.write(img["user_IMG"])
            file_url = url_for('uploaded_file', filename=filename)


            #file_url = url_for('uploaded_file',filename=filename)
            return render_template('findSimilar.html') + get_emp_SN +'<br><img src=' + file_url + ' width = "500" height= "500">'


        #return render_template('VisualRecognition.html')

@app.route('/VRmanage',methods=['GET','POST'])
def VRmanage():
    return render_template('VRimageManage.html')

@app.route('/addImage',methods=['GET','POST'])
def image_manage():

    print('aaaa')
    if request.method=='POST':
        image_file = request.files['imagefile']

        collection_name= request.form['collection_name']
        emp_name = request.form['emp_name']
        emp_SN = request.form['emp_SN']
        metadata_object = {'emp_SN':emp_SN,'emp_name':emp_name}
        if image_file and allowed_file(image_file.filename):
            image_filename =secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            image_file_url= os.path.join(app.config['UPLOAD_FOLDER'], image_filename)

            if collection_name == 'emp_collection':
                get_collection_id=WatsonVisualRecognition().getCollectionID(collection_name=collection_name)
                print('@@@@@'+get_collection_id)
                get_image_info=WatsonVisualRecognition().addImagetoCollection(collection_name=collection_name,
                                                               image=image_file_url,
                                                               metadata=metadata_object)
                print(json.dumps(get_image_info,indent=2))

                return render_template('VRimageManage.html')

            else:
                collection_name = 'emp_collection'
                get_collection_name = WatsonVisualRecognition().createCollection(collection_name=collection_name)
                get_collection_id=WatsonVisualRecognition().getCollectionID(collection_name=collection_name)
                print('######'+get_collection_id)
                get_image_info=WatsonVisualRecognition().addImagetoCollection(collection_name=collection_name,
                                                               image=image_file_url,
                                                               metadata=metadata_object)
                print(json.dumps(get_image_info,indent=2))

                return render_template('VRimageManage.html')
    render_template('VRimageManage.html')


@app.route('/uploadfile',methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':

        file = request.files['file']


        #if len(file.read()) <= config.MAX_CONTENT_LENGTH:

        userSN= request.form['usersn']

        if file and allowed_file(file.filename):
            filename =secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            #file_url = url_for('uploaded_file', filename=filename)

            save_file(userSN,img_filename)
            ##save_file(userSN,file)

            img=query_file(userSN)

            down_filename=os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
            with open(down_filename,'wb') as downimage:
                downimage.write(img["user_IMG"])

            file_url = url_for('uploaded_file', filename=filename)

            #file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

            #file_url = url_for('uploaded_file',filename=filename)
            return render_template('VisualRecognition.html') + img["userSN"] +'<br><img src=' + file_url + ' width = "300" height= "400">'
            #return render_template('VisualRecognition.html') + userSN +'<br><img src=' + file_url + '>'
        #else:
            #return render_template('VisualRecognition.html') + 'File Size is over'

    return render_template('VisualRecognition.html')

