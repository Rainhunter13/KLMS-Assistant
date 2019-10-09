import requests
from bs4 import BeautifulSoup

def portal_login(username, password):

    r = requests.Session()

    headersPost = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ko;q=0.6",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "https://portalsso.kaist.ac.kr/login.ps",
        "Content-Type": "application/x-www-form-urlencoded",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    data = {
        "saveid": "on",
        "langKnd": "en",
        "userId": username,
        "password": password
    }

    lol_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ko;q=0.6',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://portal.kaist.ac.kr/portal/default/home/today',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    kek_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ko;q=0.6',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://portal.kaist.ac.kr/portal/default/home/today',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    r.post(url = "https://portalsso.kaist.ac.kr/ssoProcess.ps?returnURL=portal.kaist.ac.kr%2Fuser%2FssoLoginProcess.face%3Ftimestamp%3D1565937295240&timestamp=1565937303802", headers=headersPost, data=data)
    r.get('https://board.kaist.ac.kr/kaist/bd/portalMainTab/list.face?lang_knd=en&userAgent=Chrome&isMobile=false&', headers=lol_headers)
    text = r.get(url = "https://portal.kaist.ac.kr/portal/default/home/today", headers = kek_headers)

    soup = BeautifulSoup(text.text.replace('\r', '').replace('\n', '').replace('\\', '').replace('rn', ''), 'html.parser')
    student_notices = soup.find_all('a', href = True, title = True)
    i = 0
    while i < len(student_notices):
        if student_notices[i]['href'].find('student_notice')==-1:
            del student_notices[i]
        else:
            i += 1

    arr = []
    for i in range(len(student_notices)):
        arr.append(student_notices[i]['title'])

    i = 1
    while i < len(arr):
        if arr[i] in arr[:i]:
            del arr[i]
        else:
            i = i + 1

    s = "Last Student Notices are:\n"
    for i in range (len(arr)):
        s = s + arr[i] + "\n"

    return s