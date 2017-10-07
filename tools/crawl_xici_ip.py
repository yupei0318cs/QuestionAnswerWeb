__author__ = 'peipei'

import requests
from scrapy.selector import Selector
import MySQLdb

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="article_spider", charset="utf8")
cursor = conn.cursor()

def crawl_ips():
    #爬取西刺的免费ip代理
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
    for i in range(1568):

        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)

        selector = Selector(text=re.text)
        all_trs = selector.css("#ip_list tr")

        ip_list = []
        for tr in all_trs[1:]:
            speed_str = tr.css(".bar::attr(title)").extract_first()
            print (speed_str)
            if speed_str:
                speed = float(speed_str.split("秒")[0])

                all_texts = tr.css("td::text").extract()
                ip = all_texts[0]
                port = all_texts[1]
                proxy_type = all_texts[5]

                ip_list.append((ip, port, proxy_type, speed))

        for ip_info in ip_list:
            cursor.execute(
                "insert proxy_ip(ip, port, speed, proxy_type) VALUES('{0}', '{1}', {2}, 'HTTP')".format(
                ip_info[0], ip_info[1], ip_info[3])
            )
            conn.commit()

class GetIP(object):

    def delete_ip(self, ip):
        #数据库中删除无效ip
        delete_sql = """
            delete from proxy_ip where ip = '{0}'
        """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True
    def judge_ip(self, ip, port):
        #判断Ip是否可用
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {
                "http": proxy_url,

            }
            response = requests.get(http_url, proxies = proxy_dict)

            return True
        except Exception as e:
            print ("Invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print ("Effective IP")
                return true
            else:
                print ("invalid ip and port")
                self.delete_ip(ip)
                return False



    def get_random_ip(self):
        #从数据库中随机获取ip
        random_sql = """
            SELECT ip, port FROM proxy_ip
            ORDER BY RAND()
            LIMIT 1
        
        """
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]

            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()



if __name__ == "__main__":
    #crawl_ips()
    get_ip = GetIP()
    print (get_ip.get_random_ip())