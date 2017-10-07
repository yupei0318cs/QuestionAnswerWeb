from bs4 import BeautifulSoup

soup = BeautifulSoup(open('test.html'))
print (soup.prettify())

print (type(soup.title))
print (soup.title.name)
print (soup.title)
print (soup.title.string)

#comment
print (type(soup.a.string))
print (soup.a.string)

for item in soup.body.contents:
    print (item.name)
#CSS查询
print (soup.select('.sister'))
print (soup.select('#link1'))
print (soup.select('head > title'))

a_s = soup.select('a')
for a in a_s:
    print (a)

