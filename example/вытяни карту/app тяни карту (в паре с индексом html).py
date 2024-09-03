from flask import Flask, render_template
import json
import requests
app = Flask(__name__)
@app.route('/')
def get_deck():
    deck = json.loads(requests.post
	('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1').text)["deck_id"]
    return render_template('index.html', deck=deck)

@app.route('/draw/<deck>')
def draw_card(deck):
    draw = json.loads(requests.get
	('https://deckofcardsapi.com/api/deck/'+deck+'/draw/?count=2').text)["cards"][0]["image"]
    return render_template('index.html', draw=draw,deck=deck)
	
if __name__ == '__main__':
	app.run(debug=True)