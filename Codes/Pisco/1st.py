import pandas as pd


# # fantacalcio.it anni [2015-2021], giornate 38, squadre 20
# dfs = []

# years = [15+i for i in range(6)]
# table = {}

# for y in years:
#     table[f'20{y}-{y+1}'] = {}
#     for g in range (1, 39):
#         table[f'20{y}-{y+1}'][f'giornata_{g}'] = []
#         for t in range(1, 21):
#             try:
#                 url = f'https://www.fantacalcio.it/Servizi/Voti.ashx?s=20{y}-{y+1}&g={g}&tv=-5&t={t}'
#                 table[f'20{y}-{y+1}'][f'giornata_{g}'].append(pd.read_html(url)[0])
#             except:
#                 url = 'https://www.fantacalcio.it/Servizi/Voti.ashx?s=20{y}-{y+1}&g={g}&tv=1606109126000&t={t}'
#                 table[f'20{y}-{y+1}'][f'giornata_{g}'].append(pd.read_html(url)[0])
#             except:
#                 continue
            
            

# # leghe fantacalcio classifica
# temp = []
# url = 'https://leghe.fantacalcio.it/mattia-calisesi-cup/'
# temp.append(pd.read_html(url)[0])



def getFantacalcioVotes(url, stagione, giornata):
    
    df = pd.read_html(url, thousands=".",decimal=',', header=[0])[0]
    df.drop(index=[0,1], inplace=True)
    df.reset_index(drop=True, inplace=True)
    rows = df.shape[0]
    team = df.columns[0]
    
    ruolo = [df.loc[i,team][0] for i in range(rows-1)]
    ruolo.append(df.loc[rows-1,team][:3]) # allenatore
    player = [df.loc[i,team][1:] for i in range(rows-1)]
    player.append(df.loc[rows-1,team][3:]) # allenatore
    
    df.insert(0, 'Stagione' ,[stagione for i in range(rows)])
    df.insert(1, 'Giornata' ,[giornata for i in range(rows)])
    df.insert(2, 'Team' ,[team for i in range(rows)])
    df.insert(3, 'Ruolo' ,ruolo)
    df.insert(4, 'Player' ,player)
    
    df.drop(columns=[team], inplace=True)
    
    col = ['Stagione', 'Giornata', 'Team', 'Ruolo', 'Player',
           'Voto1', 'FantaVoto1', 'Voto2', 'FantaVoto2', 'Voto3', 'FantaVoto3',
           'Gf', 'Gv', 'Gs', 'Rp', 'Rs', 'Au', 'As']
    
    df.columns = col
    
    return df

stagione = '2020-21'

box = []

for g in range (1, 39):
    for t in range(1, 21):
        try:
            url = f'https://www.fantacalcio.it/Servizi/Voti.ashx?s={stagione}&g={g}&tv=1606109126000&t={t}'
            box.append(getFantacalcioVotes(url, stagione, g))
        except:
            continue
        
        
final = pd.concat(box)

final.to_excel('SerieA_2020-21.xlsx', index=False)


















