""" Monitor on real time the ticker information of all pairs given by btc-e """
import platform
import signal
import os
import tkinter as tk
import threading
from tkinter import messagebox

from btceconnect import Trader
from ticker_frame import TickerFrame


class Tickers(tk.Frame):
    """ Container frame of all available BTC-e trading pairs """

    def __init__(self, master, trader, refresh_rate):
        super().__init__(master)
        self.master = master
        self.trader = trader
        self.timed_update_thread = None
        self.refresh_rate = refresh_rate
        self.ticker_frames = list()
        self._config_widgets()
        self.grid(sticky="NEWS")
        self.master.protocol("WM_DELETE_WINDOW", self._on_close_window)
        self.start_update_thread()

    def start_update_thread(self):
        """ Sets recursively a new thread to start the TickerFrame update procedure
        according to the given 'refresh_rate' attribute """
        self.timed_update_thread = threading.Timer(self.refresh_rate, self.start_update_thread)
        self.timed_update_thread.start()
        self.update_ticker_frames()

    def update_ticker_frames(self):
        """ Updates all ticker frames objects in the 'ticker_frames' list """
        ticker_data = self.trader.ticker_public()
        for ticker in self.ticker_frames:
            ticker.update_values(ticker_data)

    def _config_widgets(self):
        """ Instanciate a TickerFrame for every Btc-e available pair and lays them out """
        ticker_data = self.trader.ticker_public()
        for pair_name, pair_ticker in sorted(ticker_data.items()):
            self.ticker_frames.append(TickerFrame(self, pair_name, pair_ticker))

        row = 0
        column = 1
        grid = [1, 0]

        max_num_columns = 10
        track = []

        # tries to set an even number of columns in case trading pairs are added or removed
        while len(self.ticker_frames) % max_num_columns:
            track.append(max_num_columns)
            max_num_columns -= 1

        for frame in self.ticker_frames:
            frame.grid(row=grid[row], column=grid[column], sticky="NEWS")
            grid[column] += 1  # place next widget to the next right column

            # if row has reached column max number, return carriage and start at new line
            if grid[column] == min(track) - 1:
                grid[column] = 0
                grid[row] += 1

    def _on_close_window(self):
        """ Cancels running child threads and destroys window """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            try:
                self.timed_update_thread.cancel()
            except AttributeError:
                messagebox.showwarning("Error", "Update thread could not be killed")
                stop = messagebox.askyesnocancel("Quit", "Do you want to force the application to close?")
                if stop and platform == "win32":
                    os.kill(os.getpid(), signal.CTRL_C_EVENT)
                elif platform.system() == "linux":
                    os.kill(os.getpid(), signal.SIGKILL)
                self.master.destroy()
            else:
                self.master.destroy()


def main():
    key = ""
    secret = ""

    refresh_rate = 2
    root = tk.Tk()
    root.title("BTC-e Ticker ")
    trader = Trader(key, secret)
    application = Tickers(root, trader, refresh_rate)
    application.mainloop()


if __name__ == "__main__":
    main()
