#彭永超 沈楷
import config
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, session
from werkzeug.utils import secure_filename
from datetime import timedelta
import os
import cv2
import time
import numpy as np
from PIL import Image
from carLogo import identify, getToken,featureIdentify, driver
from RecognitionPlate import PlateRecognition
from carRecognition.test import Mytest
app=Flask(__name__)
# 设置静态文件缓存过期时间

app.send_file_max_age_default = timedelta(seconds=1)
app.secret_key='dsfsdf'
app.config.from_object(config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)
class User(db.Model):
    __tablename__ = 'webuser'
    name = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(32), nullable=False)
@app.route('/')
def index():
    return redirect(url_for('login'))
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        name = request.form.get('name')
        password = request.form.get('password')
        user = User.query.filter_by(name=name,password=password).first()
        if user:
            session['user_id'] = user.name
            session.permanent=True
            return redirect(url_for('carRecognition'))
        else:
            return '用户名或密码错误'
@app.route('/regist',methods=['GET','POST'])
def regist():
    if request.method =='GET':
        return render_template('regist.html')
    else:
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(name=name).first()
        if user:
            return '该用户名已被注册，请更换'
        else:
            if password1 != password2:
                return '两个密码不相等，请重新输入'
            else:
                adduser = User(name=name,password=password1)
                db.session.add(adduser)
                db.session.commit()
                return redirect(url_for('login'))
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/carRecognition',methods=['GET','POST'])
def carRecognition():
    if request.method == 'POST':
        f = request.files['file']#上传的文件
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        basepath = os.path.dirname(__file__)  # 当前文件所在的目录
        print(basepath)
        upload_path = os.path.join(basepath, 'static/image', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径 sccure_filename  上传文件的文件名获取
        f.save(upload_path)
        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/image', 'test.jpg'), img)#把图片重新保存为统一的路径
        os.remove(upload_path)#删除指定路径的文件
        img_dir = './static/image/test.jpg'
        image = Image.open(img_dir)
        image = image.resize((28, 28))
        image_arr = np.array(image)
        result = Mytest(image_arr)
        user_input = result
        return render_template('carRecognition_ok.html', userinput=user_input, val1=time.time())
    return render_template('carRecognition.html')

@app.route('/numberRecognition',methods=['GET','POST'])
def numberRecognition():
    if request.method == 'POST':

        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'static/image', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)

        # 使用Opencv转换一下图片格式和名称

        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/image', 'testchepai.jpg'), img)
        os.remove(upload_path)
        img_dir = './static/image/testchepai.jpg'


        a = PlateRecognition()
        result = a.vehicleLicensePlateRecognition(img_dir)
        if result:
            user_input = result["Number"]
            return render_template('numberRecognition_ok.html', userinput=user_input, val1=time.time())
        else:
            return render_template('numberRecognition_ok.html', userinput=False, val1=time.time())
    return render_template('numberRecognition.html')

@app.route('/logoRecognition',methods=['GET','POST'])
def logoRecognition():
    if request.method == 'POST':
        f = request.files['file']#上传的文件
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        basepath = os.path.dirname(__file__)  # 当前文件所在的目录

        upload_path = os.path.join(basepath, 'static/image', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径 sccure_filename  上传文件的文件名获取

        #upload_path = os.path.join(upload_path,'test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径

        f.save(upload_path)

        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/image', 'testlogo.jpg'), img)#把图片重新保存为统一的路径
        os.remove(upload_path)#删除指定路径的文件
        img_dir = './static/image/testlogo.jpg'
        token1 = getToken()
        result = identify(token1, img_dir)
        data = eval(result)
        return render_template('logoRecognition_ok.html',name = data["result"][0]['name'], year = data["result"][0]['year'], color = data['color_result'],val1=time.time())
    return render_template('logoRecognition.html')

@app.route('/feaRecognition', methods=['GET','POST'])
def feaRecognition():
    if request.method == 'POST':
        f = request.files['file']  # 上传的文件
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        basepath = os.path.dirname(__file__)  # 当前文件所在的目录

        upload_path = os.path.join(basepath, 'static/image', secure_filename(
            f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径 sccure_filename  上传文件的文件名获取

        # upload_path = os.path.join(upload_path,'test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径

        f.save(upload_path)

        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/image', 'testfea.jpg'), img)  # 把图片重新保存为统一的路径
        os.remove(upload_path)  # 删除指定路径的文件
        img_dir = './static/image/testfea.jpg'
        token1 = getToken()
        num, fea = featureIdentify(token1, img_dir)
        list1=[]
        list1.append(fea['rearview_item']['score'])
        list1.append(fea['in_car_item']['score'])
        list1.append(fea['skylight']['score'])
        list1.append(fea[ 'copilot']['score'])
        list1.append(fea['window_rain_eyebrow']['score'])
        list1.append(fea['roof_rack']['score'])
        for i in range(6):
            list1[i] = round(list1[i],3)
        return render_template('feaRecognition_ok.html', list1=list1,val1=time.time())

    return render_template('feaRecognition.html')

@app.route('/driverAnalyse',methods=['GET','POST'])
def driverAnalyse():
    if request.method == 'POST':
        f = request.files['file']  # 上传的文件
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        basepath = os.path.dirname(__file__)  # 当前文件所在的目录

        upload_path = os.path.join(basepath, 'static/image', secure_filename(
            f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径 sccure_filename  上传文件的文件名获取

        # upload_path = os.path.join(upload_path,'test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径

        f.save(upload_path)

        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)  # 删除原图片文件
        cv2.imwrite(os.path.join(basepath, 'static/image', 'testdriver.jpg'), img)  # 把图片重新保存为统一的路径
        os.remove(upload_path)  # 删除指定路径的文件
        img_dir = './static/image/testdriver.jpg'
        token1 = getToken()
        phone, hands_leave, not_face_front, not_buckle_up, smoke = driver(token1, img_dir)
        list1 = [phone, hands_leave, not_face_front, not_buckle_up, smoke]
        for i in range(5):
            list1[i]=round(list1[i],3)
        print(list1)



        return render_template('driverAnalyse_ok.html', list1=list1, val1=time.time())
    return render_template('driverAnalyse.html')
@app.context_processor
def my_context_processor():
    user_id=session.get('user_id')
    if user_id:
        user = User.query.filter_by(name=user_id).first()
        if user:
            return {'user': user}
    return {}



if __name__ == '__main__':
    db.create_all()
    app.run()
