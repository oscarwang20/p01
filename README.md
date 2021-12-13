# Word in the Middle Game
---
Advent - Renggeng Zheng, Oscar Wang, Tami Takada, Tomas Acuna  
SoftDev  
P01: ArRESTed Development  

# Roles
Tami: Frontend, word generation  
Oscar: Database  
Reng: API calls  
Tomas: Leaderboard  

# Description
Two players (local on one computer) will be assigned one randomly generated "word in the
middle" by the Random Word API. They will also individually be given two distinct, also
randomly generated, starting words and a selection of related words that appear as links.
Related words are any words that appear as synonyms for the current word given by the
Thesaurus API, and as links in the current word's Wikipedia entry given by the Wikipedia API.

The aim of the game is to get closer to the word in the middle by strategically choosing words
that relate to the previous word. The winner of the game the player that reaches the word
the middle first, determined by their total score at the end of the
game, which is calculated by
the total number of turns they took.

# Launch Codes
Make sure you have python3 and pip3 installed on your computer

1. Clone this repository
```
$ git clone https://github.com/oscarwang20/p01.git
```

2. Create a virtual environment inside the cloned repository directory
```
$ cd p01
$ python3 -m venv foo
$ path/to/venv/bin/activate
```

3. Install dependencies
```
(env) $ pip3 install -r requirements.txt
```

4. Run the server
```
(env) $ python3 __init__.py
```

Head over to localhost:5000 to play the game!
