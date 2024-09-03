# табуляция пробелами!!!!!
from flask import Flask, render_template
import json
import requests
cardsrow = []
score_player=[]
app = Flask(__name__)
@app.route('/')

def start():
    cardsrow.clear()
    score_player.clear()
    return render_template('index.html')

@app.route('/form/')
def get_deck():
    deck = json.loads(requests.post
	('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1').text)["deck_id"]
    return render_template('form.html', deck=deck)

@app.route('/new_cards/<deck>')

def draw_card(deck):
    all_info=json.loads(requests.get
	('https://deckofcardsapi.com/api/deck/'+deck+'/draw/?count=1').text)
    draw=all_info["cards"][0]["image"]
    rem =all_info['remaining']
    value=int(all_info["cards"][0]["value"]) #проблема value= валет, дама...это не int
	
#def draw_card(deck): (рабочий код)
#    draw = json.loads(requests.get
#	('https://deckofcardsapi.com/api/deck/'+deck+'/draw/?count=1').text)["cards"][0]["image"]
#    rem = json.loads(requests.get
#    ('https://deckofcardsapi.com/api/deck/'+deck+'/draw/?count=0').text)['remaining']
    score_player.append(value)
    sum_score_player=int(sum(score_player))
    cardsrow.append(draw)
    return render_template('form.html', draw=draw,deck=deck,cardsrow=cardsrow, rem=rem, sum_score_player=sum_score_player)

# @app.route('&&&')


if __name__ == '__main__':
	app.run(debug=True)