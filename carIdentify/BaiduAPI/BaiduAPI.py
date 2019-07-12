#沈楷
import urllib.request, urllib
import requests
import json
import base64

# client_id 为官网获取的AK， client_secret 为官网获取的SK


def getToken():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=vSVRSXAqwdKkionHoLv43GNM&client_secret=psR4GC5DhLjB7rHbroNYZGkuy3YRDBXd'
    res = requests.get(host).json()
    return res["access_token"]

def identify(access_Token,image_file):
    # encoding:utf-8
    '''
    车型识别
    '''

    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/car"

    # 二进制方式打开图片文件
    f = open(image_file, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img, "top_num": 5}
    params = urllib.parse.urlencode(params).encode(encoding='UTF8')
    access_token = access_Token
    request_url = request_url + "?access_token=" + access_token
    request = urllib.request.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')  # string类型

    return content

#车辆分析—车辆属性识别
def featureIdentify(access_Token,image_file):
    '''
        车辆属性
    '''
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/vehicle_attr"
    # 二进制方式打开图片文件
    f = open(image_file, 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img}
    params = urllib.parse.urlencode(params).encode(encoding='UTF8')

    access_token = access_Token
    request_url = request_url + "?access_token=" + access_token
    request = urllib.request.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')  # string类型
    data = eval(content)
    num = data["vehicle_num"]
    fea = data["vehicle_info"][0]["attributes"]
    return num,fea

def driver(access_Token,image_file):
    '''
        驾驶员行为
    '''
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/driver_behavior"

    # 二进制方式打开图片文件
    f = open(image_file, 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img}
    params = urllib.parse.urlencode(params).encode(encoding='UTF8')
    access_token = access_Token
    request_url = request_url + "?access_token=" + access_token
    request = urllib.request.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')  # string类型
    data = eval(content)
    person_info = data["person_info"][0]["attributes"]
    phone = person_info["cellphone"]["score"]
    hands_leave = person_info["both_hands_leaving_wheel"]["score"]
    not_face_front = person_info['not_facing_front']['score']
    not_buckle_up = person_info['not_buckling_up']['score']
    smoke = person_info["smoke"]["score"]
    return phone,hands_leave,not_face_front,not_buckle_up,smoke


