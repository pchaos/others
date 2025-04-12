from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class RecorderTest(BaseCase):
    def test_recording(self):
        self.open("http://192.168.124.80:5344/教育/编程开发")
        self.click('p[title="00-【计算机基础197GB】"]')
        self.click('p[title="Git从入门到精通"]')
        self.click('p[title="01-课程导读.mp4"]')
