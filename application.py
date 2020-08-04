# -*- coding: utf:8 -*-
from PIL import Image, ImageTk
import tkinter as tk
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

class Window:
    def __init__(self,master):
        self.master = master
        self.WIDTH = 600
        self.HEIGHT = 600
        self.frame1_height = 600*0.2
        self.master.title('Pesquisa Dolar')
        self.master.geometry("{}x{}+960+150".format(self.WIDTH,self.HEIGHT))
        self.master.resizable(False,False)
        self.interval_dates = tk.IntVar()
        self.sv_date1 = tk.StringVar()

    
    def set_frame_upper(self):
        self.frame_upper = tk.Frame(self.master)
        self.frame_upper.place(relwidth=1,relheight=0.2)
        self.canvas = tk.Canvas(self.frame_upper,height = self.frame1_height,width=self.WIDTH)
        self.image = ImageTk.PhotoImage(Image.open("./img.jpg").resize((self.WIDTH, int(self.frame1_height)), Image.ANTIALIAS))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
        self.canvas.pack()


    def set_frame_lower(self):
        self.frame_lower = tk.Frame(self.master,bg='red')
        self.frame_lower.place(rely = 0.2,relwidth=1,relheight=0.8)

    def set_title(self):
        titulo_str = "Pesquisar Preço Dólar, data MMDDAAAA"
        self.titulo = tk.Label(self.frame_upper,text = titulo_str)
        self.titulo.place(relx = 0.5,anchor = tk.N)

    def first_date_entry(self):
        self.sv_date1.trace("w",lambda name, index, mode, sv=self.sv_date1: self.entryUpdateDate(self.sv_date1))
        self.first_date = tk.Entry(self.frame_upper,
        state = 'normal', textvariable = self.sv_date1)
        self.first_date.place(relx = 0.1,
            rely = 0.20,
            relwidth = 0.25,
            relheight=0.25)
        self.first_date.insert(0,'MM-DD-AAAA')
    
    def last_date_entry(self):
        self.sv_date2 = tk.StringVar()
        self.sv_date2.trace("w",lambda name, index, mode, sv=self.sv_date2: self.entryUpdateDate(self.sv_date2))
        self.last_date = tk.Entry(self.frame_upper, 
        state = 'normal', textvariable = self.sv_date2)
        self.last_date.insert(0,'MM-DD-AAAA')
        self.last_date.place(relx = 0.1,
            rely = 0.50,
            relwidth = 0.25,
            relheight=0.25)
        self.last_date.configure(state="disabled")
        

    def entryUpdateDate(self,stringvar):
        digits = list(filter(str.isdigit,stringvar.get()))
        digits =  digits + ["0","0","0","0","0","0","0","0"]
        month = int(digits[0]+digits[1])
        day = int(digits[2]+digits[3])
        year = int(digits[4]+digits[5]+digits[6]+digits[7])
        stringvar.set("{:02d}{:02d}{:04d}".format(month,day,year))


    def second_date_use(self):
        if self.interval_dates.get()==1:
            self.last_date.configure(state="normal")
            self.last_date.update()
            self.last_date.delete(0,'end')
            
            self.last_date.insert(0,dt.datetime.now().strftime("%m%d%Y"))
        else:
            self.last_date.update()
            self.last_date.delete(0,'end')
            self.last_date.insert(0,'MM-DD-AAAA')
            self.last_date.configure(state="disabled")


    def set_checkbox_last_date(self):
        self.checkbox_last_date = tk.Checkbutton(
            self.frame_upper, text = "Dolar em um Periodo",
            variable = self.interval_dates, onvalue = 1,
            offvalue = 0, command = lambda : self.second_date_use()
        )
        self.checkbox_last_date.place(relx = 0.7,
            rely = 0.50)

    def set_btn_begin_real(self):
        self.btn_begin_real = tk.Button(
            self.frame_upper,text = "Plano Real",
            activebackground = '#b5dfff',
            activeforeground = '#ff0800',
            command = lambda : self.set_real_date()
        )
        self.btn_begin_real.place(relx = 0.7,
            rely = 0.25, relwidth = 0.25, relheight=0.25
        )
    
    def set_real_date(self):
        self.first_date.delete(0,"end")
        self.first_date.insert(0,"07011994")

    def set_btn_search(self):
        self.btn_search = tk.Button(self.frame_upper,
            text='Pesquisar',
            activebackground = '#b5dfff',
            activeforeground = '#ff0800',
            command= lambda: self.search())
        self.btn_search.place(relx = 0.375,
            rely = 0.75,
            relwidth = 0.25,
            relheight=0.25)

    def format_date_numbers(self,date):
        month = int(date[0]+date[1])
        day = int(date[2]+date[3])
        year = int(date[4]+date[5]+date[6]+date[7])
        if month>12:
            month=12
        elif month<1:
            month=1
        if day>31:
            day=31
        elif day<1:
            day=1
        if year>dt.datetime.now().year:
            year=dt.datetime.now().year
        elif year<1984:
            year=1984
        return "{:02d}{:02d}{:02d}".format(month,day,year)

    def format_date_to_request(self,date):
        month = int(date[0]+date[1])
        day = int(date[2]+date[3])
        year = int(date[4]+date[5]+date[6]+date[7])
        return "{:02d}-{:02d}-{:02d}".format(month,day,year)

    def search(self):
        date1 = self.sv_date1.get()
        self.first_date.insert(0,self.format_date_numbers(date1))
        if self.interval_dates.get() == 1:
            date2 = self.sv_date2.get()
            self.last_date.insert(0,self.format_date_numbers(date2))
        self.request_api()

    def request_api(self):
        if self.interval_dates.get() == 0:
            url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{}'&$top=100&$format=json&$select=cotacaoCompra"
            url = url.format(self.format_date_to_request(self.sv_date1.get()))
            data = requests.get(url).json().get('value')
            try:
                self.label_result.destroy()
            except:
                pass
            if len(data) == 0:
                str = "Data Invalida ou sem valor de dolar"
            else:
                str = "Valor do Dolar = {}".format(data[0].get('cotacaoCompra'))
            self.label_result = tk.Label(self.frame_lower,
            text = str)
            self.label_result.place(relx = 0.5,
            anchor=tk.N)
        elif self.interval_dates.get() == 1:
            self.frame_lower['bg'] ='blue'
            url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@dataInicial='{begin}'&@dataFinalCotacao='{end}'&$format=json&$select=cotacaoCompra,dataHoraCotacao"
            url = url.format(begin = self.format_date_to_request(self.sv_date1.get()),end = self.format_date_to_request(self.sv_date2.get()))
            data = requests.get(url).json().get('value')
            data = pd.DataFrame(data).set_index('dataHoraCotacao')
            data.index = pd.to_datetime(data.index).date
            self.frame_lower['bg'] ='red'
            print(data.head())