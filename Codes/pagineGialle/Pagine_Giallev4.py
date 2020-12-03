import re
import requests
from bs4 import BeautifulSoup
import pandas as pd



def ClientsFinder(Queries, Cities, Location, Clients, Address, Lat, Long):
    
    maxPage = 100
    pages =[f'/p-{i+2}' for i in range(maxPage)]
    pages.insert(0, '')
    
    for page in pages:
        
        clients = []
        address = []
        lat = []
        long = []
        location = []
        
        URL = 'https://www.paginegialle.it/ricerca/{}/{}{}'.format(Queries, Cities, page)
        page = requests.get(URL)
        if not page.ok: #♦ check if webpage exist
            break
        print(URL)
        
        soup = BeautifulSoup(page.content, 'html.parser')
        
        
        temp = []
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
        
        
               
        for i in range(len(temp)):
            clients.append(temp[i][0]) # first element is client name
            
            # Check if clients contains km info as often happens
            pattern1 = re.compile(r'\d\d.\d(km)')
            pattern2 = re.compile(r'\d.\d(km)')
            try:
                matches = pattern1.finditer(clients[i])
                _ = list(matches)
                start = _[0].span(0)[0] #beginning of first coord
                temp[i][1] = clients[i][start:] + ' ' + temp[i][1]
                clients[i] =  clients[i][:start]
            except:
                try:
                    matches = pattern2.finditer(clients[i])
                    _ = list(matches)
                    start = _[0].span(0)[0] #beginning of first coord
                    temp[i][1] = clients[i][start:] + ' ' + temp[i][1]
                    clients[i] =  clients[i][:start]
                except:
                    pass    
            
            # Clean Address, deleting useless things
            pattern1 = re.compile(r'\d\d.\d(km)')
            pattern2 = re.compile(r'\d.\d(km)')
            try:
                matches = pattern1.finditer(temp[i][1])
                _ = list(matches)
                end = _[0].span(0)[1] #beginning of first coord
                try:
                    concat = temp[i][1][end:] + ' ' + temp[i][2]
                    address.append(concat)
                except:
                    address.append(temp[i][1][end:])
            except:
                try:
                    matches = pattern2.finditer(temp[i][1])
                    _ = list(matches)
                    end = _[0].span(0)[1] #beginning of first coord
                    try:
                        concat = temp[i][1][end:] + ' ' + temp[i][2]
                        address.append(concat)
                    except:
                        address.append(temp[i][1][end:])
                except:
                    try:
                        concat = temp[i][1] + ' ' + temp[i][2]
                        address.append(concat)
                    except:
                        address.append(temp[i][1])
            
        # split address and geo coordinates   
        
        pattern = re.compile(r'\d\d\.')      
        for num, i in enumerate(address): 
            try:
                matches = pattern.finditer(i)
                _ = list(matches)
                start = _[0].span(0)[0] #beginning of first coord
                mid = _[1].span(0)[0] # beginning of second coord
                stop = _[1].span(0)[1] # beginning of second coord
                lat.append(address[num][start:mid])
                long.append(address[num][mid:])
                address[num] = address[num].replace(address[num][start:],'')
            except:
                lat.append('-')
                long.append('-')
                pass
            
        # find cap and replace with '' 
            #TODO: store cap value if useful
        for num, i in enumerate(address):
            try:
                i = re.sub(r'\d\d\d\d\d', ' ', i)
                address[num] = i
            except:
                pass           
            
        Clients += clients
        Address += address
        Lat += lat
        Long += long
        
        location = [Cities for i in range(len(clients))]
        Location += location
            

    
City = ['Faenza', 'Rimini']
query = ['arredo su misura', 'falegname']



    
PagineGialle = {}
for c in City:
    for q in query:
        Location = []
        Clients = []
        Address = []
        Lat = []
        Long = []
        if ' ' in query:
            q = q.replace(' ', '%20')
        print(c, q)
        ClientsFinder(q, c, Location, Clients, Address, Lat, Long) 
        PagineGialle[c + ' - ' + q.replace('%20', ' ').capitalize()] =  {'Nome':Clients,
                                                                         'Indirizzo':Address,
                                                                         'City': Location,
                                                                         'Lat.':Lat, 'Lon':Long}
        
df = []
for i, j in PagineGialle.items():
    df.append(pd.DataFrame.from_dict(PagineGialle[i]))
    
# PagineGialle = {City + ' - ' + query.capitalize() :
#                 {'Nome':Clients, 'Indirizzo':Address,
#                  'City': Location, 'Lat.':Lat, 'Lon':Long}}  
    
    
# df = pd.DataFrame.from_dict({(i,j): PagineGialle[0][i][j] 
#                             for i in PagineGialle.keys() 
#                             for j in PagineGialle[0][i].keys()},
#                             orient='columns')    

# df.to_excel('test.xlsx')


