# NodeChat

NodeChat is a lightweight, peer-to-peer chat application built in Python using socket programming and a modern GUI powered by [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter).

Unlike traditional chat applications, NodeChat operates entirely on your **local network (LAN)**, requiring **no internet connection or central server**. Each user acts as both a client and a server, enabling fully decentralized, secure, and private messaging.

---

## 🚀 Features

- 📡 Peer-to-peer chat over LAN — no server needed
- 🪪 Auto-discovery of contact usernames by IP
- 💬 Real-time message sending and receiving
- 🕓 Chat history with timestamps
- 🧑‍🤝‍🧑 Contact list panel with IP, username, and display name
- 🧵 Multithreaded backend for non-blocking communication
- 🌙 Clean, responsive UI using CustomTkinter (supports light/dark modes)
- 🔒 No data leaves your local network

---


## 📦 Installation

> Requires Python 3.9 or later

1. **Clone the repository**:

```bash
git clone https://github.com/CyberPokemon/NodeChat.git
cd NodeChat
```

2. **Create a virtual environment** (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Run the app**:

```bash
python3 main.py
```

---

## 🔧 Dependencies

- [`customtkinter`](https://github.com/TomSchimansky/CustomTkinter)
- Standard libraries: `socket`, `threading`, `datetime`, `json`, etc.

All dependencies are listed in `requirements.txt`.

---

## 🛠 Usage Tips

- All devices must be on the **same local network** (Wi-Fi or Ethernet).
- Use the **About section** to view app info.
- Supports **multithreading** — UI stays responsive even during messaging.

---

## 💡 Future Improvements

- ✅ File sharing support (images, files)
- ✅ Emoji support
- 🔒 Encrypted messaging (SSL/TLS)
- 🌐 Cross-network discovery (via relays or bridging)
- 📱 Mobile/Tablet UI support

---

## 🧑‍💻 Contribution

Want to contribute? PRs are welcome! Open an issue or fork the repo.

---

## 📄 License

MIT License © 2025 Imon Mallik
---
