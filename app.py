from flask import Flask, render_template
import json
import requests
cardsrow = []
app = Flask(__name__)
@app.route('/')

def start():
    return render_template('index.html')

@app.route('/form/')
def get_deck():
    deck = json.loads(requests.post
	('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1').text)["deck_id"]
    return render_template('form.html', deck=deck)

@app.route('/new_cards/<deck>')
def draw_card(deck):
    draw = json.loads(requests.get
	('https://deckofcardsapi.com/api/deck/'+deck+'/draw/?count=1').text)["cards"][0]["image"]
    cardsrow.append(draw)
    return render_template('form.html', draw=draw,deck=deck,cardsrow=cardsrow)

# @app.route('&&&')


if __name__ == '__main__':
	app.run(debug=True)