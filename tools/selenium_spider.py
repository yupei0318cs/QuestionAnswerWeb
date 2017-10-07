from selenium import webdriver
from scrapy.selector import Selector

#browser = webdriver.Chrome(executable_path="C:/Users/yupei0318/Downloads/chromedriver_win32/chromedriver.exe")
#知乎模拟登陆
#browser.get("https://detail.tmall.com/item.htm?spm=a222r.8694472.9630914069.7.xYvxq6&acm=lb-zebra-236689-2002742.1003.4.1763021&id=521025211566&scm=1003.4.lb-zebra-236689-2002742.ITEM_521025211566_1763021&skuId=3104821102761")
#browser.get("http:zhihu.com/#signin")
#print (browser.page_source)
#browser.find_element_by_css_selector(".view-signin input[name='account']").send_keys("yupei0318@gmail.com")
#browser.find_element_by_css_selector(".view-signin input[name='password']").send_keys("yumin716")

#browser.find_element_by_css_selector(".view-signin button.sign-button").click()

#browser.get("https://www.oschina.net/blog")
#browser.find_elements_by_css_selector("#loginname").send_keys("")
import time
time.sleep(5) #未加载完页面就开始登陆，所以找不到，因此需要等待加载完成
#browser.find_elements_by_css_selector(".info_list.password input[node-type='password']").send_keys("")
#browser.find_elements_by_css_selector(".info_list.login_btn a[node-type='submitBtn']").click()

#t_selector = Selector(text=browser.page_source)
#for i in range(3):
    #javascript 实现鼠标下拉功能
    #browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
    #time.sleep(2)
    #print (t_selector.css(".tm-promo-price .tm-price::text").extract())
    #browser.quit()

#设置chromdriver不加载图片
chrome_opt = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}
chrome_opt.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(executable_path="C:/Users/yupei0318/Downloads/chromedriver_win32/chromedriver.exe", chrome_options=chrome_opt)

browser.get("https://www.taobao.com")
#phantomjs, 无界面浏览器，多进程情况下phantomjs性能下降很严重