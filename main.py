import customtkinter as CTk

class WelcomeDialogBox(CTk.CTkToplevel):
    def __init__(self,parent,onSubmitCallback):
        super().__init__(parent)
        self.title("Welcome to NodeChat")
        self.geometry("400x300")
        self.resizable(False,False)
        self.onSubmit=onSubmitCallback
        self.protocol("WM_DELETE_WINDOW",self.onClose)

        CTk.set_appearance_mode("System")
        CTk.set_default_color_theme("blue")

        self.label = CTk.CTkLabel(self,text="Welcome to NodeChat",font=CTk.CTkFont(size=18, weight="bold"))
        self.label.pack(pady=(30,10))

        self.label2 = CTk.CTkLabel(self, text="Please enter your name:")
        self.label2.pack(pady=(10,5))

        self.nameEntry = CTk.CTkEntry(self, placeholder_text="Your name")
        self.nameEntry.pack(padx=40, pady=(5, 20))
        self.nameEntry.bind("<Return>", self.submitName)

        self.submitButton = CTk.CTkButton(self, text="Enter Chat", command=self.submitName)
        self.submitButton.pack()

        self.grab_set()  # Focus on this window

    def submitName(self,event = None):
        name = self.nameEntry.get().strip()
        if name:
            self.onSubmit(name,"127.0.0.1")
            self.destroy()
    
    def onClose(self):
        self.master.destroy()



class ChatAppUi:

    def __init__(self,root):
        self.root = root
        self.root.withdraw()
        self.username = None
        self.ipaddress= None

        self.dialog = WelcomeDialogBox(root,self.startChat)

    def startChat(self, name,ipaddress):
        self.username = name
        self.ipaddress= ipaddress
        self.root.deiconify()
        self.buildChatUi()
    def buildChatUi(self):
        self.root.title("NodeChat")
        self.root.geometry("800x600")
        self.root.minsize(800,600)

        self.mainframe = CTk.CTkFrame(self.root)
        self.mainframe.pack(fill="both",expand=True)

        #sidebar
        self.sidebar = CTk.CTkFrame(self.mainframe, width=200)
        self.sidebar.pack(side="left", fill="y", padx=(10, 5), pady=10)

        self.userInfo = CTk.CTkLabel(
            self.sidebar, 
            text=f"Username: {self.username}\nIP: {self.ipaddress}", 
            wraplength=180
        )
        self.userInfo.pack(pady=(10, 20), padx=10)

        self.contactListLabel = CTk.CTkLabel(self.sidebar, text="Contacts", anchor="w")
        self.contactListLabel.pack(padx=10)

        self.contactList = CTk.CTkScrollableFrame(self.sidebar, width=180, height=100)
        self.contactList.pack(padx=10, pady=(0,5), fill="both", expand=True)

        self.addContactBtn = CTk.CTkButton(self.sidebar, text="+ Add Contact")
        self.addContactBtn.pack(padx=10, pady=10)


        #chat section

        self.chatPanel = CTk.CTkFrame(self.mainframe)
        self.chatPanel.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        self.chatDisplay = CTk.CTkTextbox(self.chatPanel, state="disabled", wrap="word")
        self.chatDisplay.pack(padx=10, pady=10, fill="both", expand=True)

        # Bottom bar
        self.bottomBar = CTk.CTkFrame(self.chatPanel)
        self.bottomBar.pack(fill="x", padx=10, pady=(0, 10))

        self.messageEntry = CTk.CTkEntry(self.bottomBar, placeholder_text="Type your message...", width=200)
        self.messageEntry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.sendButton = CTk.CTkButton(self.bottomBar, text="Send")
        self.sendButton.pack(side="right")



if __name__ == "__main__":
    CTk.set_appearance_mode("System")
    CTk.set_default_color_theme("blue")

    root = CTk.CTk()
    app=ChatAppUi(root)
    root.mainloop()