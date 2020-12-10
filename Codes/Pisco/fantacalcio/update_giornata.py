import pandas as pd
import pickle

from fantacalcio import getFanta_20

def scaricaStorico_20():
    data_history = []
    team_2020_21 = [1,24,2,21,22,6,8,9,10,11,12,13,107,15,16,17,129,18,19,20] # stagione 2020-21
    giornate = 11
    stagione = '2020-21'
    for g in range(giornate, giornate+1):
        g+=1
        print(f'parsing giornata {g}/{giornate}')
        for t in team_2020_21:
            print(t)
            url = f'https://www.fantacalcio.it/Servizi/Voti.ashx?s={stagione}&g={g}&tv=1607403898000&t={t}'
            # print(url)
            data_history.append(getFanta_20(url, stagione, g))

            
    return data_history

df_add = scaricaStorico_20()

df = pd.read_pickle('db_fantacalcio.p')
df = pd.concat([df,df_add])
df.reset_index(drop=True, inplace=True)
