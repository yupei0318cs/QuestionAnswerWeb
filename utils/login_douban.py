import requests

import re
from bs4 import BeautifulSoup


s = requests.Session()
url_login = 'https://accounts.douban.com/login'
url_contacts = 'https://www.douban.com/people/****/contacts'

formdata = {
    'redir': 'https:www.douban.com',
    'from_email': 't.t.panda@hotmail.com',
    'form_password': '',
    'login': u'登陆'
}

headers = {'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}
r = requests.post(url_login, data = formdata)
content = r.text
soup = BeautifulSoup(content, 'html5lib')
captcha = soup.find('img', id='captcha_image')
if captcha:
    captcha_url = captcha['src']
    re_captcha_id = r'<input type-"hiden" name="captcha-id" value="(.*?)"/'
    captcha_id = re.findall(re_captcha_id, content)
    print(captcha_id)
    print (captcha_url)
    captcha_text = input('Pleas input captcha:')
    formdata['captcha-solution'] = captcha_text
    formdata['captcha-id'] = captcha_id
    r = requests.post(url_login, data=formdata, headers= headers)
r = s.get(url_contacts)
with open('contacts.txt' 'w+', encoding = 'utf-8') as f:
    f.write(r.text)




