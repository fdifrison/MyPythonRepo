import requests
import pandas as pd
from bs4 import BeautifulSoup
from collections import OrderedDict
from selenium import webdriver
import re

# initialize containers
temp = {}
output = OrderedDict()


# READ SQUADRE AND THEIR ID
url = f'https://leghe.fantacalcio.it/mattia-calisesi-cup/classifica'
path = r'D:\DataScience\Python\Codes\Pisco\chromedriver_win32\chromedriver'
driver = webdriver.Chrome(executable_path = path)
driver.get(url)
header = driver.find_elements_by_xpath("//div[@class='media-body']")
tables = driver.find_elements_by_tag_name("table")
temp['tables'] = [t.get_attribute('innerHTML') for t in tables]


players = []
for num, t in enumerate(temp['tables']):
    FIND = list(iter(BeautifulSoup(t,'lxml').find_all("td", {"data-key": "teamName"})))
    players.append([f.prettify().splitlines() for f in FIND])

output['T'] = {}
for p in players[0]: 
     output['T'][p[2].strip().split('=')[-1][:-2]] = {'Name' : p[3].strip()}
    
# FINE INIZIALIZZAZIONE


# PARSING PER OGNI GIORNATA

# GIORNATA
giornata = 1

output_g = {}



url = f'https://leghe.fantacalcio.it/mattia-calisesi-cup/formazioni/{giornata}'
path = r'D:\DataScience\Python\Codes\Pisco\chromedriver_win32\chromedriver'
driver = webdriver.Chrome(executable_path = path)
driver.get(url)
header = driver.find_elements_by_xpath("//div[@class='media-left']") # try to find team id from pictures
tables = driver.find_elements_by_tag_name("table")

# SQUADRE
temp['header'] = [h.get_attribute('innerHTML') for h in header]
temp['header_clean'] = [BeautifulSoup(h,'lxml').prettify().splitlines() for h in temp['header']]


#remove admin header # TODO check if admin is always last element
del temp['header_clean'][-1]
del temp['header_clean'][-1]

# find tema id from team pictures... TODO find a better way
output_g['T'] = {t[3].split('/')[-2].split('_')[0]:{} for t in temp['header_clean']}
if 'no' in output_g['T'].keys():
    output_g['T'] = {t[6].split('/')[-2].split('_')[0]:{} for t in temp['header_clean']}
if 'no' in output_g['T'].keys():
    print('ERROR, cant find team ID')


for team in output_g['T'].keys(): 
    output_g['T'][team]['titolari'] = {'id':[],'nome':[],'ruolo':[],'team':[],
                                     'bonus':[], 'voto':[], 'totale':[], 'mantra':[]}
    output_g['T'][team]['panchina'] = {'id':[],'nome':[],'ruolo':[],'team':[],
                                     'bonus':[], 'voto':[], 'totale':[], 'mantra':[]}
    output_g['T'][team]['formazione'] = {'inizio': 0, 'fine': 0}
    output_g['T'][team]['bonus'] = {}




# FORMAZIONE
header = driver.find_elements_by_xpath("//div[@class='media-body']")
temp['header'] = [h.get_attribute('innerHTML') for h in header]
temp['header_clean'] = [BeautifulSoup(h,'lxml').prettify().splitlines() for h in temp['header']]

for team, t in zip(output['T'].keys(), temp['header_clean']): 
    output_g['T'][team]['formazione']['inizio'] =  t[6].strip()
    try: # if formazione es 4-4-2
        output_g['T'][team]['formazione']['fine'] = re.search(r'\d-\d-\d', t[8])[0] # dopo sostituzioni
    except: # if formazione es 4-2-2-2
        output_g['T'][team]['formazione']['fine'] = re.search(r'\d-\d-\d-\d', t[8])[0] # dopo sostituzioni
        

temp['tables'] = [t.get_attribute('innerHTML') for t in tables]

players = []
for num, t in enumerate(temp['tables']):
    FIND = list(iter(BeautifulSoup(t,'lxml').find_all("td", {"data-key": "name"})))
    players.append([f.prettify().splitlines() for f in FIND])
    
# titolari nome ruolo id
for team, titolari in zip(output_g['T'].keys(), players[0::4]): 
    for t in titolari: 
        output_g['T'][team]['titolari']['nome'].append(t[9].strip())
        output_g['T'][team]['titolari']['ruolo'].append(t[4].strip())
        output_g['T'][team]['titolari']['id'].append(re.search(r'[0-9]*',t[8].strip().split('/')[-1])[0])

# panchina nome ruolo id
for team, titolari in zip(output_g['T'].keys(), players[1::4]): 
    for t in titolari: 
        output_g['T'][team]['panchina']['nome'].append(t[9].strip())
        output_g['T'][team]['panchina']['ruolo'].append(t[4].strip())
        output_g['T'][team]['panchina']['id'].append(re.search(r'[0-9]*',t[8].strip().split('/')[-1])[0])
    
