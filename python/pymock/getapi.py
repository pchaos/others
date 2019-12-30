import requests
 
def api():
    response = requests.get('https://www.nourlsohu.com/')
    return response
    