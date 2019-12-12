import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

# image PIL

from tkinter import *
from PIL import ImageTk, Image


# window=tk.Tk()
# window.title("運彩模擬器")
# window.geometry("500x300")
# # welcome page
# canvas=tk.Canvas(window, height=500, width=300)
# img=Image.open("NBALogo.gif")
# img=img.resize((500, 300), Image.ANTIALIAS) 
# img=ImageTk.PhotoImage(img)
# image=canvas.create_image(0, 0, anchor="nw", image=img)
# canvas.pack(fill=BOTH)

# font1=tkFont.Font(size=15, family="Didot")
# tk.Label(window, text="User name:", font=font1).place(x=50,y=150)
# tk.Label(window, text="Password", font=font1).place(x=50, y=190)

# var_usr_name=tk.StringVar()
# # 默認值
# # var_usr_name.set("")
# entry_usr_name=tk.Entry(window, textvariable=var_usr_name)
# entry_usr_name.place(x=160, y=150)

# var_usr_pwd=tk.StringVar()
# entry_usr_pwd=tk.Entry(window, textvariable=var_usr_pwd, show="*") 
# entry_usr_pwd.place(x=160, y=190)

# def usr_login():
#     pass 
# def usr_signup():
#     pass


# btn_login=tk.Button(window, text="Log in", font=font1, command=usr_login)
# btn_login.place(x=170, y=230)
# btn_signup=tk.Button(window, text="Sign up", font=font1, command=usr_signup)
# btn_signup.place(x=270, y=230)
# window.mainloop()


# class LogIn(tk.Frame):
#     def __init__(self):
#         tk.Frame.__init__(self)
#         self.grid()
#         self.createWidgets()


class SportsLottery(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(LoginPage)
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame = new_frame
            
class LoginPage(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self) 
        self.master.title("運彩模擬器")
        self.master.geometry("300x300")  #出現視窗的大小
        self.pack()
        self.createWidgets()
        # self.master.configure(bg="misty rose")
    
    def createWidgets(self):
        # welcome page
        self.canvas=tk.Canvas(self, height=1000, width=500) #??
        self.img=Image.open("NBALogo.gif")
        self.img=self.img.resize((200, 200), Image.ANTIALIAS) 
        self.img=ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.img)
        self.canvas.pack(fill=BOTH,expand=Y)

        f1=tkFont.Font(size=15, family="Didot")
        self.l1=tk.Label(self.canvas, text="User name:", font=f1)
        self.l2=tk.Label(self.canvas, text="Password:", font=f1)
        self.l1.pack(side=TOP, fill=X, padx=10, pady=10)
        self.var_usr_name=tk.StringVar(self)
        self.entry_usr_name=tk.Entry(self.canvas, textvariable=self.var_usr_name)
        self.entry_usr_name.pack()
        # 默認值
        # var_usr_name.set("")
        self.l2.pack(side=TOP,padx=20, pady=10) #fill=X, 

        self.var_usr_pwd=tk.StringVar()
        self.entry_usr_pwd=tk.Entry(self.canvas, textvariable=self.var_usr_pwd, show="*") 
        self.entry_usr_pwd.pack(side=TOP, padx=10, pady=10)
        
        self.btn_login=tk.Button(self.canvas, text="Log in", font=f1, command=self.usr_login)
        self.btn_login.pack(side=RIGHT, padx=10, pady=10)
        self.btn_signup=tk.Button(self.canvas, text="Sign up", font=f1, command=self.usr_signup)
        self.btn_signup.pack(side=RIGHT, padx=10, pady=10)
    def usr_login(self):
        pass 
    def usr_signup(self):
        pass
    

app=SportsLottery()
app.mainloop()