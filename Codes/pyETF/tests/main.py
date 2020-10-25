import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web
# style.use('ggplot')

# Define the instruments to download
ishares = ['CSNDX.MI'] # ishares nasdaq 100 ETF UCITS USD ACC
tickers = ['^NDX'] # nasdaq

# sample data
start_date = '1990-01-01'
end_date = '2020-10-10'
# download df
# df = web.get_data_yahoo(tickers, start=start_date, end=end_date, interval='m' )
df = web.get_data_yahoo(tickers, start=start_date, end=end_date)
# adjust df
df.columns = df.columns.droplevel('Symbols')
df = df.drop(['Close', 'High', 'Low', 'Open'], 1)
df_ohlc = df['Adj Close'].resample('1M').ohlc()


# compute % gain
perc = [(df['value'][i+1]/df['value'][i]-1)*100 for i in range(df['value'].shape[0]-1)]
perc.insert(0,0)
df['%'] = perc


ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1, )
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)

ax1.plot(df.index, df['value'])
ax2.bar(df.index, df['%'])

plt.show()
