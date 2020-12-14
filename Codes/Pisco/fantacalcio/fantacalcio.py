import requests
import pandas as pd
from bs4 import BeautifulSoup
from collections import OrderedDict

def getFanta_20(url, stagione, giornata):

    page = requests.get(url)
    
    soup = BeautifulSoup(page.content, 'lxml')
    tab = soup.prettify()
    
    if len(tab) <1:
        return print('la squadra non ha giocato?')
      
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
            row = [td.text.strip().replace(',','.').splitlines()[0] for td in tr.select('td') if td.text.strip()]
            if row:
                voti[num] = row[1:] 
            
    
    col = ['v_F', 'fv_F', 'v_S', 'fv_S', 'v_I', 'fv_I',
            'Gf', 'Gv', 'Gs', 'Rp', 'Rs', 'Au', 'As']
    dfVoti = pd.DataFrame.from_dict(voti, orient='index', columns=col)
    dfNomi = pd.DataFrame.from_dict(output, orient='index' ).T
    
    final = pd.concat([dfNomi, dfVoti], axis=1)
    final.replace('-', 0, inplace=True)
    final = final.apply(pd.to_numeric, errors='ignore')
    final.fillna(0,inplace=True)
    final = final.astype({'v_F':'float', 'fv_F':'float',
                          'v_I':'float', 'fv_I':'float',
                          'Gf':'int32', 'Gv':'int32', 'Gs':'int32', 'Rp':'int32',
                          'Rs':'int32', 'Au':'int32', 'As':'int32'})
    
    return final

def scaricaStorico_20():
    data_history = []
    team_2020_21 = [1,24,2,21,22,6,8,9,10,11,12,13,107,15,16,17,129,18,19,20] # stagione 2020-21
    giornate = 11
    stagione = '2020-21'
    for g in range(giornate):
        g+=1
        print(f'parsing giornata {g}/{giornate}')
        for t in team_2020_21:
            print(t)
            url = f'https://www.fantacalcio.it/Servizi/Voti.ashx?s={stagione}&g={g}&tv=1607403898000&t={t}'
            # print(url)
            data_history.append(getFanta_20(url, stagione, g))

            
    return data_history
              
def getFanta_15_16(url, stagione, giornata):

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
    team = BeautifulSoup(header, 'lxml').findAll("img")
    output['T']  =  [str(team[0]).split('/')[-2].split(' ')[0][:-5].upper() for i in range(len(player))]
    
    
    # ID GIOCATORE & NOME 
    output['ID'] = []
    output['N'] = []
    for num, p in enumerate(player):
            role = BeautifulSoup(p, 'lxml').findAll("a",href=True)
            if bool(role): # if role is not empty
                output['N'].append(str(role[0]).splitlines()[0].split('/')[5].upper())
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
        role = BeautifulSoup(p, 'lxml').findAll("td", {"class": 'aleft'})
        if bool(role): # if role is not empty
            temp = str(role[0]).splitlines()
            for t in temp:
                if 'Entrato' in t:
                    output['E'][num] = 1
        else:
           role = BeautifulSoup(p, 'lxml').findAll("span", {"class": 'aleft'}) 
           if bool(role): # if role is not empty
            temp = str(role[0]).splitlines()
            for t in temp:
                if 'Entrato' in t:
                    output['E'][num] = 1
            
    # USCITO
    output['U'] = [0 for i in range(len(player))]
    for num, p in enumerate(player):
        role = BeautifulSoup(p, 'lxml').findAll("td", {"class": 'aleft'})
        if bool(role): # if role is not empty
            temp = str(role[0]).splitlines()
            for t in temp:
                if 'Uscito' in t:
                    output['U'][num] = 1
        else:
           role = BeautifulSoup(p, 'lxml').findAll("span", {"class": 'aleft'}) 
           if bool(role): # if role is not empty
            temp = str(role[0]).splitlines()
            for t in temp:
                if 'Uscito' in t:
                    output['U'][num] = 1
                
                    
    # GOL_VITTORIA
    output['V'] = [0 for i in range(len(player))]
    for num, p in enumerate(player):
        role = BeautifulSoup(p, 'lxml').findAll("td", {"class": 'aleft'})
        if bool(role): # if role is not empty
            temp = str(role[0]).splitlines()
            for t in temp:
                if 'Gol' in t:
                    output['V'][num] = 1
        else:
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
            # row = [td.text.strip().replace(',','.') for td in tr.select('td') if td.text.strip()]
            row = [td.text.strip() for td in tr.select('td') ]
            # print(row)
            rows = row[2:]
            if len(row[2:]) < 11:
                rows = row[1:]
            for n, r in enumerate(rows):
                if len(r)>3:
                    rows[n] = r[:4].strip()
                # print(row)
            if rows:
                voti[num] = rows
                
                
            
    
    col = ['v_F', 'fv_F', 'v_I', 'fv_I',
           'Gf', 'Gv', 'Gs', 'Rp', 'Rs', 'Au', 'As']
    dfVoti = pd.DataFrame.from_dict(voti, orient='index', columns=col)
    dfNomi = pd.DataFrame.from_dict(output, orient='index' ).T
    
    # add statistical votes for consistency even if not present for 2015-2016
    v_S = [None for i in range(dfVoti.shape[0])]
    fv_S = [None for i in range(dfVoti.shape[0])]
    dfVoti.insert(2, 'v_S', v_S)
    dfVoti.insert(3, 'fv_S', fv_S)
    
    final = pd.concat([dfNomi, dfVoti], axis=1)
    final.replace('-', 0, inplace=True)
    final.fillna(0,inplace=True)
    if final['v_F'].dtypes == object:
        final['v_F'] = final['v_F'].str.replace(',','.').apply(pd.to_numeric, errors='ignore').round(2)
    if final['fv_F'].dtypes == object:
        final['fv_F'] = final['fv_F'].str.replace(',','.').apply(pd.to_numeric, errors='ignore').round(2)
    if final['v_I'].dtypes == object:
        final['v_I'] = final['v_I'].str.replace(',','.').apply(pd.to_numeric, errors='ignore').round(2)
    if final['fv_I'].dtypes == object:
        final['fv_I'] = final['fv_I'].str.replace(',','.').apply(pd.to_numeric, errors='ignore').round(2)
    final = final.astype({'v_F':'float', 'fv_F':'float',
                          'v_I':'float', 'fv_I':'float',
                          'Gf':'int32', 'Gv':'int32', 'Gs':'int32', 'Rp':'int32',
                          'Rs':'int32', 'Au':'int32', 'As':'int32'})
    
    return final

