import customtkinter as CTk
import socket

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

        self.nameLabel = CTk.CTkLabel(self, text="Please enter your name:")
        self.nameLabel.pack(pady=(10,5))

        self.nameEntry = CTk.CTkEntry(self, placeholder_text="Your name")
        self.nameEntry.pack(padx=40, pady=(5, 20))
        self.nameEntry.bind("<Return>", self.submitName)

        self.ipLabel = CTk.CTkLabel(self, text=f"ip : {socket.gethostbyname(socket.gethostname()) if socket.gethostbyname(socket.gethostname())!="127.0.0.1" else "NOT CONNECTED TO ANY NETWORK"}")
        self.ipLabel.pack(pady=(10,5))

        self.submitButton = CTk.CTkButton(self, text="Enter Chat", command=self.submitName)
        self.submitButton.pack()

        self.errorLabel = CTk.CTkLabel(self, text="", text_color="red")
        self.errorLabel.pack(pady=(5, 0))

        self.grab_set()  # Focus on this window

    def submitName(self,event = None):
        name = self.nameEntry.get().strip()
        ip= socket.gethostbyname(socket.gethostname())
        if name and (ip !="127.0.0.1"):
            self.onSubmit(name,ip)
            self.destroy()
        elif len(name)==0:
            self.errorLabel.configure(text="Enter your username")
            return
        elif ip == "127.0.0.1":
            self.errorLabel.configure(text="You are not connected to a network!")
            return

        
    
    def onClose(self):
        self.master.destroy()

class Contact:
    def __init__(self,name, ipAddress):
        self.name=name
        self.ipAddress= ipAddress
        self.chatHistory=[]
        

class AddContactdialogBox(CTk.CTkToplevel):
    
    def __init__(self,parent,onSubmitCallback):
        super().__init__(parent)

        self.title("Add New Contact")
        self.geometry("300x200")
        self.resizable(False, False)
        self.onSubmit = onSubmitCallback
        self.protocol("WM_DELETE_WINDOW", self.destroy)
    
        CTk.set_appearance_mode("System")
        CTk.set_default_color_theme("blue")

        self.label = CTk.CTkLabel(self, text="Enter Contact Name:")
        self.label.pack(pady=(20, 5))

        self.nameEntry = CTk.CTkEntry(self, placeholder_text="Name")
        self.nameEntry.pack(padx=20, pady=5)

        self.ipLabel = CTk.CTkLabel(self, text="Enter IP Address:")
        self.ipLabel.pack(pady=(10, 5))

        self.ipEntry = CTk.CTkEntry(self, placeholder_text="e.g., 192.168.1.2")
        self.ipEntry.pack(padx=20, pady=5)

        self.errorLabel = CTk.CTkLabel(self, text="", text_color="red")
        self.errorLabel.pack()

        self.submitButton = CTk.CTkButton(self, text="Add", command=self.submit)
        self.submitButton.pack(pady=10)

        self.grab_set() 

    def submit(self):
        name = self.nameEntry.get().strip()
        ip = self.ipEntry.get().strip()

        if name and (ip !="127.0.0.1"):
            self.onSubmit(name,ip)
            self.destroy()
        elif len(name)==0:
            self.errorLabel.configure(text="Enter recipents name")
            return
        elif ip == "127.0.0.1" or len(ip)==0:
            self.errorLabel.configure(text="INVALID NETWORK IP")
            return

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