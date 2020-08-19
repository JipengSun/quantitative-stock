import tushare as ts
import talib as ta
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

def buy_opreation(data,idx,share,cash,br):
    share += cash / data.loc[idx, 'close']
    cash = 0
    data.loc[idx,'operation'] = 1
    br.append(idx)
    return share, cash


def sell_opreation(data,idx,share,cash,sr):
    cash += share * data.loc[idx, 'close']
    share = 0
    data.loc[idx, 'operation'] = 0
    sr.append(idx)
    return share, cash


def figure_plot(data,current,win_size,sr,br):
    '''
    fig = plt.figure()
    ax = plt.axes()
    #bar1 = ax.bar(x=[], height=[], bottom=8000)
    line1 = ax.plot([])
    line2 = ax.plot([])
    #ticks = ax.xticks([],[],rotation='vertical')

    line1.set_data(data_slice['close'])
    line2.set_data(data_slice['value'])
    '''
    data_slice = data.iloc[max(0, current - win_size):(current + 1), :]
    #plt.clf()
    #plt.figure(figsize=(80, 40))
    
    plt.bar(x=data_slice.index, height=data_slice['hist'], bottom=8000)
    plt.plot(data_slice['close'])
    plt.plot(data_slice['value'])
    # plt.grid(color="k", linestyle=":")
    plt.xticks(data_slice.index, data_slice['date'], rotation='vertical')
    #plt.savefig("test.png", dpi=120)
    if len(sr) != 0:
        for xsr in sr:
            if xsr >= current-win_size:
                plt.axvline(x=xsr, c='green')
    if len(br) != 0:
        for xbr in br:
            if xbr >= current-win_size:
                plt.axvline(x=xbr, c='red')

    plt.draw()
    plt.show()
    #plt.close('all')


def summary_plot(data,current):
    data_slice = data.iloc[0:(current + 1), :]
    #plt.figure(figsize=(120, 40))
    plt.bar(data_slice.index,
            height=data_slice['hist'], bottom=8000)
    plt.plot(data_slice['close'])
    plt.plot(data_slice['value'])
    # plt.grid(color="k", linestyle=":")
    plt.xticks(data_slice.index,
               data_slice['date'], rotation='vertical')
    # plt.savefig("test.png", dpi=120)
    if len(sr) != 0:
        for xsr in sr:
            if xsr >= 0:
                plt.axvline(x=xsr, c='green')
    if len(br) != 0:
        for xbr in br:
            if xbr >= 0:
                plt.axvline(x=xbr, c='red')
    plt.savefig('/Users/Jipeng/PycharmProjects/quantitative_stock/human_decision.png')
    plt.show()


if __name__ == '__main__':
    df = pd.read_csv('/Users/Jipeng/PycharmProjects/quantitative_stock/game_data.csv')
    df['operation'] = [2 for i in range(len(df))]
    share = 0
    cash = 10000
    df['value'] = [cash for i in range(len(df))]
    win_size = 30
    br = []
    sr = []
    current = 0
    for idx in range(242,len(df)):
        print('Press 1 for buy, 0 for sell, 6 for end, other numbers for hold')
        decision = int(sys.stdin.readline().strip())
        if decision == 1:
            share, cash = buy_opreation(df,idx,share,cash,br)
        elif decision == 0:
            share, cash = sell_opreation(df,idx,share,cash,sr)
        elif decision == 6:
            current = idx
            break
        current = idx
        value = share * df.loc[idx, 'close'] + cash
        df.loc[idx,'value'] = value
        print('After transaction. Your current cash is %f, share is %f, value is %f'%(cash,share,value))
        figure_plot(df,current,win_size,sr,br)
    summary_plot(df,current)