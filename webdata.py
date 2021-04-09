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
def sort_price_array(lis):
    a=1
req=requests.get('https://www.expat.com/en/housing/middle-east/iran/tehran/')
r=lambda x:'Get Url' if x==200  else 'Get Url Failed!'
print(r(req.status_code))
sort=bs4.BeautifulSoup(req.text,'html.parser')
find=sort.find_all('span', attrs={'class':'classified-wrapper__category'})
find_attrs=re.findall(r'[0-9]+',str(find))
values=build(find_attrs)
print(values)
find_price_text=sort.find_all('span', attrs={'class':'classified-wrapper__price'})
find_price=re.findall(r'\s+.*\s(\d.\d+).per.\w+',str(find_price_text))
find_unit=re.findall(r'\s+(.*)\s\d+.+\d.per.\w+',str(find_price_text))
find_dur=re.findall(r'\s+.*\s\d.\d+.per.(\w+)',str(find_price_text))
print(find_price)
print(find_unit)
print(find_dur)