import requests
import base64
import json
import os
import datetime
from urllib.parse import urlencode
class YiBan:
    def __init__(self,username:str):
        self.username = base64.b64encode(username.encode('utf-8')).decode('utf-8')
        self.password = base64.b64encode(('@c'+username).encode('utf-8')).decode('utf-8')
        self.session = requests.session()
        self.cookies={}
        self.valid_code=''
        self.valid_code_status=False
        self.valid_code_path=self.username+'.jpeg'
        self.con_status = 'fail'
        self.login_status='fail'
    #建立连接
    def con(self):
        #获取cookie
        try:
            r=self.session.get(url='http://202.203.16.42')
        except:
            return('网络拥堵')
        if r.status_code==200:
            self.cookies=requests.utils.dict_from_cookiejar(r.cookies)
            #检测是否需要验证码
            self.valid_code_status=self.session.post(url='http://202.203.16.42/nonlogin/login/captcha/isvalid.htm').content.decode('utf-8')
            self.valid_code_status=bool(self.valid_code_status)
            self.con_status = 'success'
    #验证码部分
    def base64_api(self,uname, pwd,  img):
        with open(img, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            b64 = base64_data.decode()
        data = {"username": uname, "password": pwd, "image": b64}
        result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
        if result['success']:
            return result["data"]["result"]
        else:
            return ""
    def get_valid_code(self):
        if self.valid_code_status:
            r=self.session.get(url='http://202.203.16.42:80/nonlogin/login/captcha.htm')
            with open(self.valid_code_path,'wb') as f:
                f.write(r.content)
                f.close()
            self.valid_code = self.base64_api(uname='你的用户名', pwd='你的密码', img=self.valid_code_path)
            os.remove(self.valid_code_path)
        else:
            pass
    #登录
    def login(self):
        self.get_valid_code()
        if self.con_status=='success':
            post_data = {
                'username':self.username,
                'password':self.password,
                'verification':self.valid_code,
                'token':self.cookies['token']
            }
            headers = {
                'Content-Type':'application/x-www-form-urlencoded',
                'Content-Length':'112',
                'Host': '202.203.16.42',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57'
            }
            r=self.session.post(url='http://202.203.16.42:80//login/Login.htm',data=urlencode(post_data).encode('utf-8'),headers=headers)
            if r.status_code==200:
                self.login_status = 'success'
    #打卡
    def clock(self):
        if self.login_status == 'success':
            url = "http://202.203.16.42:80/syt/zzapply/operation.htm"
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': '202.203.16.42',
                'Content-Length':'326',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57',
            }
            curr_time = datetime.datetime.now()
            now_date = str(curr_time.hour)+str(curr_time.minute)
            if now_date>'600' and now_date<'1400':
                payload='data=%7B%22xmqkb%22%3A%7B%22id%22%3A%224a4b90aa73fad84c017411601830099d%22%7D%2C%22pdnf%22%3A%222020%22%2C%22type%22%3A%22xsfxtwjc%22%2C%22c1%22%3A%22%E5%B0%8F%E4%BA%8E37.3%C2%B0C%22%2C%22c2%22%3A%22%E5%90%A6%22%7D&msgUrl=syt%2Fzzglappro%2Findex.htm%3Ftype%3Dxsfxtwjc%26xmid%3D4a4b90aa73fad84c017411601830099d&multiSelectData='
                try:
                    response = self.session.post(url, headers=headers, data=payload)
                    return(response.text)           
                except:
                    return('错误')
            elif now_date>'1700' and now_date<'2200':
                payload='data=%7B%22xmqkb%22%3A%7B%22id%22%3A%224a4b90aa73faf66a0174116ae01b0a14%22%7D%2C%22pdnf%22%3A%222020%22%2C%22type%22%3A%22xsfxtwjc%22%2C%22c1%22%3A%22%E5%B0%8F%E4%BA%8E37.3%C2%B0C%22%2C%22c2%22%3A%22%E5%90%A6%22%7D&msgUrl=syt%2Fzzglappro%2Findex.htm%3Ftype%3Dxsfxtwjc%26xmid%3D4a4b90aa73faf66a0174116ae01b0a14&multiSelectData='
                try:
                    response = self.session.post(url, headers=headers, data=payload)
                    return response.text           
                except:
                    return('打卡错误')
            else:
                return('不在时间范围')
        else:
            return('登陆出错')