# squadra giocatore
players = []
for num, t in enumerate(temp['tables']):
    FIND = list(iter(BeautifulSoup(t,'lxml').find_all("td", {"data-key": "team"})))
    players.append([f.prettify().splitlines() for f in FIND])
 
# titolari squadra
for team, titolari in zip(output_g['T'].keys(), players[0::4]): 
    for t in titolari: 
        output_g['T'][team]['titolari']['team'].append(t[2].strip())

# panchina squadra
for team, titolari in zip(output_g['T'].keys(), players[1::4]): 
    for t in titolari: 
        output_g['T'][team]['panchina']['team'].append(t[2].strip())


# BONUS
players = []
for num, t in enumerate(temp['tables']):
    FIND = list(iter(BeautifulSoup(t,'lxml').find_all("td", {"data-key": "bonus"})))
    players.append([f.prettify().splitlines() for f in FIND])

# titolari voto
for team, titolari in zip(output_g['T'].keys(), players[0::4]): 
    for t in titolari:
        bonus = 0
        for l in t:
            if re.search(r'\(.[0-9].[0-9]\)', l):
                b = re.search(r'\(.[0-9].[0-9]\)', l)[0].strip('(').strip(')')
                bonus += float(b)        
            elif re.search(r'\(.[0-9]\)', l):
                b = re.search(r'\(.[0-9]\)', l)[0].strip('(').strip(')')
                bonus += float(b)        
            else:
                bonus += 0
                
        output_g['T'][team]['titolari']['bonus'].append(bonus)

# panchina voto
for team, titolari in zip(output_g['T'].keys(), players[1::4]): 
    for t in titolari: 
        bonus = 0
        for l in t:
            if re.search(r'\(.[0-9].[0-9]\)', l):
                b = re.search(r'\(.[0-9].[0-9]\)', l)[0].strip('(').strip(')')
                bonus += float(b)        
            elif re.search(r'\(.[0-9]\)', l):
                b = re.search(r'\(.[0-9]\)', l)[0].strip('(').strip(')')
                bonus += float(b)        
            else:
                bonus += 0
        
        output_g['T'][team]['panchina']['bonus'].append(bonus) 

  
# VOTO
players = []
for num, t in enumerate(temp['tables']):
    FIND = list(iter(BeautifulSoup(t,'lxml').find_all("td", {"data-key": "vote"})))
    players.append([f.prettify().splitlines() for f in FIND])

# titolari voto
for team, titolari in zip(output_g['T'].keys(), players[0::4]): 
    for t in titolari: 
        output_g['T'][team]['titolari']['voto'].append(t[2].strip())

# panchina voto
for team, titolari in zip(output_g['T'].keys(), players[1::4]): 
    for t in titolari: 
        output_g['T'][team]['panchina']['voto'].append(t[2].strip())
        

# VOTO TOTALE
players = []
for num, t in enumerate(temp['tables']):
    FIND = list(iter(BeautifulSoup(t,'lxml').find_all("td", {"data-key": "total"})))
    players.append([f.prettify().splitlines() for f in FIND])

# titolari voto
for team, titolari in zip(output_g['T'].keys(), players[0::4]): 
    for t in titolari: 
        output_g['T'][team]['titolari']['totale'].append(t[2].strip())

# panchina voto
for team, titolari in zip(output_g['T'].keys(), players[1::4]): 
    for t in titolari: 
        output_g['T'][team]['panchina']['totale'].append(t[2].strip())


# MANTRA
players = []
for num, t in enumerate(temp['tables']):
    FIND = list(iter(BeautifulSoup(t,'lxml').find_all("td", {"data-key": "mantra-pos"})))
    players.append([f.prettify().splitlines() for f in FIND])

# titolari voto
for team, titolari in zip(output_g['T'].keys(), players[0::4]): 
    for t in titolari: 
        output_g['T'][team]['titolari']['mantra'].append(t[2].strip())

# panchina voto
for team, titolari in zip(output_g['T'].keys(), players[1::4]): 
    for t in titolari: 
        output_g['T'][team]['panchina']['mantra'].append(t[2].strip())
        
        

#convert panchinari e titolari to df
for team in output_g['T'].keys(): 
    output_g['T'][team]['titolari'] = pd.DataFrame.from_dict(output_g['T'][team]['titolari'])
    output_g['T'][team]['panchina'] = pd.DataFrame.from_dict(output_g['T'][team]['panchina'])



# ALTRI PUNTI
mod = []
val = []
for num, t in enumerate(temp['tables'][2::4]):
    FIND_n = list(iter(BeautifulSoup(t,'lxml').find_all("td", {"data-key": "name"})))
    FIND_v = list(iter(BeautifulSoup(t,'lxml').find_all("td", {"data-key": "value"})))
    mod.append([f.prettify().splitlines()[2].strip() for f in FIND_n])
    val.append([f.prettify().splitlines()[2].strip() for f in FIND_v])


for t, m, v in zip(output_g['T'].keys(), mod, val):
    for i , j in zip(m,v):
        if j == '---':
            continue
        output_g['T'][t]['bonus'][i] = j

