from bs4 import BeautifulSoup
import requests
import pandas as pd
from collections import OrderedDict

# root url
base_url = "https://sofifa.com/players?showCol%5B0%5D=ae&showCol%5B1%5D=pi&showCol%5B2%5D=hi&showCol%5B3%5D=wi&showCol%5B4%5D=pf&showCol%5B5%5D=oa&showCol%5B6%5D=pt&showCol%5B7%5D=bo&showCol%5B8%5D=bp&showCol%5B9%5D=gu&showCol%5B10%5D=jt&showCol%5B11%5D=le&showCol%5B12%5D=vl&showCol%5B13%5D=wg&showCol%5B14%5D=rc&showCol%5B15%5D=ta&showCol%5B16%5D=cr&showCol%5B17%5D=fi&showCol%5B18%5D=he&showCol%5B19%5D=sh&showCol%5B20%5D=vo&showCol%5B21%5D=ts&showCol%5B22%5D=dr&showCol%5B23%5D=cu&showCol%5B24%5D=fr&showCol%5B25%5D=lo&showCol%5B26%5D=bl&showCol%5B27%5D=to&showCol%5B28%5D=ac&showCol%5B29%5D=sp&showCol%5B30%5D=ag&showCol%5B31%5D=re&showCol%5B32%5D=ba&showCol%5B33%5D=tp&showCol%5B34%5D=so&showCol%5B35%5D=ju&showCol%5B36%5D=st&showCol%5B37%5D=sr&showCol%5B38%5D=ln&showCol%5B39%5D=te&showCol%5B40%5D=ar&showCol%5B41%5D=in&showCol%5B42%5D=po&showCol%5B43%5D=vi&showCol%5B44%5D=pe&showCol%5B45%5D=cm&showCol%5B46%5D=td&showCol%5B47%5D=ma&showCol%5B48%5D=sa&showCol%5B49%5D=sl&showCol%5B50%5D=tg&showCol%5B51%5D=gd&showCol%5B52%5D=gh&showCol%5B53%5D=gc&showCol%5B54%5D=gp&showCol%5B55%5D=gr&showCol%5B56%5D=tt&showCol%5B57%5D=bs&showCol%5B58%5D=wk&showCol%5B59%5D=sk&showCol%5B60%5D=aw&showCol%5B61%5D=dw&showCol%5B62%5D=ir&showCol%5B63%5D=pac&showCol%5B64%5D=sho&showCol%5B65%5D=pas&showCol%5B66%5D=dri&showCol%5B67%5D=def&showCol%5B68%5D=phy&offset="

# list of df to concat later
df_final = []

