import requests
import pandas as pd
from bs4 import BeautifulSoup
from collections import OrderedDict

def getFantacalcioVotes(url, stagione, giornata):

    page = requests.get(url)
    
    soup = BeautifulSoup(page.content, 'lxml')
    tab = soup.prettify()
      
    FIND = list(iter(BeautifulSoup(tab, 'lxml').find_all(['tbody', 'thead']))) 
    header = FIND[0].prettify()
    body = FIND[1].prettify()
    
    FIND = list(iter(BeautifulSoup(body, 'lxml').find_all(['tr'])))
    player = [f.prettify() for f in FIND]
    
    
    output = OrderedDict()
    
    
    # STAGIONE
    output['S'] = [stagione for i in range(len(player))]
    
    # GIORNATA
    output['G'] = [giornata for i in range(len(player))]
    
    # TEAM
    team = BeautifulSoup(header, 'lxml').findAll("th", {"class": 'team-header'})
    output['T']  =  [str(team[0]).splitlines()[4].lstrip() for i in range(len(player))]
    
    
    # ID GIOCATORE & NOME SQUADRA
    class_id = "player-name"
    output['ID'] = []
    output['N'] = []
    for num, p in enumerate(player):
            role = BeautifulSoup(p, 'lxml').findAll("a", {"class": class_id})
            if bool(role): # if role is not empty
                output['N'].append(str(role[0]).splitlines()[1].lstrip().upper())
                output['ID'].append(str(role[0]).splitlines()[0].split('/')[6])
    
    
    
    
    # RUOLO
    class_role = ["role label label-sm p",          #portiere
                  "role label label-sm d",          #difensore 
                  "role label label-sm c",          #centrocampista  
                  "role label label-sm a",          #attaccante
                  "role label label-sm label-grey"  #allenatore
                  ]
    
    
    output['R'] = []
    for num, p in enumerate(player):
        for c in class_role:
            role = BeautifulSoup(p, 'lxml').findAll("span", {"class": c})
            if bool(role): # if role is not empty
                output['R'].append(str(role[0]).splitlines()[1].replace(' ', ''))
                
    
    # ENTRATO
    output['E'] = [0 for i in range(len(player))]
    for num, p in enumerate(player):
        role = BeautifulSoup(p, 'lxml').findAll("span", {"class": 'aleft'})
        if bool(role): # if role is not empty
            temp = str(role[0]).splitlines()
            for t in temp:
                if 'Entrato' in t:
                    output['E'][num] = 1
                
            
    # USCITO
    output['U'] = [0 for i in range(len(player))]
    for num, p in enumerate(player):
        role = BeautifulSoup(p, 'lxml').findAll("span", {"class": 'aleft'})
        if bool(role): # if role is not empty
            temp = str(role[0]).splitlines()
            for t in temp:
                if 'Uscito' in t:
                    output['U'][num] = 1
                
                    
    # GOL_VITTORIA
    output['V'] = [0 for i in range(len(player))]
    for num, p in enumerate(player):
        role = BeautifulSoup(p, 'lxml').findAll("span", {"class": 'aleft'})
        if bool(role): # if role is not empty
            temp = str(role[0]).splitlines()
            for t in temp:
                if 'Gol' in t:
                    output['V'][num] = 1
    
    # VOTI
    voti = OrderedDict()
    for num, p in enumerate(player):
        for tr in BeautifulSoup(p, 'lxml').select('tr'):
            row = [td.text.strip().replace(',','.') for td in tr.select('td') if td.text.strip()]
            if row:
                voti[num] = row[1:] 
            
    
    col = ['v_F', 'fv_F', 'v_S', 'fv_S', 'v_I', 'fv_I',
           'Gf', 'Gv', 'Gs', 'Rp', 'Rs', 'Au', 'As']
    dfVoti = pd.DataFrame.from_dict(voti, orient='index', columns=col)
    dfNomi = pd.DataFrame.from_dict(output, orient='index' ).T
    
    final = pd.concat([dfNomi, dfVoti], axis=1)
    final.replace('-', 0, inplace=True)
    final.fillna(0,inplace=True)
    final = final.astype({'v_F':'float', 'fv_F':'float', 'v_S':'float', 'fv_S':'float',
                          'v_I':'float', 'fv_I':'float',
                          'Gf':'int32', 'Gv':'int32', 'Gs':'int32', 'Rp':'int32',
                          'Rs':'int32', 'Au':'int32', 'As':'int32'})
    
    return final

box = []
teams_tag = [1,24,2,21,22,6,8,9,10,11,12,13,107,15,16,17,129,18,18,20] # stagione 2020-21
giornate = 7
stagione = '2020-21'
for g in range(giornate):
    for t in teams_tag:
        try:
            url = f'https://www.fantacalcio.it/Servizi/Voti.ashx?s={stagione}&g={g}&tv=1606109126000&t={t}'
            box.append(getFantacalcioVotes(url, stagione, g))
        except:
            continue
        
        
final = pd.concat(box)
final.reset_index(drop=True, inplace=True)
final.drop_duplicates(inplace=True)

best_d = final[final['R'] == 'D'].groupby(['T', 'R'])['Gf'].sum()
best_c = final[final['R'] == 'C'].groupby(['T', 'R'])['Gf'].sum()
best_a = final[final['R'] == 'A'].groupby(['T', 'R'])['Gf'].sum()

import matplotlib.pyplot as plt

fig, ax = plt.subplots(1,3)
best_d.plot.bar(ax=ax[0], color='r')
best_c.plot.bar(ax=ax[1], color='g')
best_a.plot.bar(ax=ax[2], color='y')

plt.tight_layout()


cambi = final.groupby(['T'])['E'].sum()

fig, ax = plt.subplots()
cambi.plot.bar()

best_d = final[(final['R'] == 'C') & (final['T'] == 'INTER')].groupby(['N'])['v_F'].mean()

fig, ax = plt.subplots()
ax.scatter(best_d.index, best_d, s=17, c='k')
ax.scatter(best_d.index, best_d, s=12, c='b')
ax.axes.get_xaxis().set_visible(False)
ax.set_ylabel('VOTO')
ax.set_title('Migliori centrocampisti Inter')
ax.grid(c='k', ls='--', alpha=0.5)
for i in range(best_d.shape[0]):
    ax.annotate(best_d.index[i], (best_d.index[i], best_d[i]), fontsize=8)
