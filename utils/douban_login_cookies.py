import requests
headers = {'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}
cookies = {'cookie': ''}
url = 'https://accounts.douban.com'
r = requests.get(url, cookies = cookies, headers = headers)
with open('douban2.txt' 'wb+', encoding = 'utf-8') as f:
    f.write(r.text)
