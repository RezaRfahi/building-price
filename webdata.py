import requests
import bs4
import  re
def build(lis):
    cunt=1
    attrs=[]
    varlist=[]
    listcount=0
    for i in lis:
        if cunt%3!=0:
            varlist.append(i)
            listcount=listcount+1
            if listcount==2:
                attrs.append(varlist)
                listcount=0
                varlist=[]
        cunt=cunt+1
    return attrs
req=requests.get('https://www.expat.com/en/housing/middle-east/iran/tehran/')
r=lambda x:'Get Url' if x==200  else 'Get Url Failed!'
print(r(req.status_code))
sort=bs4.BeautifulSoup(req.text,'html.parser')
find=sort.find_all('span', attrs={'class':'classified-wrapper__category'})
find_attrs=re.findall(r'[0-9]+',str(find))
print(build(find_attrs))