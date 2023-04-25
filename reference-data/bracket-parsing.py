from bs4 import BeautifulSoup
import re
import json

def parse_player(text):
    text = text[1:]
    match = re.match(r'^(\d+)(.*)$', text)
    if match:
        # In our system seeding starts at 0
        return int(match.group(1)) - 1
    else:
        return text

def parse(html):
    rep = {}
    soup = BeautifulSoup(html)
    for match in soup.find_all(class_="match"):
        label = match.find(class_="label").get_text()
        players = [parse_player(el.get_text()) for el in match.find_all(class_="match-section")]
        rep[label] = players
    return rep


def load_and_parse(nb_players):
    with open(f'../local/scraps/{nb_players}.txt', 'r') as file:
        scraped = file.read()
    return parse(scraped)

final = {}

for nb_players in range(8, 65):
    print(f'Parsing #{nb_players}')
    final[nb_players] = load_and_parse(nb_players)

with open('../local/brackets.json', 'w') as file:
    file.write(json.dumps(final))