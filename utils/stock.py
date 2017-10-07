import requests
import threading
def display_info(code):
    url = "http://hq.sinajs.cn/list=" + code
    response = requests.get(url).text
    print (response)
    #javascript_info = response.read()
    #print (javascript_info)

def single_thread(codes):
    for code in codes:
        code = code.strip()
        display_info(code)


def multi_thread(tasks):
    #threads = [threading.Thread(target = single_thread, args = (codes)) for codes in tasks]
    threads = []
    for t in tasks:
        threads.append(threading.Thread(target = single_thread, args = (t,)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()



if  __name__ == '__main__':
    codes = ['sh601006', 'sh601007', 'sh601008', 'sh601005', 'sh601099']
    thread_len = int(len(codes) / 4)
    t1 = codes[0: thread_len]
    t2 = codes[thread_len: thread_len * 2]
    t3 = codes[thread_len * 2: thread_len * 3]
    t4 = codes[thread_len * 3:]
    print (t1, t2, t3, t4)
    multi_thread([t1, t2, t3, t4])


    