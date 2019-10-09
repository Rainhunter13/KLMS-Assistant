import requests
from bs4 import BeautifulSoup
import time

def notices(username, password):

    r = requests.Session()

    headersPost = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ko;q=0.6",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://ksso.kaist.ac.kr/iamps/IntegratedLogin.do",
        "Content-Type": "application/x-www-form-urlencoded",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    data = {
        "refererUrl": "https://klms.kaist.ac.kr/login.php",
        "message": "",
        "userSe": "USR",
        "j_username": "",
        "id": username,
        "password": password
    }

    headersGet = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ko;q=0.6',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://ksso.kaist.ac.kr/iamps/IntegratedAuth.do',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ko;q=0.6',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://klms.kaist.ac.kr/login.php',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    r.get("https://ksso.kaist.ac.kr/iamps/requestLogin.do", headers = headers1)
    time.sleep(1)
    r.post(url="https://ksso.kaist.ac.kr/iamps/IntegratedAuth.do", headers=headersPost, data=data)
    time.sleep(1)
    text = r.get('http://klms.kaist.ac.kr/', headers=headersGet)

    soup = BeautifulSoup(text.text.replace('\r', '').replace('\n', '').replace('\\', '').replace('rn', ''), 'html.parser')
    notice = soup.find(attrs = {'class' : 'notification_list'})
    notices1 = notice.find_all('a')
    notices2 = notices1

    s = "Your last notices are:\n\n"
    for i in range(len(notices1)):
        if (notices1[i].img == None):
            s1 = notices1[i].find('h5')
            s2 = notices2[i].find('p')
            s2.span.decompose()
            s = s + s1.string + ":\n" + s2.string + "\n\n"
        else:
            s1 = notices1[i]
            s1.img.decompose()
            s1 = s1.find('h5')
            s2 = notices2[i].find('p')
            if (s1.img != None):
                s1.img.decompose()
            s2.span.decompose()
            s = s + s1.string + ":\n" + s2.string + "\n\n"
    return s
