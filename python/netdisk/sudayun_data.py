# Last Modified: 2024-05-02 18:39:19
"""
s = requests.session()
s.get("https://path.dirts.cn/tH0c47D2P", params={"i": "3632", "dir": "/%E6%95%99%E8%82%B2%E4%B8%80%E5%8C%BA/----%E5%85%B6%E4%BB%96%E5%B9%B3%E5%8F%B0%E7%B2%BE%E5%93%81%E8%AF%BE%E7%A8%8B---/04.%E5%B0%8F%E8%8B%97/804-806"}, headers={"dnt": "1"}, cookies={"Hm_lvt_0e42d925d22019079151233bdd075179": "1706080163", "Hm_lpvt_0e42d925d22019079151233bdd075179": "1706713078"})
s.get("https://path.dirts.cn/suda/server/front/business/info", headers={"authorization": "1ee2464b7a750097c77eb427969e4d4c", "dnt": "1"}, cookies={"Hm_lvt_0e42d925d22019079151233bdd075179": "1706080163", "Hm_lpvt_0e42d925d22019079151233bdd075179": "1706713078"})
s.get("https://path.dirts.cn/suda/server/front/business/images", headers={"authorization": "1ee2464b7a750097c77eb427969e4d4c", "dnt": "1"}, cookies={"Hm_lvt_0e42d925d22019079151233bdd075179": "1706080163", "Hm_lpvt_0e42d925d22019079151233bdd075179": "1706713078"})
s.get("https://path.dirts.cn/suda/server/front/business/path", headers={"authorization": "1ee2464b7a750097c77eb427969e4d4c", "dnt": "1"}, cookies={"Hm_lvt_0e42d925d22019079151233bdd075179": "1706080163", "Hm_lpvt_0e42d925d22019079151233bdd075179": "1706713078"})
s.post("https://path.dirts.cn/suda/server/front/business/path/file/list", json={"id":"3632","path":"/VIP会员群/教育一区/----其他平台精品课程---/04.小苗/804-806"}, headers={"authorization": "1ee2464b7a750097c77eb427969e4d4c", "dnt": "1"}, cookies={"Hm_lvt_0e42d925d22019079151233bdd075179": "1706080163", "Hm_lpvt_0e42d925d22019079151233bdd075179": "1706713078"})
s.get("https://path.dirts.cn/manifest.json", headers={"DNT": "1"})

s = requests.session()
s.get("https://path.dirts.cn/tH0c47D2P", params={"i": "3632", "dir": "/%E6%95%99%E8%82%B2%E4%B8%80%E5%8C%BA/----%E5%85%B6%E4%BB%96%E5%B9%B3%E5%8F%B0%E7%B2%BE%E5%93%81%E8%AF%BE%E7%A8%8B---/04.%E5%B0%8F%E8%8B%97/804-806"}, headers={"dnt": "1"}, cookies={"Hm_lvt_0e42d925d22019079151233bdd075179": "1706080163", "Hm_lpvt_0e42d925d22019079151233bdd075179": "1706713078"})
ls=s.post("https://path.dirts.cn/suda/server/front/business/path/file/list", json={"id":"3632","path":"/VIP会员群/教育一区/----其他平台精品课程---/04.小苗/804-806"}, headers={"authorization": "1ee2464b7a750097c77eb427969e4d4c", "dnt": "1"}, cookies={"Hm_lvt_0e42d925d22019079151233bdd075179": "1706080163", "Hm_lpvt_0e42d925d22019079151233bdd075179": "1706713078"})

ls.content
Out[3]: b'{"msg":"ok","errorCode":0,"result":[{"fsId":94993375208494,"path":"/VIP\xe4\xbc\x9a\xe5\x91\x98\xe7\xbe\xa4/\xe6\x95\x99\xe8\x82\xb2\xe4\xb8\x80\xe5\x8c\xba/----\xe5\x85\xb6\xe4\xbb\x96\xe5\xb9\xb3\xe5\x8f\xb0\xe7\xb2\xbe\xe5\x93\x81\xe8\xaf\xbe\xe7\xa8\x8b---/04.\xe5\xb0\x8f\xe8\x8b\x97/804-806/806","category":6,"isDir":1,"size":0,"serverTime":1704904109,"serverFileName":"806"},{"fsId":753780243476880,"path":"/VIP\xe4\xbc\x9a\xe5\x91\x98\xe7\xbe\xa4/\xe6\x95\x99\xe8\x82\xb2\xe4\xb8\x80\xe5\x8c\xba/----\xe5\x85\xb6\xe4\xbb\x96\xe5\xb9\xb3\xe5\x8f\xb0\xe7\xb2\xbe\xe5\x93\x81\xe8\xaf\xbe\xe7\xa8\x8b---/04.\xe5\xb0\x8f\xe8\x8b\x97/804-806/\xe8\xbf\xb7\xe5\xae\xab804","category":6,"isDir":1,"size":0,"serverTime":1704904109,"serverFileName":"\xe8\xbf\xb7\xe5\xae\xab804"},{"fsId":798749328944709,"path":"/VIP\xe4\xbc\x9a\xe5\x91\x98\xe7\xbe\xa4/\xe6\x95\x99\xe8\x82\xb2\xe4\xb8\x80\xe5\x8c\xba/----\xe5\x85\xb6\xe4\xbb\x96\xe5\xb9\xb3\xe5\x8f\xb0\xe7\xb2\xbe\xe5\x93\x81\xe8\xaf\xbe\xe7\xa8\x8b---/04.\xe5\xb0\x8f\xe8\x8b\x97/804-806/.mp3","category":2,"isDir":0,"size":42,"serverTime":1704904109,"serverFileName":".mp3"},{"fsId":923549789260369,"path":"/VIP\xe4\xbc\x9a\xe5\x91\x98\xe7\xbe\xa4/\xe6\x95\x99\xe8\x82\xb2\xe4\xb8\x80\xe5\x8c\xba/----\xe5\x85\xb6\xe4\xbb\x96\xe5\xb9\xb3\xe5\x8f\xb0\xe7\xb2\xbe\xe5\x93\x81\xe8\xaf\xbe\xe7\xa8\x8b---/04.\xe5\xb0\x8f\xe8\x8b\x97/804-806/805\xe6\x8b\xbc\xe9\x9f\xb3\xe4\xba\x92\xe5\x8a\xa8\xe4\xb9\xa62.pdf","category":4,"isDir":0,"size":4045148,"serverTime":1704904109,"serverFileName":"805\xe6\x8b\xbc\xe9\x9f\xb3\xe4\xba\x92\xe5\x8a\xa8\xe4\xb9\xa62.pdf"}]}'

  # {
    "msg": "ok",
    "errorCode": 0,
    "result": [
        {
            "fsId": 94993375208494,
            "path": "/VIP会员群/教育一区/----其他平台精品课程---/04.小苗/804-806/806",
            "category": 6,
            "isDir": 1,
            "size": 0,
            "serverTime": 1704904109,
            "serverFileName": "806"
        },
        {
            "fsId": 753780243476880,
            "path": "/VIP会员群/教育一区/----其他平台精品课程---/04.小苗/804-806/迷宫804",
            "category": 6,
            "isDir": 1,
            "size": 0,
            "serverTime": 1704904109,
            "serverFileName": "迷宫804"
        },
        {
            "fsId": 798749328944709,
            "path": "/VIP会员群/教育一区/----其他平台精品课程---/04.小苗/804-806/.mp3",
            "category": 2,
            "isDir": 0,
            "size": 42,
            "serverTime": 1704904109,
            "serverFileName": ".mp3"
        },
        {
            "fsId": 923549789260369,
            "path": "/VIP会员群/教育一区/----其他平台精品课程---/04.小苗/804-806/805拼音互动书2.pdf",
            "category": 4,
            "isDir": 0,
            "size": 4045148,
            "serverTime": 1704904109,
            "serverFileName": "805拼音互动书2.pdf"
        }
    ]
    }

# 根目录
s = requests.session()
s.get("https://path.dirts.cn/tH0c47D2P", headers={"dnt": "1"}, cookies={"Hm_lvt_0e42d925d22019079151233bdd075179": "1706080163", "Hm_lpvt_0e42d925d22019079151233bdd075179": "1706848968"})
s.get("https://path.dirts.cn/suda/server/front/business/info", headers={"authorization": "1ee2464b7a750097c77eb427969e4d4c", "dnt": "1"}, cookies={"Hm_lvt_0e42d925d22019079151233bdd075179": "1706080163", "Hm_lpvt_0e42d925d22019079151233bdd075179": "1706848968"})
s.get("https://path.dirts.cn/suda/server/front/business/images", headers={"authorization": "1ee2464b7a750097c77eb427969e4d4c", "dnt": "1"}, cookies={"Hm_lvt_0e42d925d22019079151233bdd075179": "1706080163", "Hm_lpvt_0e42d925d22019079151233bdd075179": "1706848968"})
s.get("https://path.dirts.cn/suda/server/front/business/path", headers={"authorization": "1ee2464b7a750097c77eb427969e4d4c", "dnt": "1"}, cookies={"Hm_lvt_0e42d925d22019079151233bdd075179": "1706080163", "Hm_lpvt_0e42d925d22019079151233bdd075179": "1706848968"})
  # {
    "msg": "ok",
    "errorCode": 0,
    "result": [
        {
            "id": 3632,
            "alias": null,
            "uk": 1102622597917,
            "serverFileName": "教育一区",
            "type": 1,
            "path": "/VIP会员群/教育一区",
            "fsId": null
        },
        {
            "id": 3633,
            "alias": null,
            "uk": 1102622597917,
            "serverFileName": "教育二区",
            "type": 1,
            "path": "/VIP会员群/教育二区",
            "fsId": null
        },
        {
            "id": 3634,
            "alias": null,
            "uk": 1102622597917,
            "serverFileName": "教育三区",
            "type": 1,
            "path": "/VIP会员群/教育三区",
            "fsId": null
        },
        {
            "id": 3635,
            "alias": null,
            "uk": 1102622597917,
            "serverFileName": "教育资料一",
            "type": 1,
            "path": "/教育资料一",
            "fsId": null
        },
        {
            "id": 3636,
            "alias": null,
            "uk": 1102622597917,
            "serverFileName": "英语专区",
            "type": 1,
            "path": "/VIP会员群/英语专区",
            "fsId": null
        },
        {
            "id": 6305,
            "alias": null,
            "uk": 1102622597917,
            "serverFileName": "好课收集",
            "type": 1,
            "path": "/VIP会员群/好课收集",
            "fsId": null
        }
    ]
    }
s.get("https://path.dirts.cn/suda/server/front/business/path", headers={"authorization": "1ee2464b7a750097c77eb427969e4d4c", "dnt": "1"}, cookies={"Hm_lvt_0e42d925d22019079151233bdd075179": "1706080163", "Hm_lpvt_0e42d925d22019079151233bdd075179": "1706848968"})
s.get("https://path.dirts.cn/manifest.json", headers={"DNT": "1"})
response = ls.content
decoded_response = response.decode('utf-8')
json_data = json.loads(decoded_response)

print(json_data)
"""
import requests
from requests import Session


class sudayun(object):
    def __init__(self, main_url="https://path.dirts.cn/tH0c47D2P") -> None:
        self.main_url = main_url


def main():
    s = Session()
    # Reddit will think we are a bot if we have the wrong user agent
    selenium_user_agent = driver.execute_script("return navigator.userAgent;")
    s.headers.update({"user-agent": selenium_user_agent})
    for cookie in driver.get_cookies():
        s.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])


if __name__ == "__main__":
    main()
