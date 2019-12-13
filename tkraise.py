import tkinter as tk
from tkinter import *
import webbrowser
import tkinter.font as tkFont
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from PIL import Image, ImageTk
import io 
from io import BytesIO
import ssl
 # f1=tkFont.Font(size=20, family="標楷體")
 # f2=tkFont.Font(size=10, family="微軟正黑體")
 

class SportsLottery(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("1000x1000")
        self.title("新聞介紹")
        self.title_font=tkFont.Font(family="Didot", size=20)
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        
        container = tk.Frame(self,bg="misty rose",width=500, height=500)
        container.pack(side=TOP, fill=BOTH , expand=TRUE)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        functions=["新聞介紹","球隊介紹","賽事下注","歷史資料","個人帳戶"]
        i=0
        # 這行
        for function in functions:
            btn=tk.Button(container, height=2, width=10, relief=tk.FLAT, bg="lemon chiffon", fg="sienna4", font="Didot", text=function)
            btn.grid(row=0, column=3+i,sticky="NW",padx=5 ,pady=10)
            i+=1
            # btn.pack(side=RIGHT , pady=30, anchor=N)
        # line 40-56
        self.frames = {}
        for page in (StartPage, PageOne, PageTwo): #Pnews
            page_name = page.__name__
            frame = page(parent=container, controller=self)
            self.frames[page_name] = frame # 存進dictionary
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=1, column=0, sticky="nsew")

        self.show_frame("StartPage")
    
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(width=500, height=300)
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SportsLottery()
    app.mainloop()