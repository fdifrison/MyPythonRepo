import pandas as pd

df = pd.read_excel('fifa2020.xlsx')
df.reset_index(drop=True, inplace=True)
df.drop_duplicates(inplace=True)

import seaborn as sns
sns.set(style="white")
sns.set(font_scale=0.7)
import matplotlib.pyplot as plt

from math import pi
import numpy as np




g1 = df[df['NAME'].str.contains('Lionel Messi')]
g2 = df[df['NAME'].str.contains('C. Ronaldo')]

def fifaCompare(g1,g2):
    
    id1 = g1['ID'].values[0]
    naz1 = g1['NATIONALITY'].values[0].replace(' ', '')
    logo1 = g1['TEAM'].values[0].replace(' ', '')
    
    
    id2 = g2['ID'].values[0]
    naz2 = g2['NATIONALITY'].values[0].replace(' ', '')
    logo2 = g2['TEAM'].values[0].replace(' ', '')
    
    name = g1['NAME'].values[0].split()[:2]
    name1 = ' '.join(name)
    
    name = g2['NAME'].values[0].split()[:2]
    name2 = ' '.join(name)
    
    
    
    
    fig = plt.figure(figsize=(5,7), constrained_layout=True)
    # fig = plt.figure(facecolor='green')
    gs = fig.add_gridspec(10, 6)
    
    # giocatore 1
    player1 = fig.add_subplot(gs[0:2, 0:2])
    a = plt.imread(f'https://github.com/fdifrison/MyPythonRepo/blob/master/Codes/FIFA2020/my_scraper/pictures/{id1}.png?raw=true')
    player1.imshow(a)
    player1.axes.get_xaxis().set_visible(False)
    player1.axes.get_yaxis().set_visible(False)
    player1.set_title(name1)
    # logo nazione
    logoNaz1 = fig.add_subplot(gs[0, 2])
    a = plt.imread(f'https://github.com/fdifrison/MyPythonRepo/blob/master/Codes/FIFA2020/my_scraper/pictures/{naz1}.png?raw=true')
    logoNaz1.imshow(a)
    logoNaz1 .axes.get_xaxis().set_visible(False)
    logoNaz1 .axes.get_yaxis().set_visible(False)
    # logo team
    logoTeam1 = fig.add_subplot(gs[1, 2])
    a = plt.imread(f'https://github.com/fdifrison/MyPythonRepo/blob/master/Codes/FIFA2020/my_scraper/pictures/{logo1}.png?raw=true')
    logoTeam1.imshow(a)
    logoTeam1 .axes.get_xaxis().set_visible(False)
    logoTeam1 .axes.get_yaxis().set_visible(False)
    # giocatore 2
    player2 = fig.add_subplot(gs[0:2, 3:5])
    a = plt.imread(f'https://github.com/fdifrison/MyPythonRepo/blob/master/Codes/FIFA2020/my_scraper/pictures/{id2}.png?raw=true')
    player2.imshow(a)
    player2.axes.get_xaxis().set_visible(False)
    player2.axes.get_yaxis().set_visible(False)
    player2.set_title(name2)
    # logo nazione
    logoNaz2 = fig.add_subplot(gs[0, 5])
    a = plt.imread(f'https://github.com/fdifrison/MyPythonRepo/blob/master/Codes/FIFA2020/my_scraper/pictures/{naz2}.png?raw=true')
    logoNaz2.imshow(a)
    logoNaz2.axes.get_xaxis().set_visible(False)
    logoNaz2.axes.get_yaxis().set_visible(False)
    # logo team
    logoTeam2 = fig.add_subplot(gs[1, 5])
    a = plt.imread(f'https://github.com/fdifrison/MyPythonRepo/blob/master/Codes/FIFA2020/my_scraper/pictures/{logo2}.png?raw=true')
    logoTeam2.imshow(a)
    logoTeam2 .axes.get_xaxis().set_visible(False)
    logoTeam2 .axes.get_yaxis().set_visible(False)

    #statistiche
    statg1 = fig.add_subplot(gs[2:5, 0:3])
    # statg1.tick_params(axis="y",direction="in", pad=-22)
    # statg1.tick_params(axis="x",direction="in", pad=-15)
    bar = g1[['ATTACKING', 'SKILL', 'MOVEMENT', 'POWER',  'MENTALITY', 'DEFENDING', 'GOALKEEPING']]
    bar.columns = ['ATT', 'SKILL', 'MOV', 'POW', 'MENT', 'DEF', 'GK']
    sns.barplot(data=bar,orient='h', ax=statg1, edgecolor='k', label='small')
    statg1.xaxis.grid() # vertical lines
    
    # statg1.axes.get_xaxis().set_visible(False)
    # statg1.axes.get_yaxis().set_visible(False)
    
    
    statg2 = fig.add_subplot(gs[2:5, 3:6], sharex=statg1)
    # statg2.tick_params(axis="y",direction="in", pad=-22)
    # statg2.tick_params(axis="x",direction="in", pad=-15)
    bar = g2[['ATTACKING', 'SKILL', 'MOVEMENT', 'POWER',  'MENTALITY', 'DEFENDING', 'GOALKEEPING']]
    sns.barplot(data=bar, orient='h', ax=statg2, edgecolor='k', label='small')
    statg2.xaxis.grid() # vertical lines
    
    # statg2.axes.get_xaxis().set_visible(False)
    statg2.axes.get_yaxis().set_visible(False)
    
    
    #confronto
    g1g2 = fig.add_subplot(gs[5:, :], polar=True)
    
    
    g11 = g1.drop(columns=['ATTACKING', 'SKILL', 'MOVEMENT', 'POWER',  'MENTALITY', 'DEFENDING', 'GOALKEEPING'])
    g22 = g2.drop(columns=['ATTACKING', 'SKILL', 'MOVEMENT', 'POWER',  'MENTALITY', 'DEFENDING', 'GOALKEEPING'])
    
    categories =['CR', 'FI', 'HA', 'SP', 'VO', 'DR', 'CU', 'FKA', 'LP',
                 'BC', 'AC', 'SS', 'AGI', 'RE', 'BA', 'SP', 'JU', 'STA',
                 'STR', 'LS', 'AGG', 'INT', 'POS', 'VI', 'PE', 'CO',
                 'MA', 'STT', 'SLT'] # from corssing to sliding_tackle
    
    N = len(categories)
     
    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
     
     
    # If you want the first axis to be on top:
    g1g2.set_theta_offset(pi / 2)
    g1g2.set_theta_direction(-1)
    plt.yticks([10,20,30,40,50,60,70,80,90,100],
               ['10','20','30','40','50','60','70','80','90','100'], color="k", size=7)
    plt.ylim(0,100)

    plt.xticks(angles[:-1], categories, fontsize=8)
    g1g2.tick_params(pad=2)
    g1g2.tick_params(axis="y",direction="in", pad=-22)
    
     
    # Draw one axe per variable + add labels labels yet
    values=g11.iloc[0, 22:51].values.flatten().tolist()
    values += values[:1]
    g1g2.plot(angles, values, linewidth=1.2, linestyle='solid', label=name1)
    g1g2.fill(angles, values, 'b', alpha=0.4)
    
     
    # Ind2
    values=g22.iloc[0, 22:51].values.flatten().tolist()
    values += values[:1]
    g1g2.plot(angles, values, linewidth=1.2, linestyle='solid', label=name2)
    g1g2.fill(angles, values, 'r', alpha=0.4)
    
    
    plt.legend(loc='upper right', bbox_to_anchor=(0, 0))


     


fifaCompare(g1,g2)
# savefig('figname.png', facecolor=fig.get_facecolor(), transparent=True)



# # base_url for pictures at github repository
# player_id = 'xxxx' # player face
# nat = 'xxxx' # nation flag
# team = 'xxxx'# team logo
# url_p = f'https://github.com/fdifrison/MyPythonRepo/blob/master/Codes/FIFA2020/my_scraper/pictures/{player_id}.png?raw=true'
# url_n = f'https://github.com/fdifrison/MyPythonRepo/blob/master/Codes/FIFA2020/my_scraper/pictures/{nat}.png?raw=true'
# url_t = f'https://github.com/fdifrison/MyPythonRepo/blob/master/Codes/FIFA2020/my_scraper/pictures/{team}.png?raw=true'
