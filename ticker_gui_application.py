"""
    Monitor on real time the ticker information of all pairs given by btc-e
"""

import time
import tkinter as tk
from threading import Thread
from tkinter import messagebox
from btceconnect import Trader
from btceconnect import TickerFrame

global updating
updating = True


class Tickers(tk.Frame):
    def __init__(self, master, trader, refresh_rate=2):
        super().__init__(master)
        self.trader = trader
        self.refresh_rate = refresh_rate
        self.ticker_frames = list()
        self.config_widgets()
        self.grid(sticky="NEWS")

    def update_frames(self):
        global updating
        while updating:
            ticker_data = self.trader.ticker_public()
            for ticker in self.ticker_frames:
                ticker.update_values(ticker_data)
            time.sleep(self.refresh_rate)

    def config_widgets(self):
        ticker_data = self.trader.ticker_public()
        for pair_name, pair_ticker in sorted(ticker_data.items()):
            self.ticker_frames.append(TickerFrame(self, pair_name, pair_ticker))

        row = 0
        column = 1
        grid = [1, 0]

        max_num_columns = 10
        track = []  #

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


def window_on_closing(root):
    global updating
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        updating = False
        root.destroy()


def main():

    # PLEASE DO NOT LEAVE YOUR KEY AND SECRET IN PLAIN TEXT ON YOUR CODE
    key = "here goes your key"
    secret = "here goes your secret"

    root = tk.Tk()
    root.title("BTC-e Ticker Information")
    root.protocol("WM_DELETE_WINDOW", lambda: window_on_closing(root))

    trader = Trader(key, secret)

    application = Tickers(root, trader)

    update_thread = Thread(target=application.update_frames)
    update_thread.start()

    application.mainloop()


if __name__ == "__main__":
    main()
