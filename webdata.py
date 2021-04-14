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
####################################################
def sort_price_array(list_price):
    price=list()
    for i in list_price:
        price.append(int(i.replace(',', '')))
    return price
####################################################
def change_to_rial(list_price,list_unit):
    req_dollar=requests.get('https://www.tgju.org/')
    sort_dollar=bs4.BeautifulSoup(req_dollar.text,'html.parser')
    find_dollar_text=sort_dollar.find_all('li',attrs={'id':'l-price_dollar_rl'})
    find_dollar_text_bs=bs4.BeautifulSoup(str(find_dollar_text),'html.parser')
    find_dollar_price=find_dollar_text_bs.find_all('span',attrs={'class':'info-price'})
    dollar_price=re.findall(r'.(\d+.+\d).+',str(find_dollar_price))
    dollar_price=int(dollar_price[0].replace(',', ''))
####
    req_eur=requests.get('https://www.tgju.org/currency')
    sort_eur=bs4.BeautifulSoup(req_eur.text,'html.parser')
    find_eur_text=sort_eur.find_all('tr',attrs={'data-market-row':'price_eur'})
    find_eur_text_bs=bs4.BeautifulSoup(str(find_eur_text),'html.parser')
    find_eur_price=find_eur_text_bs.find_all('td',attrs={'class':'nf'})
    eur_price=re.findall(r'.+.>(\d+.+\d+.)<.+.',str(find_eur_price))
    eur_price=int(eur_price[0].replace(',',''))
####
    rial_price=list()
    for i in range(0,len(list_price)):
        if list_unit[i]=='$':
            rial_price.append(list_price[i]*dollar_price)
        elif list_unit[i]=='€':
            rial_price.append(list_price[i]*eur_price)
    return rial_price

####################################################
req=requests.get('https://www.expat.com/en/housing/middle-east/iran/tehran/')
r=lambda x:'Get Url' if x==200  else 'Get Url Failed!'
print(r(req.status_code))
sort=bs4.BeautifulSoup(req.text,'html.parser')
find=sort.find_all('span', attrs={'class':'classified-wrapper__category'})
find_attrs=re.findall(r'[0-9]+',str(find))
values=build(find_attrs)
find_price_text=sort.find_all('span', attrs={'class':'classified-wrapper__price'})
find_price=re.findall(r'\s+.*\s(\d.\d+).per.\w+',str(find_price_text))
find_unit=re.findall(r'\s+(.*)\s\d+.+\d.per.\w+',str(find_price_text))
duration=re.findall(r'\s+.*\s\d.\d+.per.(\w+)',str(find_price_text))
price=sort_price_array(find_price)
price=change_to_rial(price,find_unit)
find_dur=re.findall(r'\s+.*\s\d.\d+.per.(\w+)',str(find_price_text))
print(sort_price_array(find_price))
print(find_unit)
print(find_dur)