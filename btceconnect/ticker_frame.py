import tkinter as tk

TICKER_FONT = ('Verdana', 7, "bold")
RED = "red"
BLACK = "black"


class TickerFrame(tk.Frame):
    ticker_fields = ["buy", "sell", "last", "low", "high", "avg", "vol", "vol_cur", "updated"]

    def __init__(self, master, pair_name, pair_ticker):
        super().__init__(master)
        self.name = pair_name
        self.__build_ticker_frame(pair_ticker)
        self.__config_visual()
        self.grid(sticky="NEWS")

    def __config_visual(self):
        self.config(borderwidth=2)
        self.config(relief=tk.RAISED)
        self.config(padx=5, pady=5)

    def __build_ticker_frame(self, ticker):
        frame_name = self.name + "_ticker_frame"
        ticker_frame = tk.Frame(self, name=frame_name)

        frame_label = tk.Label(ticker_frame, fg=RED, text=self.name.upper(), name=self.name + "_frame_label",
                               font=TICKER_FONT)
        frame_label.grid(row=0, column=0)

        key_value_labels = [
            [tk.Label(ticker_frame, fg=BLACK, text=field, anchor=tk.W,
                      name="{}_{}_{}".format(self.name, field, "label"),
                      font=TICKER_FONT),
             tk.Label(ticker_frame, width=20, anchor=tk.E, text=ticker[field],
                      name="{}_{}_{}".format(self.name, field, "value"),
                      font=TICKER_FONT)]
            for field in self.ticker_fields]

        # LAYOUT
        row = 0
        column = 1
        grid = [1, 0]

        for labels in key_value_labels:
            key_label, value_label = labels

            # adds a highlighting feature to the label
            # key_label.bind('<Button-1>', self.highlight)

            key_label.grid(row=grid[row], column=grid[column], sticky=tk.W)
            grid[column] = 1
            value_label.grid(row=grid[row], column=grid[column], sticky=tk.E)
            grid[row] += 1
            grid[column] = 0

        # END LAYOUT

        ticker_frame.grid()

    def __highlight(self, event):
        """Highlights labels to improves visualization"""
        pass

    def update_values(self, ticker):
        """Updates all pair fields with give ticker info"""
        try:
            frame = self.children["{}_ticker_frame".format(self.name)]
        except KeyError as e:
            print(e)
        else:
            for label_name, label_widget in frame.children.items():
                if label_name.endswith("_value"):
                    ticker_field = label_name.split("_")[2]
                    label_widget.configure(text=ticker[self.name][ticker_field])
