from PIL import Image
import requests
import os, errno
import tempfile
# from .configs import *
from dotenv import load_dotenv

'''
获取https://www.hackthis.co.uk/levels/captcha/1中的验证码
使用tesseract循环200次都没有通过验证码识别；改用keras
运行程序前先设置登录用户名、密码
export username=''
export password=''

'''

def createdir(path, access_rights = 0o755):
    try:
        os.mkdir(path, access_rights)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

def postSolution(captchaCounts=100):
    url = "https://www.hackthis.co.uk/levels/captcha/1"

    # tf =tempfile.NamedTemporaryFile(delete=False)
    # tf.close()
    # captchaFileName = tf.name
    url_login = "https://www.hackthis.co.uk/?login"
    password, username = getLoginEnv()
    try:
        status = False
        while not status:
            # 直到登录成功
            r_login, s, status = login(url_login, username, password)

        url_captcha = "https://www.hackthis.co.uk/levels/extras/captcha1.php"

        i = 0
        mypath= '/tmp/captcha'
        createdir(mypath)
        while i < captchaCounts:
            # 循环保存验证码
            r_captcha = requests.get(url_captcha, cookies=r_login.history[0].cookies)
            print(r_captcha.status_code)
            captchaFileName = getRandomCaptchaFilename(mypath)
            # 保存验证码
            f = open(captchaFileName, 'wb')
            f.write(r_captcha.content)
            f.close()

            # silentremove(captchaFileName)
            print('filename:{}'.format(captchaFileName))
            i += 1

    except Exception as e:
        return ":("


def getRandomCaptchaFilename(path='/tmp'):
    captchaFileName = '{}.{}'.format(tempfile.NamedTemporaryFile().name, 'png')
    captchaFileName = os.path.join(path, os.path.basename(captchaFileName))
    # captchaFileName = '/tmp/captcha.png'
    return captchaFileName


def login(url_login, username, password):
    s = requests.Session()  # Start a session
    print('Logining...')
    r_login = s.post(url_login, {'username': username, 'password': password})
    if "Invalid login details" in r_login.text:
        print("Failed to login")
        status = False
    else:
        print("Login success")
        status = True
    return r_login, s, status


def getLoginEnv():
    '''
    从环境变量获取用户名、密码
    :return:
    '''

    def loadEnv(envFileName="../config.env"):
        load_dotenv(envFileName)

    username = 1
    if "username" in os.environ:
        username = os.getenv('username', 'username not set')
    else:
        print('请先 export username， password')
    if "password" in os.environ:
        password = os.getenv('password', 'password not set')

    if not isinstance(username, str):
        loadEnv()
        return getLoginEnv()
    return password, username


if __name__ == '__main__':
    i = 0
    while postSolution() == ":(":
        postSolution()
        i += 1
        print('：（ 失败，第 {} 次'.format(i))
    print("Solved!")
