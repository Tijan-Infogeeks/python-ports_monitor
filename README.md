# python-ports_monitor
a python port monitor to monitor and free ports occupied by other programs

🖥️ Moniteur de Ports – Temps Réel (Windows)

Moniteur de Ports est une application Python avec interface graphique moderne (basée sur ttkbootstrap) permettant de visualiser les ports en écoute ou occupés sur un système Windows, ainsi que les processus qui les utilisent.

Elle utilise la commande netstat et la librairie psutil pour afficher en temps réel les connexions réseau, avec la possibilité d’appliquer des filtres et de tuer des processus directement depuis l’interface.

⚙️ Fonctionnalités principales

✅ Affichage des ports ouverts (TCP & UDP)
✅ Nom du processus associé (via PID)
✅ Filtres par protocole, PID, ou numéro de port
✅ Bouton “Tuer le processus sélectionné”
✅ Rafraîchissement manuel (pas automatique, pour avoir le temps de lire)
✅ Interface moderne et responsive avec ttkbootstrap (thème darkly)

🧩 Technologies utilisées

🐍 Python 3.10+

🎨 ttkbootstrap (interface moderne basée sur Tkinter)

⚙️ psutil (pour accéder aux informations système et gérer les processus)

💻 netstat (commande Windows pour la liste des connexions réseau)

🚀 Installation

Clone le dépôt :

git clone https://github.com/<ton-nom-utilisateur>/ports-monitor.git
cd ports-monitor


Installe les dépendances :

pip install ttkbootstrap psutil


Lance le programme :

python ports_monitor.py

<img width="499" height="415" alt="image" src="https://github.com/user-attachments/assets/9bec3e44-807b-41f8-9ec1-5c1d7971e1d8" />