for offset in range(0, 335):
    url = base_url + str(offset * 60)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    table_body = soup.find('tbody')
    
    
    for num, row in enumerate(table_body.findAll('tr')):
        
            print(f'page {offset}/334 - row {num}/{len(table_body.findAll("tr"))}')
        
            data = OrderedDict()
            td = row.findAll('td')
            data['NAME'] = td[1].find("a").get("data-tooltip")
            data['PICTURE'] = td[0].find('img').get('data-srcset').split()[2]
            data['NATIONALITY'] = td[1].find('img').get('title')
            data['FLAG'] = td[1].find('img').get('data-srcset').split()[2]
            data['AGE'] = td[2].text
            data['OVA'] = td[3].text.strip()
            data['POT'] = td[4].text.strip()
            data['TEAM'] = td[5].find('a').text
            data['TEAM_LOGO'] = td[5].find('img').get('data-srcset').split()[2]
            data['CONTRACT'] = td[5].find('div',{"class": "sub"}).text.strip().replace(' ~ ', '-')
            data['ID'] = td[6].text.strip()
            data['HEIGHT'] = td[7].text.strip()
            data['WEIGHT'] = td[8].text.strip()
            data['FOOT'] = td[9].text.strip()	
            data['BOV'] = td[10].text.strip()
            data['BP'] = td[11].text.strip()
            data['GROWTH'] = td[12].text.strip()
            data['JOINED'] = td[13].text.strip()
            data['LOAN_DATE_END'] = td[14].text.strip()
            data['VALUE'] = td[15].text.strip()
            data['WAGE'] = td[16].text.strip()
            data['RELEASE_CLAUSE'] = td[17].text.strip()
            data['ATTACKING'] = td[18].text.strip()
            data['CROSSING'] = td[19].text.strip()
            data['FINISHING'] = td[20].text.strip()
            data['HEADING_ACCURACY'] = td[21].text.strip()
            data['SHORT_PASSING'] = td[22].text.strip()
            data['VOLLEYS'] = td[23].text.strip()
            data['SKILL'] = td[24].text.strip()
            data['DRIBBLING'] = td[25].text.strip()
            data['CURVE'] = td[26].text.strip()
            data['FK_ACCURACY'] = td[27].text.strip()
            data['LONG_PASSING'] = td[28].text.strip()
            data['BALL_CONTROL'] = td[29].text.strip()
            data['MOVEMENT'] = td[30].text.strip()
            data['ACCELERATION'] = td[31].text.strip()
            data['SPRINT_SPEED'] = td[32].text.strip()
            data['AGILITY'] = td[33].text.strip()
            data['REACTIONS'] = td[34].text.strip()
            data['BALANCE'] = td[35].text.strip()
            data['POWER'] = td[36].text.strip()
            data['SHOT_POWER'] = td[37].text.strip()
            data['JUMPING'] = td[38].text.strip()
            data['STAMINA'] = td[39].text.strip()
            data['STRENGTH'] = td[40].text.strip()
            data['LONG_SHOTS'] = td[41].text.strip()
            data['MENTALITY'] = td[42].text.strip()
            data['AGGRESSION'] = td[43].text.strip()
            data['INTERCEPTIONS'] = td[44].text.strip()
            data['POSITIONING'] = td[45].text.strip()
            data['VISION'] = td[46].text.strip()
            data['PENALTIES'] = td[47].text.strip()
            data['COMPOSURE'] = td[48].text.strip()
            data['DEFENDING'] = td[49].text.strip()
            data['MARKING'] = td[50].text.strip()
            data['STANDING_TACKLE'] = td[51].text.strip()
            data['SLIDING_TACKLE'] = td[52].text.strip()
            data['GOALKEEPING'] = td[53].text.strip()
            data['GK_DIVING'] = td[54].text.strip()
            data['GK_HANDLING'] = td[55].text.strip()
            data['GK_KICKING'] = td[56].text.strip()
            data['GK_POSITIONING'] = td[57].text.strip()
            data['GK_REFLEXES'] = td[58].text.strip()
            data['TOTAL_STATS'] = td[59].text.strip()
            data['BASE_STATS'] = td[60].text.strip()
            data['W/F'] = td[61].text.strip()
            data['SM'] = td[62].text.strip()
            data['A/W']	= td[63].text.strip()
            data['D/W'] = td[64].text.strip()  	
            data['IR'] = td[65].text.strip()
            data['PAC'] = td[66].text.strip()
            data['SHO'] = td[67].text.strip()
            data['PAS'] = td[68].text.strip()
            data['DRI'] = td[69].text.strip()
            data['DEF'] = td[70].text.strip()
            data['PHY'] = td[71].text.strip()
            data['HITS'] = td[72].text.strip()
            df = pd.DataFrame.from_dict(data, orient='index').T
            try:
                df = df.apply(pd.to_numeric, errors='ignore')
                df = df.astype({'JOINED': 'datetime64'})
            except:
                pass
            df_final.append(df)
            
            
    
data = pd.concat(df_final)   
data.reset_index(drop=True, inplace=True) 
data.drop_duplicates(inplace=True)    

data.to_excel('fifa2020.xlsx', index=False)

        

