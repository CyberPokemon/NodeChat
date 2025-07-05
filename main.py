import customtkinter as CTk
import socket
from datetime import datetime as dt
import threading
import json

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

        self.ipAddress= self.get_my_ip()

        self.ipLabel = CTk.CTkLabel(self, text=f"IP: {self.ipAddress if self.ipAddress != '127.0.0.1' else 'NOT CONNECTED TO ANY NETWORK'}")
        self.ipLabel.pack(pady=(10,5))

        self.submitButton = CTk.CTkButton(self, text="Enter Chat", command=self.submitName)
        self.submitButton.pack()

        self.errorLabel = CTk.CTkLabel(self, text="", text_color="red")
        self.errorLabel.pack(pady=(5, 0))

        self.grab_set()  # Focus on this window


    def get_my_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
        except:
            ip = "127.0.0.1"
        return ip   

    def submitName(self,event = None):
        name = self.nameEntry.get().strip()
        ip= self.ipAddress
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

class Message:
    def __init__(self,messageContent: str, isSender: bool):
        self.content = messageContent
        self.isSender=isSender
        self.timestamp = dt.now()

class Contact:
    def __init__(self,name, ipAddress, receiverUserName):
        self.name=name
        self.ipAddress= ipAddress
        self.receiverUserName=receiverUserName
        self.chatHistory=[]
        

class AddContactdialogBox(CTk.CTkToplevel):
    
    def __init__(self,parent,onSubmitCallback):
        super().__init__(parent)

        self.title("Add New Contact")
        self.geometry("500x350")
        self.resizable(False, False)
        self.onSubmit = onSubmitCallback
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.fetchedUsername = None

    
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

        self.fetchButton = CTk.CTkButton(self, text="Fetch Username", command=self.fetchUsername)
        self.fetchButton.pack(pady=(5, 5))

        self.fetchedUsernameLabel = CTk.CTkLabel(self, text="Fetched Username: Not fetched yet")
        self.fetchedUsernameLabel.pack()


        self.errorLabel = CTk.CTkLabel(self, text="", text_color="red")
        self.errorLabel.pack()

        self.submitButton = CTk.CTkButton(self, text="Add", command=self.submit)
        self.submitButton.pack(pady=10)

        self.grab_set() 

    def fetchUsername(self):
        ip = self.ipEntry.get().strip()
        if not ip or ip == "127.0.0.1":
            self.fetchedUsernameLabel.configure(text="Fetched Username: Invalid IP", text_color="red")
            return

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                s.connect((ip, 5000))
                s.send("HELLO".encode())
                username = s.recv(1024).decode()
                self.fetchedUsername = username
                self.fetchedUsernameLabel.configure(text=f"Fetched Username: {username}", text_color="green")
        except:
            self.fetchedUsername = None
            self.fetchedUsernameLabel.configure(text="Fetched Username: Could not reach user", text_color="red")


    def submit(self):
        name = self.nameEntry.get().strip()
        ip = self.ipEntry.get().strip()
        receiverName = self.fetchedUsername

        if name and (ip !="127.0.0.1") and receiverName:
            self.onSubmit(name,ip,receiverName)
            self.destroy()
        elif len(name)==0:
            self.errorLabel.configure(text="Enter recipents name")
            return
        elif ip == "127.0.0.1" or len(ip)==0:
            self.errorLabel.configure(text="INVALID NETWORK IP")
            return
        elif receiverName =="Fetched Username: Could not reach user":
            self.errorLabel.configure(text="Enter correct ip to get the receiver username")
            return

