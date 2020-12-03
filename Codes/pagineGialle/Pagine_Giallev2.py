import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://www.paginegialle.it/ricerca/arredo%20su%20misura/Faenza?'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')


temp = []
# for aa in soup.find_all('span', class_='tel'):
for aa in soup.find_all('span.tel.dropdown-item'):
    temp.append(aa.text)


# temp.pop(0)
# for num, i in enumerate(temp):
#     temp[num] = i.replace('\n', '')
    
# for num, i in enumerate(temp):
#     temp[num] = i.split('\t')

# for i in range(len(temp)):
#     while '' in temp[i]:
#         for ind, j in enumerate(temp[i]):
#             if temp[i][ind] == '':
#                 temp[i].pop(ind)

# clients = []
# address = []
# lat = []
# long = []
       
# for i in range(len(temp)):
#     clients.append(temp[i][0]) # first element is client name
    
#     # Check if clients contains km info as often happens
#     pattern1 = re.compile(r'\d\d.\d(km)')
#     pattern2 = re.compile(r'\d.\d(km)')
#     try:
#         matches = pattern1.finditer(clients[i])
#         _ = list(matches)
#         start = _[0].span(0)[0] #beginning of first coord
#         temp[i][1] = clients[i][start:] + ' ' + temp[i][1]
#         clients[i] =  clients[i][:start]
#     except:
#         try:
#             matches = pattern2.finditer(clients[i])
#             _ = list(matches)
#             start = _[0].span(0)[0] #beginning of first coord
#             temp[i][1] = clients[i][start:] + ' ' + temp[i][1]
#             clients[i] =  clients[i][:start]
#         except:
#             pass    
    
#     # Clean Address, deleting useless things
#     pattern1 = re.compile(r'\d\d.\d(km)')
#     pattern2 = re.compile(r'\d.\d(km)')
#     try:
#         matches = pattern1.finditer(temp[i][1])
#         _ = list(matches)
#         end = _[0].span(0)[1] #beginning of first coord
#         try:
#             concat = temp[i][1][end:] + ' ' + temp[i][2]
#             address.append(concat)
#         except:
#             address.append(temp[i][1][end:])
#     except:
#         try:
#             matches = pattern2.finditer(temp[i][1])
#             _ = list(matches)
#             end = _[0].span(0)[1] #beginning of first coord
#             try:
#                 concat = temp[i][1][end:] + ' ' + temp[i][2]
#                 address.append(concat)
#             except:
#                 address.append(temp[i][1][end:])
#         except:
#             try:
#                 concat = temp[i][1] + ' ' + temp[i][2]
#                 address.append(concat)
#             except:
#                 address.append(temp[i][1])
    
# # split address and geo coordinates   

# pattern = re.compile(r'\d\d\.')      
# for num, i in enumerate(address):  
#     matches = pattern.finditer(i)
#     _ = list(matches)
#     start = _[0].span(0)[0] #beginning of first coord
#     mid = _[1].span(0)[0] # beginning of second coord
#     stop = _[1].span(0)[1] # beginning of second coord
#     lat.append(address[num][start:mid])
#     long.append(address[num][mid:])
#     address[num] = address[num].replace(address[num][start:],'')   
    
# # find cap and replace with '' 
#     #TODO: store cap value if useful
# for num, i in enumerate(address):
#     try:
#         i = re.sub(r'\d\d\d\d\d', ' ', i)
#         address[num] = i
#     except:
#         pass           
    
# PagineGialle = {'Faenza':{'Nome':clients, 'Indirizzo':address, 'Lat.':lat, 'Lon':long}}    
    
    
    
    




# df = pd.DataFrame.from_dict({(i,j): PagineGialle[i][j] 
#                             for i in PagineGialle.keys() 
#                             for j in PagineGialle[i].keys()},
#                         orient='columns')    

# # df.to_excel('test.xlsx')
# # # print(soup.get())

