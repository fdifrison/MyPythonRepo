import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://www.paginegialle.it/ricerca/arredo%20su%20misura/Faenza?'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')


Clienti = {'Faenza':{'Nome':[], 'Indirizzo':[]}}

temp = []
body = soup.body
for aa in soup.find_all('header'):
    temp.append(aa.text)

temp.pop(0)
for num, i in enumerate(temp):
    temp[num] = i.replace('\n', '')
    
for num, i in enumerate(temp):
    temp[num] = i.split('\t')

for i in range(len(temp)):
    while '' in temp[i]:
        for ind, j in enumerate(temp[i]):
            if temp[i][ind] == '':
                temp[i].pop(ind)

Clients = []
Address = []
for i in range(len(temp)):
    Clients.append(temp[i][0])
    try:
        Address.append(''.join(temp[i][1:]))     
    except:
        Address.append(temp[i][1])
       
    pattern1 = re.compile(r'\d\d.\d(km)')
    pattern2 = re.compile(r'\d.\d(km)')
    try:
        matches = pattern1.finditer(Clients[i])
        _ = list(matches)
        start = _[0].span(0)[0] #beginning of first coord
        add2Address = Clients[i][start:]
        Clients[i] = Clients[i][:start]
        Address[i] = add2Address + ' ' +  Address[i]
    except:
        try: 
            matches = pattern1.finditer(Clients[i])
            _ = list(matches)
            start = _[0].span(0)[0] #beginning of first coord
            add2Address = Clients[i][start:]
            Clients[i] = Clients[i][:start]
            Address[i] = add2Address + ' ' +  Address[i]
        except:
            check = False
            pass


for num, i in enumerate(Address):
    try:
        i = re.sub(r'a \d\d.\d(km)', '', i)
        Address[num] = i
    except:
        pass
    try:
        i = re.sub(r'a \d.\d(km)', '', i)
        Address[num] = i
    except:
        pass
    try:
        i = re.sub(r'\d.\d(km)', '', i)
        Address[num] = i
    except:
        pass
    # print(i)

# split address and coordinates   
lat = []
long = []
       
pattern = re.compile(r'\d\d\.')      
for num, i in enumerate(Address):  
    matches = pattern.finditer(i)
    _ = list(matches)
    start = _[0].span(0)[0] #beginning of first coord
    mid = _[1].span(0)[0] # beginning of second coord
    stop = _[1].span(0)[1] # beginning of second coord
    lat.append(Address[num][start:mid])
    long.append(Address[num][mid:])
    Address[num] = Address[num].replace(Address[num][start:],'')
    
# find cap and replace with '' 
for num, i in enumerate(Address):
    try:
        i = re.sub(r'\d\d\d\d\d', ' ', i)
        Address[num] = i
    except:
        pass           



# df = pd.DataFrame.from_dict({(i,j): Clienti[i][j] 
#                            for i in Clienti.keys() 
#                            for j in Clienti[i].keys()},
#                        orient='columns')    

# df.to_excel('test.xlsx')
# # print(soup.get())

