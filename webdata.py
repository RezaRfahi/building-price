import requests
import bs4
import  re
def build(lis):
    count=1
    attrs=list()
    for i in lis:
        if count%3!=0:
            attrs.append(i)
        count=count+1
    return attrs
req=requests.get('https://www.expat.com/en/housing/middle-east/iran/tehran/')
r=lambda x:'Get Url' if x==200  else 'Get Url Failed!'
print(r(req.status_code))
sort=bs4.BeautifulSoup(req.text,'html.parser')
find=sort.find_all('span', attrs={'class':'classified-wrapper__category'})
find_attrs=re.findall(r'[0-9]+',str(find))
print(build(find_attrs))