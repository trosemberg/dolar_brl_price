# -*- coding: utf:8 -*-
from application import Window
import tkinter as tk
import requests


def main():
    # start aplication
    root = tk.Tk()
    # create window 
    app = Window(root)
    # create upper frame 
    app.set_frame_upper()
    # create lower frame
    app.set_frame_lower()
    # add to upper frame text with info
    app.set_title()
    # create entry for first date on upper frame
    app.first_date_entry()
    # create button to insert begin of "Plano Real" date on first entry on upper frame
    app.set_btn_begin_real()
    # create last date entry on upper frame
    app.last_date_entry()
    # create checkbox to enable last date entry on upper frame
    app.set_checkbox_last_date()
    # create  search button on upper frame
    app.set_btn_search()
    # exec mainloop
    root.mainloop()

if __name__ == '__main__':
    main()

