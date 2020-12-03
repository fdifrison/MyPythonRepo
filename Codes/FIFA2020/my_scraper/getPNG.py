import requests
import pandas as pd
import os

cwd = os.getcwd()
try:
    os.mkdir('.\pictures')
except:
    print('picture dir is already here')
    
print('\nloading data')
df = pd.read_excel('fifa2020.xlsx')
flag = df.drop_duplicates(subset='FLAG', keep="last")
team = df.drop_duplicates(subset='TEAM', keep="last")
print('\ndone\n')

passed = []
#loop over PICTURE, FLAG, TEAM_LOGO
os.chdir(cwd + '\pictures')
for row in range(flag.shape[0]):
    print(f'{row}/{flag.shape[0]}')
    NAZ = df.loc[row, 'NATIONALITY']
    FLAG = df.loc[row, 'FLAG']
    try:
        f = open(f'{NAZ}.jpg','wb')
        f.write(requests.get(FLAG).content)
        f.close()
    except:
        passed.append(NAZ)

print()       
print(passed)   
print()   

for row in range(team.shape[0]):
    print(f'{row}/{team.shape[0]}')
    TNAME = df.loc[row, 'TEAM']
    LOGO = df.loc[row, 'TEAM_LOGO']
    try:
        f = open(f'{TNAME}.jpg','wb')
        f.write(requests.get(LOGO).content)
        f.close()
    except:
        passed.append(TNAME)
        
print()       
print(passed)   
print()   

for row in range(df.shape[0]):
    print(f'{row}/{df.shape[0]}')
    ID = df.loc[row, 'ID']
    FACE = df.loc[row, 'PICTURE']
    try:
        f = open(f'{ID}.jpg','wb')
        f.write(requests.get(FACE).content)
        f.close()
    except:
        passed.append(ID)
print()       
print(passed)   
print()   
