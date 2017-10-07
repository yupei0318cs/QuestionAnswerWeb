import re
import time
from selenium import webdriver


mr = re.match(r'\d{3}-\d{3,8}', '001-223456')
print (mr)

#分组
m =  re.match(r'(\d{3})-(\d{3,8})$', '010-12345')
print (m.groups())
print (m.group(0))
print (m.group(1))
print (m.group(2))

t = '20:15:45'
n = re.match(r'^(0[0-9]|1[0-9]|2[0-3]|[0-9])\:(0[0-9]|1[0-9]|2[0-3]|3[0-9]|4[0-9]|5[0-9]|[0-9])\:(0[0-9]|1[0-9]|2[0-3]|3[0-9]|4[0-9]|5[0-9]|[0-9])$', t)
print (n.groups())

#分割字符串
p = re.compile(r'\d+')
print (p.split('one1two22three333'))


browser = webdriver.Chrome()
browser.set_page_load_timeout(30)
browser.get('http://www.17huo.com/search.html?sq=2&keyword=%E5%A4%A7%E8%A1%A3')
#有多少页商品
page_info = browser.find_element_by_css_selector('body > div.wrap > div.pagem.product_list_pager > div')
page_num = int(page_info.text.split(',')[0].split(' ')[1])
print ('商品有%d页' % page_num)

for page in range(page_num):
    if page > 2:
        break
    print ('第%d页' % (page + 1))
    url = 'http://www.17huo.com/search.html?sq=2&keyword=%E5%A4%A7%E8%A1%A3&page=' + str(page+1)
    browser.get(url)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    goods = browser.find_element_by_css_selector('body > div.wrap > div:nth-child(2) > div.p_main > ul').find_elements_by_tag_name('li')
    print ('第%d页有%d件商品' % ((page + 1), len(goods)) )
    for good in goods:
        try:
            title = good.find_elements_by_tag_name('p class="item_title"')

            title = good.find_element_by_css_selector('a:nth-child(1) > p:nth-child(2)').text
            #title2 = good.find_element_by_css_selector('li:nth-child(2) > a:nth-child(1) > p:nth-child(2)').text
            #title = good.find_elements_by_xpath('/ html / body / div[5] / div[2] / div[4] / ul / li[18] / a[1] / p[2]')
            price = good.find_element_by_css_selector('div > a > span').text
            print (title, price)
        except:
            print ('Exception!')
