from PIL import Image
import pytesseract  # pip install pytesseract && sudo  dnf install tesseract
import requests
import os, errno
import tempfile
# from multiprocessing import Pool

'''
运行程序前先设置登录用户名、密码
export username=''
export password=''

'''

def silentremove(filename):
    '''
    删除文件
    :param filename:
    :return:
    '''
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred

def solve(captcha):
    '''
    识别验证码
    :param captcha: 图形路径
    :return: 识别的数字
    '''
    def grayImage(captcha):
        image = Image.open(captcha)
        # 转成灰度图
        imgry = image.convert('L')
        # imgry.show()
        # 二值化，阈值可以根据情况修改
        threshold = 65
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        out = imgry.point(table, '1')
        out.show()
        return out

    config = '-psm 7'
    # config = '-psm 6 tessedit_char_whitelist abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$*+-? '
    return pytesseract.image_to_string(grayImage(captcha), config=config)[::-1]

def postSolution():
    url = "https://www.hackthis.co.uk/levels/captcha/1"
    captchaFileName = '/tmp/captcha.png'
    # tf =tempfile.NamedTemporaryFile(delete=False)
    # tf.close()
    # captchaFileName = tf.name
    url_login = "https://www.hackthis.co.uk/?login"
    password, username = getLoginEnv()
    try:

        s = requests.Session()  # Start a session
        r_login = s.post(url_login, {'username': username, 'password': password})

        if "Invalid login details" in r_login.text:
            print("Failed to login")
        else:
            print("Login success")

        url_captcha = "https://www.hackthis.co.uk/levels/extras/captcha1.php"
        r_captcha = requests.get(url_captcha, cookies=r_login.history[0].cookies)

        print(r_captcha.status_code)

        # 保存验证码
        f = open(captchaFileName, 'wb')
        f.write(r_captcha.content)
        f.close()

        #
        solution = solve(captchaFileName)
        # silentremove(captchaFileName)
        print('captcha: {} , 识别长度：{}'.format(solution, len(solution)))
        payload = {"answer": solution}
        s.post(url, data=payload) # Post data
        response = s.get(url).text
        if ("Incomplete" in response):
            return ":("
        else:
            return "Sucessfully solved problem"
    except Exception as e:
        return ":("


def getLoginEnv():
    '''
    从环境变量获取用户名、密码
    :return:
    '''
    if "username" in os.environ:
        username = os.getenv('username', 'username not set')
    else:
        print('请先 export username， password')
    if "password" in os.environ:
        password = os.getenv('password', 'password not set')
    return password, username


if __name__ == '__main__':
    i=0
    while postSolution() == ":(":
        postSolution()
        i+=1
        print('：（ 失败，第 {} 次'.format(i))
    print("Solved!")