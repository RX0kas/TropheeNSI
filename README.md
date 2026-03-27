# BlackJack
Cette application est une recréation du jeu de BlackJack avec quelques modifications.

## Prerequis
- [Python 3.11](https://www.python.org/downloads/)
- Window 10/11 ou Ubuntu

## Comment installer
```bash
>>> git clone https://github.com/RX0kas/TropheeNSI
>>> cd ./TropheeNSI
```
##### Windows
```bash
>>> python -m venv .venv
>>> ./.venv/Scripts/activate.bat
```
##### Ubuntu
```bash
>>> python -m venv .venv
>>> ./.venv/bin/activate
```
#### Installer les dépendances et lancer
```bash
>>> pip install -r requirements.txt
>>> python main.py
```
## Changement
Le fonctionnement est légèrement différent de celui du blackjack.
On vous proposera 5 jeux. Vous pouvez défausser ou jouer à au moins 3 jeux à la fois.
Vous êtes limité dans le nombre de défausses et de jeux que vous allez pouvoir faire.
L'objectif est de faire 250 points.