def scaricaStorico_15_16():
    team_2015_16 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    # team_2016_17 = [1,2,21,4,22,5,6,8,9,10,11,12,13,14,23,15,16,17,18,19]

    # teams = {'2015-16':team_2015_16, '2016-17':team_2016_17}
    teams= {'2015-16':team_2015_16}
    
    data_history = []
    for k, team_list in teams.items():
        giornate = 38
        stagione = k
        print(f'parsing season {k}')
        for g in range(giornate):
            g+=1
            print(f'parsing giornata {g}/{giornate}')
            for t in team_list:
                # print(t)
                url = f'https://www.fantacalcio.it/Servizi/Voti.ashx?s={k}&g={g}&tv=-5&t={t}'
                # print(url)
                data_history.append(getFanta_15_16(url, stagione, g))
    return data_history
        
def getFanta_17_19(url, stagione, giornata):

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
    team = BeautifulSoup(header, 'lxml').findAll("span", {"class": 'txtbig'})
    output['T']  =  [str(team[0]).splitlines()[1].lstrip() for i in range(len(player))]
    
    
    # ID GIOCATORE & NOME SQUADRA
    output['ID'] = []
    output['N'] = []
    for num, p in enumerate(player):
            role = BeautifulSoup(p, 'lxml').findAll("a",href=True)
            if bool(role): # if role is not empty
                output['N'].append(str(role[0]).splitlines()[0].split('/')[5].upper())
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
        role = BeautifulSoup(p, 'lxml').findAll("td", {"class": 'aleft'})
        if bool(role): # if role is not empty
            temp = str(role[0]).splitlines()
            for t in temp:
                if 'Entrato' in t:
                    output['E'][num] = 1
                
            
    # USCITO
    output['U'] = [0 for i in range(len(player))]
    for num, p in enumerate(player):
        role = BeautifulSoup(p, 'lxml').findAll("td", {"class": 'aleft'})
        if bool(role): # if role is not empty
            temp = str(role[0]).splitlines()
            for t in temp:
                if 'Uscito' in t:
                    output['U'][num] = 1
                
                    
    # GOL_VITTORIA
    output['V'] = [0 for i in range(len(player))]
    for num, p in enumerate(player):
        role = BeautifulSoup(p, 'lxml').findAll("td", {"class": 'aleft'})
        if bool(role): # if role is not empty
            temp = str(role[0]).splitlines()
            for t in temp:
                if 'Gol' in t:
                    output['V'][num] = 1
    
    # VOTI
    voti = OrderedDict()
    for num, p in enumerate(player):
        for tr in BeautifulSoup(p, 'lxml').select('tr'):
            # row = [td.text.strip().replace(',','.') for td in tr.select('td') if td.text.strip()]
            row = [td.text.strip() for td in tr.select('td') ]
            row = row[2:]
            for n, r in enumerate(row):
                if len(r)>3:
                    row[n] = r[:4].strip()
            # print(row)
            if row:
                voti[num] = row
            
    
    col = ['v_F', 'fv_F', 'v_S', 'fv_S', 'v_I', 'fv_I',
           'Gf', 'Gv', 'Gs', 'Rp', 'Rs', 'Au', 'As']
    dfVoti = pd.DataFrame.from_dict(voti, orient='index', columns=col)
    dfNomi = pd.DataFrame.from_dict(output, orient='index' ).T
    
    final = pd.concat([dfNomi, dfVoti], axis=1)
    final.replace('-', 0, inplace=True)
    final.fillna(0,inplace=True)
    if final['v_F'].dtypes == object:
        final['v_F'] = final['v_F'].str.replace(',','.').apply(pd.to_numeric, errors='ignore').round(2)
    if final['fv_F'].dtypes == object:
        final['fv_F'] = final['fv_F'].str.replace(',','.').apply(pd.to_numeric, errors='ignore').round(2)
    if final['v_S'].dtypes == object:
        final['v_S'] = final['v_I'].str.replace(',','.').apply(pd.to_numeric, errors='ignore').round(2)
    if final['fv_S'].dtypes == object:
        final['fv_S'] = final['fv_I'].str.replace(',','.').apply(pd.to_numeric, errors='ignore').round(2)
    if final['v_I'].dtypes == object:
        final['v_I'] = final['v_I'].str.replace(',','.').apply(pd.to_numeric, errors='ignore').round(2)
    if final['fv_I'].dtypes == object:
        final['fv_I'] = final['fv_I'].str.replace(',','.').apply(pd.to_numeric, errors='ignore').round(2)
    final = final.astype({'v_F':'float', 'fv_F':'float',
                          'v_I':'float', 'fv_I':'float',
                          'Gf':'int32', 'Gv':'int32', 'Gs':'int32', 'Rp':'int32',
                          'Rs':'int32', 'Au':'int32', 'As':'int32'})

    return final

