# -*- coding: utf:8 -*-
from application import Window
import tkinter as tk
import requests


def main():
    root = tk.Tk()
    app = Window(root)
    app.set_frame_upper()
    app.set_frame_lower()
    app.set_title()
    app.first_date_entry()
    app.last_date_entry()
    app.set_checkbox_last_date()
    app.set_btn_search()

    root.mainloop()

if __name__ == '__main__':
    main()

