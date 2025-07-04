import customtkinter as CTK

class WelcomeDialogBox(CTK.CTkToplevel):
    def __init__(self,parent,onSubmitCallback):
        super().__init__(parent)
        self.title("Welcome to NodeChat")
        self.geometry("400x300")
        self.resizable(False,False)
        self.onSubmit=onSubmitCallback
        self.protocol("WM_DELETE_WINDOW",self.onClose)

        CTK.set_appearance_mode("System")
        CTK.set_default_color_theme("blue")

        self.label = CTK.CTkLabel(self,text="Welcome to NodeChat",font=CTK.CTkFont(size=18, weight="bold"))
        self.label.pack(pady=(30,10))

        self.label2 = CTK.CTkLabel(self, text="Please enter your name:")
        self.label2.pack(pady=(10,5))

        self.nameEntry = CTK.CTkEntry(self, placeholder_text="Your name")
        self.nameEntry.pack(padx=40, pady=(5, 20))
        self.nameEntry.bind("<Return>", self.submitName)

        self.submitButton = CTK.CTkButton(self, text="Enter Chat", command=self.submitName)
        self.submitButton.pack()

        self.grab_set()  # Focus on this window

    def submitName(self,event = None):
        name = self.nameEntry.get().strip()
        if name:
            self.onSubmit(name)
            self.destroy()
    
    def onClose(self):
        self.master.destroy()



class ChatAppUi:

    def __init__(self,root):
        self.root = root
        self.root.withdraw()
        self.username = None

        self.dialog = WelcomeDialogBox(root,self.startChat)

    def startChat(self, name):
        self.username = name
        self.root.deiconify()
        self.buildChatUi()
    def buildChatUi():
        pass

if __name__ == "__main__":
    CTK.set_appearance_mode("System")
    CTK.set_default_color_theme("blue")

    root = CTK.CTk()
    app=ChatAppUi(root)
    root.mainloop()