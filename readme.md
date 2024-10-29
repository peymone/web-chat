<h1 align="center">Real Time Chat</h1>

<p align="center">
    <img src="https://img.shields.io/badge/%20Python-3.11.3-blue?style=for-the-badge&logo=Python" alt="Python">
    <img src="https://img.shields.io/badge/%20SQLAlchemy-2.0.36-brightgreen?style=for-the-badge" alt="SQLAlchemy">
    <img src="https://img.shields.io/badge/%20Flask-3.0.3-brightgreen?style=for-the-badge" alt="Flask">
    <img src="https://img.shields.io/badge/%20SocketIO-5.4.1-brightgreen?style=for-the-badge" alt="Flask-SocketIO">
    <img src="https://img.shields.io/badge/WTForms-3.2.1-brightgreen?style=for-the-badge" alt="WTForms">
</p>

<p align="center">
    <img src="https://img.shields.io/github/downloads/peymone/web-chat/total?style=social&logo=github" alt="downloads">
    <img src="https://img.shields.io/github/watchers/peymone/web-chat" alt="watchers">
    <img src="https://img.shields.io/github/stars/peymone/web-chat" alt="stars">
</p>

<h2>About</h2>

_**Real time chat application with websockets usage. Websocket communication implements with help of flask-socketio library. What else can I say about it? Well, events are pain in my, and I hope, in everyone else asses.**_

_**Also, I want to thanks FrontEnd Developers for this div positioning shit. Thank you all, bye everyone. Let's go roll out the app.**_

_P.S. If you find a bag... and you will find it. Know, I don't care._

<h2>CI/CD</h2>


- _**Clone repo or save release manually**:_ ```git clone https://github.com/peymone/web-chat.git```
- _**Create python virtual environment:**_ ```python -m venv venv```
- _**Activate virtual environment:**_ ```venv/scripts/activate```
- _**Install dependencies**:_ ```pip install -r requirements.txt```
- _**Create database with alembic:**_ ```alembic upgrade head```
- _**Add new chat room in database by command:**_ ```python -c 1```
- _**Run server**:_ ```python chat.py```
- _**Go, pass registration and let's chatting: <a href="http://127.0.0.1:5000/auth/reg">registration</a>**_

_You also can change some settings in ```app/.env``` or check available cli commands with ```python chat.py -h```_

> _Easy right? And no need for docker mambo-jambo_
