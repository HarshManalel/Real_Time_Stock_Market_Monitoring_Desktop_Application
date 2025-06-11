# 📈 Real-Time Stock Market Monitoring App

A Python-based desktop application that streams **live stock prices** using Zerodha’s KiteConnect & KiteTicker APIs. The app features an interactive GUI built with Tkinter and uses SQLite to store and manage user-selected stock lists under categories like **NIFTY 50**, **NIFTY BANK**, etc. It supports **real-time updates**, **multithreading**, and **WebSocket integration** to ensure a smooth, responsive experience during market hours.

---

## 🚀 Features

- ✅ Real-time stock price updates via WebSocket
- 📊 Displays LTP, high, low, volume, and % change
- 🧠 Responsive GUI built using Tkinter
- 🗂️ SQLite database to store stock symbols by category
- ⚙️ Add/Remove stocks dynamically
- 🔄 Replace entire stock lists easily (e.g., update NIFTY 50)
- 🧵 Multithreaded to prevent GUI freezing
- 🔐 Secure token management (no hardcoded API keys)

---

## 🛠️ Technologies Used

- **Python 3.11**
- **Zerodha KiteConnect & KiteTicker API**
- **Tkinter** (GUI)
- **SQLite3** (Local database)
- **WebSockets** (Live data streaming)
- **Threading** (For background processes)
