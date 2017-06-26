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
    return send_from_directory(app.config['DOWNLOAD_FOLDER'],filename)

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

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_file_url= os.path.join(app.config['UPLOAD_FOLDER'], filename)

            #指定IMAGE要追加的collection_name
            collection_name = config.Image_collection_name_define

            find_similar = WatsonVisualRecognition().findSimilaImage(collection_name=collection_name,
                                                                     image=image_file_url)

            print(json.dumps(find_similar,indent=2))
            get_emp_SN = find_similar['similar_images'][0]['metadata']['emp_SN']

            key_info = {'userSN': get_emp_SN}
            #print('$$$$'+ key_info)

            img =find_object_info(key_info)
            print (img)

            down_filename=os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
            with open(down_filename,'wb') as downimage:
                downimage.write(img["user_IMG"])
            file_url = url_for('uploaded_file', filename=filename)
            response_html = 'findSimilar.html'
            response_title = 'findSimilar'
            return render_template(response_html,
                                   title =response_title,
                                   emp_name=response_emp_name,
                                   emp_SN = get_emp_SN,
                                   file_url = file_url )

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

            response_emp_name = session['login_name']
            response_html = 'VRimageManage.html'
            response_title = 'VisualRecognitionimageManage'
            return render_template(response_html,
                                   title=response_title,
                                   emp_name=response_emp_name)

@app.route('/documentConvertion')
def documentConvertion():
    response_emp_name = session['login_name']
    response_html = 'fileconvert.html'
    response_title = 'DocumentConvertion'
    return render_template(response_html,
                           title = response_title,
                           emp_name=response_emp_name)

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

@app.route('/datacollecte')
def datacollecte():
    empform = collectForm()
    response_emp_name = session['login_name']
    response_html = 'datacollecte.html'
    response_title = 'DataCollecte'
    return render_template(response_html,
                           title = response_title,
                           emp_name=response_emp_name,
                           empform= empform)

@app.route('/doDatacollecte',methods=['GET','POST'])
def doDatacollection():
    empform = collectForm()
    if request.method == 'POST':
        #if empform.validate_on_submit():
        emp_SN=empform.emp_SN.data
        emp_name=empform.emp_name.data
        emp_onboard_date=empform.emp_onboard_date.data

        emp_Skill=empform.emp_Skill.data
        emp_photo_title=empform.emp_photo_title.data
        emp_photo_image=empform.emp_photo_image.data
        emp_photo_creatdate=empform.emp_photo_creatdate.data
        emp_photo_flag=empform.emp_photo_flag.data



        if emp_SN == '':
            return
        else:
            key_info = {'emp_SN':emp_SN}
            find_result = find_object_info(key_info)
            if emp_photo_image == None:
                if find_result != None:
                    return
                else:
                    return

            return








        print(emp_SN,emp_name,emp_onboard_date,emp_Skill,emp_photo_flag)

        response_emp_name = session['login_name']
        response_html = 'datacollecte.html'
        response_title = 'DataCollecte'
        return render_template(response_html,
                           title = response_title,
                           emp_name=response_emp_name,
                           empform= empform)

@app.route('/uploadfile',methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':

        file = request.files['file']

        userSN= request.form['usersn']

        if file and allowed_file(file.filename):
            filename =secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            with open(img_filename, 'rb') as myimage:
                content = myimage.read()

            insert_object_info = {"userSN":userSN,"user_IMG":content}

            add_object_info(insert_object_info)

            key_info = {"userSN":userSN}

            #save_file(userSN,img_filename)

            img=find_object_info(key_info)

            down_filename=os.path.join(app.config['DOWNLOAD_FOLDER'], filename)

            with open(down_filename,'wb') as downimage:
                downimage.write(img["user_IMG"])

            file_url = url_for('uploaded_file', filename=filename)

            return render_template('VisualRecognition.html') + img["userSN"] +'<br><img src=' + file_url + ' width = "300" height= "400">'
    return render_template('VisualRecognition.html')