def scaricaStorico_17_19():
    data_history = []
    team_2017_18 = [1,24,2,21,4,22,6,8,9,10,11,12,13,15,16,17,25,18,19,20]
    team_2018_19 = [1,2,21,4,5,6,7,8,9,10,11,12,13,107,15,16,17,25,18,19]
    team_2019_20 = [1,2,118,21,6,8,9,10,11,119,12,13,107,15,16,17,25,18,19,20]
    
    teams = {'2017-18':team_2017_18, '2018-19':team_2018_19,
              '2019-20':team_2019_20}
    
    data_history = []
    for k, team_list in teams.items():
        giornate = 38
        stagione = k
        print(f'parsing season {k}')
        for g in range(giornate):
            g += 1
            print(f'parsing giornata {g}/{giornate}')
            for t in team_list:
                # print(t)
                url = f'https://www.fantacalcio.it/Servizi/Voti.ashx?s={k}&g={g}&tv=-5&t={t}'
                # print(url)
                data_history.append(getFanta_17_19(url, stagione, g))
    return data_history



# df_15_16 = scaricaStorico_15_16()
# df_17_19 = scaricaStorico_17_19()
# df_20 = scaricaStorico_20()



# import pickle

# df1 = pd.read_pickle('df_2015.p')
# df2 = pd.read_pickle('df_2016.p')
# df3 = pd.read_pickle('df_2017_19.p')
# df4 = pd.read_pickle('df_2020.p')

# df = pd.concat([df1,df2,df3,df4])
# df.reset_index(drop=True, inplace=True)
# a = df.apply(pd.to_numeric, errors='ignore')
# pickle.dump(df, open('db_fantacalcio.p', 'wb'))

# # df = pd.read_pickle('df_2016.p')
# df.isnull().sum()
