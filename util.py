import base64
import datetime
import random
import time
import uuid
import base64

from Cryptodome.Cipher import AES
from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import MD5

def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def get_time_no_second():
    return time.strftime("%Y-%m-%d %H:%M", time.localtime())

def get_7_day_ago():
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=-7)
    n_days = now + delta
    return n_days.strftime('%Y-%m-%d')

def get_days_ago(n):
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=n)
    n_days = now + delta
    return n_days.strftime('%Y-%m-%d')

def get_today():
    return time.strftime("%Y-%m-%d", time.localtime())

def get_yesterfay():
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=-1)
    n_days = now + delta
    return n_days.strftime('%Y-%m-%d')


def desc_sort(array, key="FeedbackTime"):
    for i in range(len(array) - 1):
        for j in range(len(array) - 1 - i):
            if array[j][key] < array[j + 1][key]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array


def encrypt_passwd(message, key):
    cipher = PKCS1_v1_5.new(RSA.importKey(key))
    return str(base64.b64encode(cipher.encrypt(message.encode('utf-8'))), 'utf-8')


def generate_imei():
    r1 = 1000000 + random.randint(1, 9000000)
    r2 = 1000000 + random.randint(1, 9000000)
    instr = str(r1) + str(r2)
    ch = list(instr)
    a = 0
    b = 0
    for i in range(len(ch)):
        tt = int(ch[i])
        if i % 2 == 0:
            a = a + tt
        else:
            temp = tt * 2
            b = b + temp / 10 + temp % 10
    last = int((a + b) % 10)
    if last == 0:
        last = 0
    else:
        last = 10 - last
    return instr + str(last)


def generate_sig():
    return MD5.MD5Hash(str(uuid.uuid1()).encode('utf-8')).hexdigest()[:16]

# AES加密
def aes_encrypt(self,data:str) -> bytes:
    cipher = AES.new(bytes('2knV5VGRTScU7pOq', 'utf-8'), AES.MODE_CBC, bytes('UmNWaNtM0PUdtFCs', 'utf-8'))
    encrypted = base64.b64encode(cipher.encrypt(self.aes_pkcs7padding(bytes(data, 'utf-8'))))
    return base64.b64encode(encrypted)