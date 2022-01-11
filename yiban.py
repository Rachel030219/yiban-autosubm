from logging import fatal
import re
import requests
import util
import json
import base64
from Cryptodome.Cipher import AES

class YiBan:
    CSRF = "sui-bian-fang-dian-dong-xi"  # 随机值 随便填点东西
    cookies = {"csrf_token": CSRF}  # 固定cookie 无需更改
    HEADERS = {"Origin": "https://app.uyiban.com", "User-Agent": "yiban"}  # 固定头 无需更改

    def __init__(self, account, passwd):
        self.account = account   #账号
        self.passwd = passwd    #密码            
        self.session = requests.Session() 
        self.headers = self.session.headers
        self.headers.update({
            "Authorization": "Bearer",
            "loginToken": '',
            "AppVersion": '5.0.1',
            "User-Agent": 'YiBan/5.0.1 Mozilla/5.0 (Linux; Android 7.1.1; Mi 10 Pro Build/LMY49I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.2743.100 Safari/537.36',
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip",
            "X-Requested-With": "com.yiban.app"
        })
        self.access_token = ''
        self.iapp = ''
        self.nick = ''

    # AES加密
    def aes_encrypt(self,data:str) -> bytes:
        cipher = AES.new(bytes('2knV5VGRTScU7pOq', 'utf-8'), AES.MODE_CBC, bytes('UmNWaNtM0PUdtFCs', 'utf-8'))
        encrypted = base64.b64encode(cipher.encrypt(self.aes_pkcs7padding(bytes(data, 'utf-8'))))
        return base64.b64encode(encrypted)
    
    # AES填充模式
    def aes_pkcs7padding(self,data:bytes) -> bytes:
        bs = AES.block_size
        padding = bs - len(data) % bs
        padding_text = bytes(chr(padding) * padding, 'utf-8')
        return data + padding_text

    def request(self, url, method="get", params=None, cookies=None):
        if method == "get":
            req = self.session.get(url, params=params, timeout=10, headers=self.HEADERS, cookies=cookies)
        else:
            req = self.session.post(url, data=params, timeout=10, headers=self.HEADERS, cookies=cookies)
        try:
            return req.json()
        except:
            return None

    def login(self):
        params = {
            'device': 'Xiaomi:Mi 10 Pro',
            'v': '5.0.1',
            'password': util.encrypt_passwd(self.passwd, b'0\x82\x02"0\r\x06\t*\x86H\x86\xf7\r\x01\x01\x01\x05\x00\x03\x82\x02\x0f\x000\x82\x02\n\x02\x82\x02\x01\x00\xe9\xa4\xc33\xc0a\t/\x0e\xd3\tq\xd8\xac\xc0\x027\xdf{>\x06\xe0\x0f\xd0Jy\xf5d;\xaf-\x16\xca\x04y\xb4\xbdPm\x06\x10\xf4\xdd\x05\'\x9cu\xef\xaa(,8\xec+\xe2\x89\xd4x\xd9cz\x02\x02\\/a\xe5\xecK\x16\'PT\x1e|0\x18\xc8\xb4\xc0<\xd5\x85ed\xa0X\xf7;a\xd6w\x87y\x14\xd6\x94T\xc2\xc7\xe5\x9a\xb2\xf6\xd2\xd0{\x98\xa4_>(\xf9{,\x93\xe3\xb4\x8e\x17\x00\x03\x8b\x06{P\x1as\xf0\t}\x85\x7f\xf2\xe0\xc2\xa9\x19l\xea\xc7\x1eCx\xe3\x88\x8b\x99X\x82_\x13T\rC\x14G\xd6\xcf\x03\xdf\xc8\xe6L\x1f\xc9\x9f\xe63\x99\xbc\xf8\x83\xe1Ivt\x7fk\xb0\xd5b\xe8\xbfS\xf8i\xe2\xa4i\xa2\x82\x7f\x97\x8b\xde~\xff\xda\xf8*\xeeL6\xa9)\x91\x00`Y\xcdn9>\xc8\xce\x12\xfc\xa0\\S\xb2\xda~\xc0\\\xbfg\x1e\x88\x03\x88\xc7[{\x86\x98\xd9T\xfb\xd2\xc9tq\xc78\xba\xf5N\xbdPL\x8as\xa9wj\xc4\xa5}?\xf1\x814u\x15\xf1\xbaJ\xcc\xee/\xab\xeaU\xb2\xd6T\x8al\xff\xb4\xb5\x0cP\x1c\xd6\xbf\n89[{\x94\xf9oX\x98\xd5\x05s\\?\xed\x04\xf8I\x9a\xe7D\x11(\xfb\xe5\xdf\xf4=\xd85\xa3\x82\x15\x95\xe1\xcb\xad\xc8\xa5\x8e\x1eM\x00\x89\x15\x07\x17vt[Mq\x1d\x0bp\xadX\xd7{I_\xe1\x99\xf2XzF\xf7\x18E~\xd7LK:\xfa^\xff\xebBM\xe0\x83\xa4P\xc9?\xa5.\xcc\xb5\xc1\x04\x00\xcb\xda\x85w\x0f\x9e\xa1bS\xa5\xb1\xc8\xc1\xa2CT\x01\x86%Z\x07\xf0\x03\xddM\x8c;\x16[\xd9\xb0j\x99\xbfx\xbb8\x14\xdc\x87\xd0\x97\x0c\x155\x87\xf5\xd9\xe5\xf0\x1e\xcf\tJ\xda\xfc\xb8?![\xfa\x1eAD\xb8"\xfb\x85U\xc61\xbc6\x05\x9b\x82 -\x95\x1bVP\xe9\x00\xfa\xe1\x7f \xe72\xfe\x1c;.\xb1\x00\xdb\x10\x95vf\xda#jT\xc8\x8e\x9cL\x92\xc6\xd1e\x1b\x07\xf8\xfd\xfe4\xd3\x998L\x14v2T\x03\x1f\x02\x03\x01\x00\x01'),
            'token': '',
            'mobile': self.account,
            'ct': '2',
            'identify': util.generate_imei(),
            'sversion': '22',
            'apn': 'wifi',
            'app': '1',
            'authCode': '',
            'sig': util.generate_sig()
        }

        r = self.request(url="https://m.yiban.cn/api/v4/passport/login", method='post',params=params)
        
        if r is not None and str(r["response"]) == "100":
            self.access_token = r["data"]["access_token"]
            self.headers.update({
                    "logintoken": self.access_token,
                    "authorization": f"Bearer {self.access_token}"
            })
            print("logintoken:"+self.access_token)
            print("authorization:"+f"Bearer {self.access_token}")
            return r
        else:
            raise Exception("账号或密码错误")

    def getHome(self):
        params = {
            "access_token": self.access_token,
        }
        r = self.request(url="https://mobile.yiban.cn/api/v4/home", params=params)
        self.name = r["data"]["user"]["userName"]
        for i in r["data"]["hotApps"]: # 动态取得iapp号 20201117更新
            if i["name"] == "校本化":
                self.iapp = re.findall(r"iapp[0-9]*", i["url"])[0]
                print(self.iapp)
        return r

    def auth(self):
        url = f"https://f.yiban.cn/{self.iapp}"
        self.session.request(url=url,method='get',allow_redirects=False)

        params = {
            "act": self.iapp
        }
        print()
        r=self.session.request(url="https://f.yiban.cn/iapp/index", method='get', params=params, allow_redirects=False)
        location = r.headers.get("Location")    

        if not location:
            if 'html' in r.text:
                message = re.findall("(?<=<title>).*(?=</title>)", r.text)[0]
                raise Exception(f'获取iapp入口遇到错误 {message}')
            else:
                # 该用户可能没进行校方认证，无此APP权限
                message = r.text[:101]
                raise Exception(f'获取iapp入口遇到错误 {message}')

        verifyRequest = re.findall(r"verify_request=(.*?)&", location)[0]

        result_auth = self.request(
            "https://api.uyiban.com/base/c/auth/yiban?verifyRequest=%s&CSRF=%s" % (verifyRequest, self.CSRF),
            cookies=self.cookies)
        data_url = result_auth["data"].get("Data")
        if data_url is not None:  # 授权过期
            result_html = self.session.get(url=data_url, headers=self.HEADERS,
                                           cookies={"loginToken": self.access_token}).text
            re_result = re.findall(r'input type="hidden" id="(.*?)" value="(.*?)"', result_html)
            post_data = {"scope": "1,2,3,"}
            for re_i in re_result:
                post_data[re_i[0]] = re_i[1]
            usersure_result = self.session.post(url="https://oauth.yiban.cn/code/usersure",
                                                data=post_data,
                                                headers=self.HEADERS, cookies={"loginToken": self.access_token})
            if usersure_result.json()["code"] == "s200":
                return self.auth()
            else:
                return False
        else:
            return True

    def getUncompletedList(self):
        params = {
            "CSRF": self.CSRF,
            "StartTime": util.get_today(),
            "EndTime": util.get_time()
        }
        return self.request("https://api.uyiban.com/officeTask/client/index/uncompletedList", params=params,
                            cookies=self.cookies)

    def getCompletedList(self):
        params = {
            "CSRF": self.CSRF,
            "StartTime": util.get_days_ago(-5),
            "EndTime": util.get_time()
        }
        return self.request("https://api.uyiban.com/officeTask/client/index/completedList", params=params,
                            cookies=self.cookies)

    def getJsonByInitiateId(self, initiate_id):
        params = {
            "CSRF": self.CSRF
        }
        return self.request("https://api.uyiban.com/workFlow/c/work/show/view/%s" % initiate_id, params=params,
                            cookies=self.cookies)

    def getTaskDetail(self, taskId):
        return self.request(
            "https://api.uyiban.com/officeTask/client/index/detail?TaskId=%s&CSRF=%s" % (taskId, self.CSRF),
            cookies=self.cookies)

    def getShareUrl(self, initiateId):
        return self.request(
            "https://api.uyiban.com/workFlow/c/work/share?InitiateId=%s&CSRF=%s" % (initiateId, self.CSRF),
            cookies=self.cookies)

    # 获取表单信息
    def getform(self,wfid):
        return self.request(
            "https://api.uyiban.com/workFlow/c/my/form/%s?CSRF=%s" % (wfid, self.CSRF),
            cookies=self.cookies)

    def clockIn(self,wfid,formDataJson,extendDataJson):
        url = "https://api.uyiban.com/workFlow/c/my/apply/"
        headers = {
            'origin': 'https://app.uyiban.com',
            'referer': 'https://app.uyiban.com/',
            'Host': 'api.uyiban.com',
            'user-agent': 'yiban'
        }
        params = {
            "CSRF":self.CSRF
        }
        postData= {
            'WFId':wfid,
            'Data':json.dumps(formDataJson,ensure_ascii=False),
            'Extend':json.dumps(extendDataJson,ensure_ascii=False)
        }
        print("提交的data",json.dumps(postData,ensure_ascii=False),"\n")
        data = {
            'Str': self.aes_encrypt(json.dumps(postData, ensure_ascii=False))
        }
        req =  self.session.post(url=url,headers=headers,params=params,data=data,cookies=self.cookies)
        return req.json()