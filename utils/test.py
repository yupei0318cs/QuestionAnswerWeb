i = 0
j = 0
while i<3:
    while j<=3:
        if j==3:
            break
        print (i, j)
        j += 1
    print ("hereh")
    i += 1
def g(x):
    return x * 5
def f(x):
    return g(x)+ 100
print (f(5))
li = [1, 2]
li2= [4, 5,3, 5]
li.extend(li2)
li.pop(2)
print (sorted(li))
li.sort()
print (li)
l2 = [[5,2], [3, 8], [2, 11], [7,6]]
l2.sort(key = lambda x: x[0])
def item_key(x):
    return x[0]
l2.sort(key = item_key)
print (l2)
#print (f(lambda x: x * 100, 100))
for i in range(5, -1, -1):
    print (i)
tp = (1,2,4)
s = set([1,3,3,3])
dict = {1: 2, 3:4}
print (dict[1])
print (tp[0], s)
x = [1,2,4,4,5,3]
print (x[-1:-4:-1])
print (x[::-1])
print (x[3::-1])

import threading
from time import sleep
def thread_func(x):
    sleep(2)
    print ('%d' % (x *100))


threads = []
for i in range(5):
    threads.append(threading.Thread(target =  thread_func, args = (100, )))
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

try:
    r = 10 / 0
except ZeroDivisionError as e:
    print (type(e))
    print (e)
finally:
    print ("alway here")
import json
obj = {"one": 1, "two": 2, "three": [1,2,4]}
encoded = json.dumps(obj)
print (encoded)
decoded = json.loads(encoded)
print (decoded["one"])
from xml.dom  import minidom
doc = minidom.parse('book.xml')

root = doc.documentElement
print (type(root))
print (root.nodeName)
books = root.getElementsByTagName('book')
for book in books:
    titles = book.getElementsByTagName('title')
    prices = book.getElementsByTagName('price')
    title = titles[0].childNodes[0].nodeValue
    price = prices[0].childNodes[0].nodeValue

    print (title, price)
