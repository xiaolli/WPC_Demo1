from app import app
import config
from werkzeug.utils import secure_filename
from flask import request,send_from_directory,url_for,render_template
import os,json
from  app.controller.forms import loginForm
from app.controller.WatsonDevCloud import WatsonVisualRecognition,WatsonDocumentConversion
from app.controller.doMongoDB import add_file,find_file

#设定配置
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = config.DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

#初始Url定向时，调用FlaskForm模版渲染
@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    #禁用CSRF
    form = loginForm(csrf_enabled=False)
    response_word =  'Hello Guest!  Please login first!'
    response_html = 'index.html'
    response_title = 'index'
    return render_template(response_html,
                           title=response_title,
                           form = form,
                           word=response_word)


@app.route('/main',methods=['GET','POST'])
def login():
    form = loginForm(csrf_enabled=False)
    login_username = form.login_name.data
    login_password = form.login_password.data
    login_object = {'login_name':login_username,'login_password':login_password}

    for num in range(0,len(config.app_login_cer)):
        if login_object == config.app_login_cer[num]:
            print(login_username + "is OK")
            response_logon = 'OK'
            break
    else:
        #print(login_username + "is NG")
        response_logon = 'NG'

    if response_logon == 'OK':
        response_title = 'main'
        response_html = 'main.html'
        response_emp_name = login_username
        return render_template(response_html,
                               title=response_title,
                               emp_name=response_emp_name)
    else:
        response_html = 'index.html'
        response_title = 'index'
        response_form = form
        response_word_end = 'Confirm your input login_name or login_passwrod!!'
        return render_template(response_html,
                               title=response_title,
                               form=response_form,
                               word_end=response_word_end)

#检查上传文件合法性
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1] in config.ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    #return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
    return send_from_directory(app.config['DOWNLOAD_FOLDER'],filename)

#@app.route('/main/find',methods=['GET','POST'])
@app.route('/main/find',methods=['GET'])
def similar_index():
    if request.method == 'GET':
        response_emp_name=request.args.get('emp_name')

        #print(response_emp_name)
        return render_template('findsimilar.html',
                               emp_name=response_emp_name)

@app.route('/findsimilar',methods=['GET','POST'])
def findSimilar_list():
    #response_emp_name = similar_index().response_emp_name
    if request.method == 'POST':
        response_emp_name = request.form['emp_name']
        print(response_emp_name)
        file = request.files['imagefile']

        if file and allowed_file(file.filename):
            filename =secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_file_url= os.path.join(app.config['UPLOAD_FOLDER'], filename)

            #指定IMAGE要追加的collection_name
            collection_name = config.Image_collection_name_define

            find_similar = WatsonVisualRecognition().findSimilaImage(collection_name=collection_name,
                                                                     image=image_file_url)

            print(json.dumps(find_similar,indent=2))
            get_emp_SN = find_similar['similar_images'][0]['metadata']['emp_SN']

            print('$$$$'+ get_emp_SN)

            img =find_file(get_emp_SN)

            down_filename=os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
            with open(down_filename,'wb') as downimage:
                downimage.write(img["user_IMG"])
            file_url = url_for('uploaded_file', filename=filename)

            return render_template('findSimilar.html',
                                   emp_name=response_emp_name) + get_emp_SN +'<br><img src=' + file_url + ' width = "500" height= "500">'


        #return render_template('VisualRecognition.html')


@app.route('/imageManage',methods=['GET','POST'])
def VRmanage():
    return render_template('VRimageManage.html')

@app.route('/addImage',methods=['GET','POST'])
def image_manage():

    if request.method=='POST':
        image_file = request.files['imagefile']

        collection_name= config.Image_collection_name_define

        emp_name = request.form['emp_name']
        emp_SN = request.form['emp_SN']
        metadata_object = {'emp_SN':emp_SN,'emp_name':emp_name}
        if image_file and allowed_file(image_file.filename):
            image_filename =secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            image_file_url= os.path.join(app.config['UPLOAD_FOLDER'], image_filename)


            get_collection_id=WatsonVisualRecognition().getCollectionID(collection_name=collection_name)
            print('@@@@@'+get_collection_id)
            get_image_info=WatsonVisualRecognition().addImagetoCollection(collection_name=collection_name,
                                                                          image=image_file_url,
                                                                          metadata=metadata_object)
            print(json.dumps(get_image_info,indent=2))

            return render_template('VRimageManage.html')

    #render_template('VRimageManage.html')


@app.route('/documentConvertion',methods=['GET'])
def documentConvertion():
    if request.method == 'GET':
        response_emp_name=request.args.get('emp_name')
        return render_template('fileconvert.html')

@app.route('/fileconvert',methods=['GET','POST'])
def doFileConvert():
    if request.method == 'POST':
        response_emp_name = request.form['emp_name']
        file = request.files['docfile']
        filename=secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        document_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        response = WatsonDocumentConversion().document_convert(document_url=document_url)
        print(response)
    return response