import requests
import base64
import json
import os
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
        self.con_status = False
        self.login_status=False
    def con(self):
        try:
            r=self.session.get(url='http://202.203.16.42')
            if r.status_code==200:
                self.cookies=requests.utils.dict_from_cookiejar(r.cookies)
                #检测是否需要验证码
                self.valid_code_status=self.session.post(url='http://202.203.16.42/nonlogin/login/captcha/isvalid.htm').content.decode('utf-8')
                self.valid_code_status=bool(self.valid_code_status)
                self.con_status = True
        except:
            return('连接服务器失败')
    def base64_api(self,uname, pwd,  img):
        try:
            with open(img, 'rb') as f:
                base64_data = base64.b64encode(f.read())
                b64 = base64_data.decode()
            data = {"username": uname, "password": pwd, "image": b64}
            result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
            if result['success']:
                return result["data"]["result"]
        except:
            return ''
    def get_valid_code(self):
        if self.valid_code_status:
            r=self.session.get(url='http://202.203.16.42:80/nonlogin/login/captcha.htm')
            with open(self.valid_code_path,'ab') as f:
                f.write(r.content)
                f.close()
            self.valid_code = self.base64_api(uname='用户名', pwd='密码', img=self.valid_code_path) #填入你注册的账号密码
            os.remove(self.valid_code_path)
        else:
            pass
    def login(self):
        if self.con_status:
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
                self.login_status = True
        else:
            return('连接失败')
    def clock(self):
        if self.login_status:
            url = "http://202.203.16.42:80/syt/zzapply/operation.htm"
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': '202.203.16.42',
                'Content-Length':'326',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57',
            }
            time=requests.get('http://quan.suning.com/getSysTime.do').content.decode('utf-8')
            time= json.loads(time)['sysTime1'][8:12]
            time=int(time)
            if time>600 and time<1400:
                payload='data=%7B%22xmqkb%22%3A%7B%22id%22%3A%224a4b90aa73fad84c017411601830099d%22%7D%2C%22pdnf%22%3A%222020%22%2C%22type%22%3A%22xsfxtwjc%22%2C%22c1%22%3A%22%E5%B0%8F%E4%BA%8E37.3%C2%B0C%22%2C%22c2%22%3A%22%E5%90%A6%22%7D&msgUrl=syt%2Fzzglappro%2Findex.htm%3Ftype%3Dxsfxtwjc%26xmid%3D4a4b90aa73fad84c017411601830099d&multiSelectData='
            elif time>1700 and time<2200:
                payload='data=%7B%22xmqkb%22%3A%7B%22id%22%3A%224a4b90aa73faf66a0174116ae01b0a14%22%7D%2C%22pdnf%22%3A%222020%22%2C%22type%22%3A%22xsfxtwjc%22%2C%22c1%22%3A%22%E5%B0%8F%E4%BA%8E37.3%C2%B0C%22%2C%22c2%22%3A%22%E5%90%A6%22%7D&msgUrl=syt%2Fzzglappro%2Findex.htm%3Ftype%3Dxsfxtwjc%26xmid%3D4a4b90aa73faf66a0174116ae01b0a14&multiSelectData='
            else:
                return ('不在时间范围')
            try:
                response = self.session.post(url, headers=headers, data=payload)
                return(response.text)           
            except:
                return('打卡失败')
        else:
            return('登录失败')