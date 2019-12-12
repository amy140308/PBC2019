class SportsLottery(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(LoginPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame = new_frame
            self._frame.pack()

class LoginPage(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self) 
        self.master.title("運彩模擬器")
        self.master.geometry("500x300")
        self.grid()
        self.createWidgets()
        
        # canvas=tk.Canvas(self, height=500, width=300)
        # img=Image.open( "NBALogo.gif")
        # img=img.resize((500, 300), Image.ANTIALIAS) 
        # img=ImageTk.PhotoImage(img)
        # image=canvas.create_image(0, 0, anchor="nw", image=img)
        # canvas.pack(fill=BOTH)
        
    def createWidgets(self):
        # welcome page
        
        font1=tkFont.Font(size=15, family="Didot")
        self.l1=tk.Label(self, text="User name:", font=font1).place(x=50,y=150)
        self.l2=tk.Label(self, text="Password", font=font1).place(x=50, y=190)
        self.var_usr_name=tk.StringVar(self)
        # 默認值
        # var_usr_name.set("")
        self.entry_usr_name=tk.Entry(self, textvariable=var_usr_name)
        self.entry_usr_name.place(x=160, y=150)

        self.var_usr_pwd=tk.StringVar()
        self.entry_usr_pwd=tk.Entry(self, textvariable=var_usr_pwd, show="*") 
        self.entry_usr_pwd.place(x=160, y=190)

        def usr_login():
            pass 
        def usr_signup():
            pass

        self.btn_login=tk.Button(self, text="Log in", font=font1, command=usr_login)
        self.btn_login.place(x=170, y=230)
        self.btn_signup=tk.Button(self, text="Sign up", font=font1, command=usr_signup)
        self.btn_signup.place(x=270, y=230)


app=SportsLottery()
app.mainloop()
    