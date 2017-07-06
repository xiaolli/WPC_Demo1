from app import app
import config
from werkzeug.utils import secure_filename
from flask import request,send_from_directory,url_for,render_template,session,escape
import os,json
from  app.controller.forms import loginForm,collectForm
from app.controller.WatsonDevCloud import WatsonVisualRecognition,WatsonDocumentConversion
from app.controller.doMongoDB import add_object_info,find_object_info,update_object_info,update_object_info_push


#设定配置
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = config.DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

#初始Url定向时，调用FlaskForm模版渲染
@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    #禁用CSRF
    form = loginForm(csrf_enabled=False)
    login_username = form.login_name.data
    if login_username in session:
        response_word = 'Logged in as %s' %escape(session['login_name'])
        response_html = 'main.html'
        response_title = 'index'
        return render_template(response_html,
                               title=response_title,
                               word=response_word)
    else:
        response_word = 'Hello Guest!  Please login first!'
        response_html = 'index.html'
        response_title = 'index'
        return render_template(response_html,
                               title=response_title,
                               form = form,
                               word=response_word)

@app.route('/main',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        form = loginForm(csrf_enabled=False)
        login_username = form.login_name.data
        login_password = form.login_password.data
        login_object = {'login_name':login_username,'login_password':login_password}

        session['login_name'] = form.login_name.data

        print("session:"+session['login_name'])

        for num in range(0,len(config.app_login_cer)):
            if login_object == config.app_login_cer[num]:
                print(login_username + "is OK")
                response_logon = 'OK'
                break
        else:
            response_logon = 'NG'

        if response_logon == 'OK':
            response_title = 'main'
            response_html = 'main.html'
            response_emp_name = session['login_name']
            return render_template(response_html,
                                   title=response_title,
                                   emp_name=response_emp_name)
        else:
            response_html = 'index.html'
            response_title = 'index'
            response_form = form
            response_word_end = 'Confirm your input login_name or login_password!!'
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
    #return send_from_directory(app.config['DOWNLOAD_FOLDER'],filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/findsimilar')
def similar_index():

    response_emp_name = session['login_name']

    response_html = 'findsimilar.html'
    response_title = 'findsimilar'
    return render_template(response_html,
                           title=response_title,
                           emp_name=response_emp_name)

@app.route('/findsimilarlist',methods=['GET','POST'])
def findSimilar_list():
    if request.method == 'POST':
        response_emp_name = session['login_name']
        print(response_emp_name)
        file = request.files['imagefile']

        if file and allowed_file(file.filename):
            filename =secure_filename(file.filename)

            #上传并取得文件的URL用于Findsimilar传参
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_file_url= os.path.join(app.config['UPLOAD_FOLDER'], filename)

            #指定IMAGE find的collection_name
            collection_name = config.Image_collection_name_define

            #执行 watson 的Findsimilar
            find_similar = WatsonVisualRecognition().findSimilaImage(collection_name=collection_name,
                                                                     image=image_file_url)

            print(json.dumps(find_similar,indent=2))

            #取得Similar照片上的KeyInfo：emp_SN
            get_emp_SN = find_similar['similar_images'][0]['metadata']['emp_SN']

            #作为Key到DB去检索
            key_info = {'userSN': get_emp_SN}
            #print('$$$$'+ key_info)
            find_result =find_object_info(key_info)
            print (find_result)

            find_SN = find_result['userSN']
            find_Name=find_result['userNAME']

            #down_filename=os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
            #with open(down_filename,'wb') as downimage:
            #    downimage.write(img["user_IMG"])
            #file_url = url_for('uploaded_file', filename=filename)
            response_html = 'findSimilar.html'
            response_title = 'findSimilar'
            return render_template(response_html,
                                   title =response_title,
                                   emp_name=response_emp_name,
                                   find_SN = find_SN,
                                   find_Name=find_Name)
                                   #file_url = file_url )

@app.route('/imageManage',methods=['GET','POST'])
def VRmanage():
    response_emp_name = session['login_name']
    response_html = 'VRimageManage.html'
    response_title = 'VisualRecognitionimageManage'
    return render_template(response_html,
                           title=response_title,
                           emp_name = response_emp_name)

@app.route('/addImage',methods=['GET','POST'])
def image_manage():

    if request.method=='POST':
        image_file = request.files['imagefile']

        #collection_name= config.Image_collection_name_define
        #用于watson 图片识别的creat collection
        collection_name='emp_collection'

        #从html 上取得 name，SN，及 照片，add到collection
        emp_name = request.form['emp_name']
        emp_SN = request.form['emp_SN']

        #用于addimage的metaData
        metadata_object = {'emp_SN':emp_SN,'emp_name':emp_name}

        #if image_file and allowed_file(image_file.filename):
        #   image_filename =secure_filename(image_file.filename)

        image_filename = image_file.filename

        #保存图片到Server 上
        upload_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'tmp/uploadfiles')
        image_file.save(os.path.join(upload_path, image_filename))

        #图片在Server上的URL
        image_file_save_url= os.path.join(upload_path, image_filename)

        #Watson的图片识别API：取得到collection的ID用于向collection add 照片
        get_collection_id=WatsonVisualRecognition().getCollectionID(collection_name=collection_name)
        print('@@@@@'+get_collection_id)

        #向collection add 照片
        get_image_info=WatsonVisualRecognition().addImagetoCollection(collection_name=collection_name,
                                                                      image=image_file_save_url,
                                                                      metadata=metadata_object)
        print(json.dumps(get_image_info,indent=2))

        response_emp_name = session['login_name']
        response_html = 'VRimageManage.html'
        response_title = 'VisualRecognitionimageManage'
        return render_template(response_html,
                               title=response_title,
                               emp_name=response_emp_name)


####插入数据到MongoDB
@app.route('/doDatacollecte',methods=['GET','POST'])
def doDatacollecte():
    response_emp_name = session['login_name']
    #FLASK-WTF的表单应用
    empform = collectForm()
    print(empform.validate_on_submit())
    #if request.method == 'POST':
    if empform.validate_on_submit():

        #从HTML上取得SN和file的信息，准备插入到DB
        emp_SN=empform.emp_SN.data
        emp_name=empform.emp_name.data

        img_filename =None


        if emp_SN.replace(' ','') == '' or emp_name.replace(' ','') == '':
            response_word = 'Input data is incorrect,try again!!!'
        else:
            #作为插入DB的对内容
            insert_object_info = {"userSN":emp_SN,"userNAME":emp_name}

            #DB插入
            add_object_info(insert_object_info)

            #response_emp_name = session['login_name']
            response_word = 'Add data is successful!!!'
        response_html = 'datacollecte.html'
        response_title = 'Data Collection'
        return render_template(response_html,
                               title=response_title,
                               emp_name=response_emp_name,
                               empform=empform,
                               response_word=response_word)

    return render_template('datacollecte.html',
                           empform=empform,
                           emp_name=response_emp_name)