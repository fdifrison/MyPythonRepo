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
    NAZ = df.loc[row, 'NATIONALITY'].replace(' ', '')
    FLAG = df.loc[row, 'FLAG']
    try:
        f = open(f'{NAZ}.png','wb')
        f.write(requests.get(FLAG).content)
        f.close()
    except:
        passed.append(NAZ)


# Central.setStyleSheet("background-image: url(sfondo.png); background-attachment: fixed; color: yellow;")
# print()       
# print(passed)   
# print()   
# import re
# os.chdir(cwd + '\pictures')
# for row in range(team.shape[0]):
#     print(f'{row}/{team.shape[0]}')
#     try:
#         Tname = df.loc[row, 'TEAM'].replace(' ', '').strip()
#         Tname = ''.join(t for t in Tname if t.isalnum())
#         Tname = re.sub(r'[^A-Za-z0-9]+', '', Tname)
#     except:
#         Tname = 'NOTEAM'
#     LOGO = df.loc[row, 'TEAM_LOGO']
#     try:
#         f = open(f'{Tname}.png','wb')
#         f.write(requests.get(LOGO).content)
#         f.close()
#     except:
#         passed.append(Tname)
        
# print()       
# print(passed)   
# print()   

# for row in range(df.shape[0]):
#     print(f'{row}/{df.shape[0]}')
#     ID = df.loc[row, 'ID']
#     FACE = df.loc[row, 'PICTURE']
#     try:
#         f = open(f'{ID}.png','wb')
#         f.write(requests.get(FACE).content)
#         f.close()
#     except:
#         passed.append(ID)
# print()       
# print(passed)   
# print()   
