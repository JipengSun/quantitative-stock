import matplotlib
import tkinter as tk
import tkinter.messagebox
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import StringVar
matplotlib.use('TkAgg')


class Application(tk.Tk):

    def __init__(self, data, start_idx):
        super().__init__()
        self.wm_title('Decision training for 1-year stock market')
        self.data = data
        self.start = start_idx
        self.idx = start_idx
        self.share = 0
        self.cash = 10000
        self.br = []
        self.sr = []
        self.last_buy_interval = 0
        self.sell_fee_percent = 1.5
        self.fig = Figure(figsize=(16, 9), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.text = StringVar()
        self.lb = tk.Label(textvariable=self.text)
        self.win_size = 30
        self.create_widgets()
        self.figure_plot()

    def create_widgets(self):
        self.text.set(
            'Your current value is %d.\n The day interval from your last buy is %d, so the current sell charge percentage is %.2f%%' % (
            10000, 0, 1.5))
        self.lb.grid(row=0, columnspan=4)
        self.canvas.get_tk_widget().grid(row=1, columnspan=4)
        # self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # toolbar = NavigationToolbar2Tk(self.canvas, self)
        # toolbar.update()
        footframe = tk.Frame(master=self).grid(row=2, columnspan=4)
        tk.Button(master=footframe, text='Sell', width=16, height=2, command=self.sell).grid(row=2, column=0)
        tk.Button(master=footframe, text='Buy', width=16, height=2, command=self.buy).grid(row=2, column=1)
        tk.Button(master=footframe, text='Hold', width=16, height=2, command=self.hold).grid(row=2, column=2)
        tk.Button(master=footframe, text='Quit', width=16, height=2, command=self.quit).grid(row=2, column=3)
        # self.draw()  # 绘图

    def buy(self):
        if self.cash > 0 and not self.__need_quit():
            self.idx += 1
            self.last_buy_interval = 0
            self.share += self.cash / self.data.loc[self.idx, 'close'] * 0.9985
            self.cash = 0
            self.data.loc[self.idx, 'value'] = self.cash + self.share * self.data.loc[self.idx, 'close']
            self.data.loc[self.idx, 'operation'] = 1
            self.br.append(self.idx)
            self.figure_plot()
            self.label_update()
            self.__need_quit()
        else:
            tk.messagebox.showwarning('Notification','No cash to buy, please sell first!')

    def sell(self):
        if self.share > 0 and not self.__need_quit():
            self.idx += 1
            self.last_buy_interval = self.idx - self.br[-1]
            if self.last_buy_interval <= 7:
                self.cash += self.share * self.data.loc[self.idx, 'close'] * 0.985
            else:
                self.cash += self.share * self.data.loc[self.idx, 'close'] * 0.995
            self.share = 0
            self.data.loc[self.idx, 'value'] = self.cash + self.share * self.data.loc[self.idx, 'close']
            self.data.loc[self.idx, 'operation'] = 0
            self.sr.append(self.idx)
            self.figure_plot()
            self.label_update()
            self.__need_quit()
        else:
            tk.messagebox.showwarning('Notification','No share to sell, please buy first!')

    def hold(self):
        if not self.__need_quit():
            self.idx += 1
            if len(self.br) == 0:
                self.last_buy_interval = 0
            else:
                self.last_buy_interval = self.idx - self.br[-1]
            self.data.loc[self.idx, 'value'] = self.cash + self.share * self.data.loc[self.idx, 'close']
            self.figure_plot()
            self.label_update()
            self.__need_quit()

    def quit(self):
        self.summary_plot()
        self.destroy()

    def figure_plot(self):
        self.ax.clear()
        data_slice = self.data.iloc[max(0, self.idx - self.win_size):(self.idx + 1), :]
        self.ax.bar(x=data_slice.index, height=data_slice.loc[:, 'hist'], bottom=8000)
        self.ax.plot(data_slice['close'])
        self.ax.plot(data_slice['value'])
        # plt.grid(color="k", linestyle=":")
        self.ax.set_xticks(data_slice.index)
        self.ax.set_xticklabels(data_slice['date'], rotation='vertical')
        # plt.savefig("test.png", dpi=120)
        if len(self.sr) != 0:
            for xsr in self.sr:
                if xsr >= self.idx - self.win_size:
                    self.ax.axvline(x=xsr, c='green')
        if len(self.br) != 0:
            for xbr in self.br:
                if xbr >= self.idx - self.win_size:
                    self.ax.axvline(x=xbr, c='red')
        self.canvas.draw()

    def summary_plot(self):
        self.ax.clear()
        data_slice = self.data.iloc[self.start:(self.idx), :]
        self.ax.bar(x=data_slice.index, height=data_slice['hist'], bottom=8000)
        self.ax.plot(data_slice['close'])
        self.ax.plot(data_slice['value'])
        # plt.grid(color="k", linestyle=":")
        self.ax.set_xticks(data_slice.index)
        self.ax.set_xticklabels(data_slice['date'], rotation='vertical')
        # plt.savefig("test.png", dpi=120)
        if len(self.sr) != 0:
            for xsr in self.sr:
                self.ax.axvline(x=xsr, c='green')
        if len(self.br) != 0:
            for xbr in self.br:
                self.ax.axvline(x=xbr, c='red')
        self.canvas.draw()
        self.fig.savefig('./user_decision_plot.png')

    def label_update(self):
        if self.last_buy_interval <= 7:
            self.sell_fee_percent = 1.5
        else:
            self.sell_fee_percent = 0.5
        self.text.set(
            'Your current value is %d.\n The day interval from your last buy is %d, so the current sell charge percentage is %.2f%%' % (
            self.data.loc[self.idx, 'value'], self.last_buy_interval, self.sell_fee_percent))
        self.lb.configure(textvariable=self.text)

    def __need_quit(self):
        # self.quit()
        if self.idx >= len(self.data):
            self.summary_plot()
            self.destroy()
            return True
        else:
            return False


def prepare_data(path):
    df1 = pd.read_csv(path)
    df1['operation'] = [2 for i in range(len(df1))]
    cash = 10000
    df1['value'] = [cash for i in range(len(df1))]
    return df1


if __name__ == '__main__':
    datapath = './game_data.csv'
    df = prepare_data(datapath)
    app = Application(df, 573)
    app.mainloop()
