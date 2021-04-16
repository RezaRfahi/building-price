from sklearn import tree
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
            varlist.append(int(i))
            listcount=listcount+1
            if listcount==2:
                attrs.append(varlist)
                listcount=0
                varlist=[]
        cunt=cunt+1
    return attrs
####################################################
def sort_price_array(list_price,length):
    price=list()
    count=0
    for i in list_price:
        price.append(int(i.replace(',', '')))
        count=count+1
        if count==length:
            break
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
def answer(Ml,Solve_liet):
    find_answer=Ml.predict([Solve_liet])
    return find_answer
###################################################
req=requests.get('https://www.expat.com/en/housing/middle-east/iran/tehran/')
r=lambda x:'Get Url' if x==200  else 'Get Url Failed!'
print(r(req.status_code))
sort=bs4.BeautifulSoup(req.text,'html.parser')
find=sort.find_all('span', attrs={'class':'classified-wrapper__category'})
find_attrs=re.findall(r'[0-9]+',str(find))
values=build(find_attrs)
find_price_text=sort.find_all('span', attrs={'class':'classified-wrapper__price'})
find_price=re.findall(r'\s+(\d.*..+.\d).+',str(find_price_text))
find_unit=re.findall(r'\s+(.*)\s\d+.+\d.per.\w+',str(find_price_text))
duration=re.findall(r'\s+.*\s\d.\d+.per.(\w+)',str(find_price_text))
price=sort_price_array(find_price,len(values))
price=change_to_rial(price,find_unit)
find_dur=re.findall(r'\s+.*\s\d.\d+.per.(\w+)',str(find_price_text))
rooms_list=list()
home_meter=list()
for room,meter in values:
    rooms_list.append(room)
    home_meter.append(meter)
for i in range(0,len(rooms_list)):
    print('%i meter , %i room(s) , %i Rial per %s'%(home_meter[i],rooms_list[i],price[i],duration[i]))
####################################################
flag=True
ml=tree.DecisionTreeClassifier()
ml.fit(values,price)
while flag:
    solve_list=[]
    insert_rooms=int(input('Insert your home rooms for find : '))
    solve_list.append(insert_rooms)
    insert_meter=int(input('Insert your home meters for find : '))
    solve_list.append(insert_meter)
    print(answer(ml,solve_list))
    continue_question=(input('Do you want countinue y/n : '))
    if continue_question.upper()=='Y':
        flag=True
    elif continue_question.upper()=='N':
        flag=False