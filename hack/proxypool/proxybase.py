from fake_useragent import UserAgent

ua = UserAgent()

def getUserAgent():
    return ua.random
