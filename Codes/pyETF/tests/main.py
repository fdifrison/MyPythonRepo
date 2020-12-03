import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
# style.use('ggplot')

def simulateETF(start, stop, base_amount, drug, drug_when):
    # Define the instruments to download
    # ishares = ['CSNDX.MI'] # ishares nasdaq 100 ETF UCITS USD ACC
    tickers = ['^IXIC'] # nasdaq
    
    # sample data
    start_date = start
    end_date = stop
    # download df
    # df = web.get_data_yahoo(tickers, start=start_date, end=end_date, interval='m' )
    df = web.get_data_yahoo(tickers, start=start_date, end=end_date, interval='d')
    # adjust df
    df.columns = df.columns.droplevel('Symbols')
    df = df.drop(['Close', 'High', 'Low', 'Open'], 1)
    df.columns = ['value', '%']
    # compute % gain
    perc = [(df['value'][i+1]-df['value'][i])/df['value'][i]*100 for i in range(df['value'].shape[0]-1)]
    perc.insert(0,0)
    df['%'] = perc
    
    year = df['value'].groupby(df.index.to_period('Y')).agg('mean')
    Qreturn = df['%'].groupby(df.index.to_period('Q')).agg('sum')

    # quarterly return table
    QRtab = pd.DataFrame(columns=['T1', 'T2', 'T3', 'T4'], index=year.index)
    
    count = 0
    for row in range(QRtab.shape[0]):
        for col in range(4):
            QRtab.iloc[row, col] = Qreturn[count]
            count +=1
    
    # invested money
    IMtab = pd.DataFrame(columns=['T1', 'T2', 'T3', 'T4'], index=year.index)
    
    for row in range(IMtab.shape[0]):
        for col in range(4):
            if row!= 0 and col == 0:
                T = QRtab.iloc[row-1,col+3]
                if  T <= drug_when:
                    IMtab.iloc[row,col] = base_amount * drug
                else:
                    IMtab.iloc[row,col] = base_amount
            elif col != 0:
                T = QRtab.iloc[row,col-1]
                if  T <= drug_when:
                    IMtab.iloc[row,col] = base_amount * drug
                else:
                    IMtab.iloc[row,col] = base_amount
            elif row== 0 and col == 0:            
                IMtab.iloc[0,0] = base_amount
                
    # capital gain tab
    CGtab = pd.DataFrame(columns=['T1', 'T2', 'T3', 'T4'], index=year.index)
    # add first investemt
    CGtab.iloc[0,0] = IMtab.iloc[0,0]
    for row in range(CGtab.shape[0]):
        for col in range(4):
            if row!= 0 and col == 0:
                CGtab.iloc[row,col] = CGtab.iloc[row-1,col+3]*(QRtab.iloc[row-1, col+3]/100 +1) + IMtab.iloc[row, col]
            elif col != 0:
                CGtab.iloc[row,col] = CGtab.iloc[row,col-1]*(QRtab.iloc[row, col-1]/100 +1) + IMtab.iloc[row, col]
            elif row== 0 and col == 0:            
                CGtab.iloc[0,0] = IMtab.iloc[0,0]
    
    totalInvest = IMtab.values.sum()
    totalGain = CGtab.iloc[-1,-1]
    capGain = totalGain-totalInvest
    performance = capGain/totalInvest
    # print(totalInvest)
    return performance


# 10 years
start = ['1990-01-01','1995-01-01','2000-01-01','2005-01-01','2010-01-01']
end = ['2000-12-31','2005-12-31','2010-12-31','2015-12-31','2020-12-31']
drug_when = [i for i in range(-15,15)]
capGain = [[simulateETF(j, k, 900, 1.5, i) for i in drug_when]for j, k in zip(start, end)]
# capGain2 = [simulateETF(900, 2, i) for i in drug_when]

fig, ax = plt.subplots()

for num, cap in enumerate(capGain):
    cap = [i/max(cap) for i in cap]
    ax.plot(drug_when, cap, alpha=0.6, label=start[num][:5]+end[num][:4])
    ax.plot(drug_when, cap, c='k', lw=3, alpha=0.6, zorder=0)

ax.set_xlabel('if % of gain in the previous Q, then drug')
ax.set_ylabel('Normalized performance')
ax.legend()
ax.grid(which='both', alpha=0.5, ls='--', c ='k')
plt.show()



# 10 years
start = ['1993-01-01','1998-01-01','2003-01-01','2008-01-01']
end = ['2003-12-31','2008-12-31','2013-12-31','2018-12-31']
drug_when = [i for i in range(-15,15)]
capGain = [[simulateETF(j, k, 900, 1.5, i) for i in drug_when]for j, k in zip(start, end)]
# capGain2 = [simulateETF(900, 2, i) for i in drug_when]

fig, ax = plt.subplots()

for num, cap in enumerate(capGain):
    cap = [i/max(cap) for i in cap]
    ax.scatter(drug_when, cap, alpha=0.6, label=start[num][:5]+end[num][:4])
    # ax.plot(drug_when, cap, c='k', lw=3, alpha=0.6, zorder=0)

ax.set_xlabel('if % of gain in the previous Q, then drug')
ax.set_ylabel('Normalized performance')
ax.legend()
ax.grid(which='both', alpha=0.5, ls='--', c ='k')
plt.show()



# 15 years
start = ['1990-01-01','1995-01-01','2000-01-01','2005-01-01']
end = ['2005-12-31','2010-12-31','2015-12-31','2020-12-31']
drug_when = [i for i in range(-15,15)]
capGain = [[simulateETF(j, k, 900, 1.5, i) for i in drug_when]for j, k in zip(start, end)]
# capGain2 = [simulateETF(900, 2, i) for i in drug_when]

fig, ax = plt.subplots()

for num, cap in enumerate(capGain):
    cap = [i/max(cap) for i in cap]
    ax.scatter(drug_when, cap, alpha=0.6, label=start[num][:5]+end[num][:4])
    ax.plot(drug_when, cap, c='k', lw=3, alpha=0.6, zorder=0)

ax.set_xlabel('if % of gain in the previous Q, then drug')
ax.set_ylabel('Normalized performance')
ax.legend()
ax.grid(which='both', alpha=0.5, ls='--', c ='k')
plt.show()