class ChatAppUi:

    def __init__(self,root):
        self.root = root
        self.root.withdraw()
        self.username = None
        self.ipaddress= None
        self.contacts=[]

        self.dialog = WelcomeDialogBox(root,self.startChat)

    def refreshContactList(self):
        for widget in self.contactList.winfo_children():
            widget.destroy()

        
        for contact in self.contacts:
            contactLabel = CTk.CTkButton(self.contactList,text=f"{contact.name}\n{contact.receiverUserName}\n{contact.ipAddress}",anchor="w",command=lambda c=contact: self.loadChat(c))
            contactLabel.pack(padx=5,pady=5,fill="x",anchor="w")

    def moveContactToTop(self,contact):
        if contact in self.contacts:
            self.contacts.remove(contact)
            self.contacts.insert(0,contact)
            self.refreshContactList()

    def fetchUsername(self,ip):
        if not ip or ip == "127.0.0.1":
            return "error"
        else:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(2)
                    s.connect((ip, 5000))
                    s.send("HELLO".encode())
                    username = s.recv(1024).decode()
                    return username
            except:
                return ""


    def startServer(self):
        def server_thread():
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('', 5000))
            server_socket.listen(5)
            while True:
                try:
                    client_socket, addr = server_socket.accept()
                    data = client_socket.recv(1024).decode()
                    if data == "HELLO":
                        client_socket.send(self.username.encode())
                    else:
                        try:
                            messageData = json.loads(data)
                            senderIP=addr[0]
                            messageText = messageData.get("message")
                        

                            contact = next((c for c in self.contacts if c.ipAddress == senderIP),None)
                            if contact:
                                contact.chatHistory.append(Message(messageText,False))
                                if hasattr(self, "activeContact") and self.activeContact == contact:
                                    self.loadChat(contact)
                            else:
                                # print("Unknown contact from IP:", senderIP)
                                username = self.fetchUsername(senderIP)
                                # newcontact= Contact(username,senderIP,username)
                                self.addContactToList(username,senderIP,username)
                                contact = next((c for c in self.contacts if c.ipAddress == senderIP),None)
                                contact.chatHistory.append(Message(messageText,False))
                                if hasattr(self, "activeContact") and self.activeContact == contact:
                                    self.loadChat(contact)
                            self.moveContactToTop(contact)

                        except Exception as e:
                            print("Invalid message format or error:", e)
                    client_socket.close()
                except Exception as e:
                    print("Server error:", e)

        threading.Thread(target=server_thread, daemon=True).start()


    def startChat(self, name,ipaddress):
        self.username = name
        self.ipaddress= ipaddress
        self.root.deiconify()
        self.buildChatUi()
        self.startServer()
    
    def loadChat(self,contact : Contact):
        self.activeContact = contact
        self.chatDisplay.configure(state="normal")
        self.chatDisplay.delete("1.0","end")


        for m in contact.chatHistory:
            timestr= m.timestamp.strftime("%H:%M")
            formatted_msg = f"{m.content}  [{timestr}]\n"

            if m.isSender:
                self.chatDisplay.insert("end", "[You] "+formatted_msg, "right")
            else:
                self.chatDisplay.insert("end", "["+self.activeContact.name+"] "+formatted_msg, "left")
        self.chatDisplay.configure(state="disabled")
        self.chatDisplay.see("end")


    def addContactToList(self,name,ip,receiverUserName):

        for contact in self.contacts:
            if contact.ipAddress==ip:
                return  
                #eliminating duplicate contacts
        
        contact = Contact(name,ip,receiverUserName)
        self.contacts.append(contact)

        contactLabel = CTk.CTkButton(self.contactList,text=f"{name}\n{receiverUserName}\n{ip}", anchor="w",command=lambda: self.loadChat(contact))

        contactLabel.pack(padx=5, pady=5, fill="x", anchor="w")
    
    def openAddContactDialog(self):
        AddContactdialogBox(self.root, self.addContactToList)


    def sendMessage(self):
        message = self.messageEntry.get().strip()

        if not message:
            return
        
        if not hasattr(self, "activeContact") or self.activeContact is None:
            return


        msg = Message(message,True)
        self.activeContact.chatHistory.append(msg)
        self.moveContactToTop(self.activeContact)
        self.messageEntry.delete(0,"end")

        self.loadChat(self.activeContact) 

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.activeContact.ipAddress,5000))
                data = json.dumps({"message":message})
                s.send(data.encode())
        except Exception as e:
            print("Failed to send message:", e)

    
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

        self.addContactBtn = CTk.CTkButton(self.sidebar, text="+ Add Contact",command=self.openAddContactDialog)
        self.addContactBtn.pack(padx=10, pady=10)


        #chat section

        self.chatPanel = CTk.CTkFrame(self.mainframe)
        self.chatPanel.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        self.chatDisplay = CTk.CTkTextbox(self.chatPanel, state="disabled", wrap="word")
        self.chatDisplay.pack(padx=10, pady=10, fill="both", expand=True)

        # self.chatDisplay.tag_configure("left", justify="left")
        # self.chatDisplay.tag_configure("right", justify="right")

        # Bottom bar
        self.bottomBar = CTk.CTkFrame(self.chatPanel)
        self.bottomBar.pack(fill="x", padx=10, pady=(0, 10))

        self.messageEntry = CTk.CTkEntry(self.bottomBar, placeholder_text="Type your message...", width=200)
        self.messageEntry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.sendButton = CTk.CTkButton(self.bottomBar, text="Send", command=self.sendMessage)
        self.messageEntry.bind("<Return>", lambda event: self.sendMessage()) # send using pressing return key
        self.sendButton.pack(side="right")



if __name__ == "__main__":
    CTk.set_appearance_mode("System")
    CTk.set_default_color_theme("blue")

    root = CTk.CTk()
    app=ChatAppUi(root)
    root.mainloop()