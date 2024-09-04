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
	cardsrow.clear()
	score_player.clear()
	return render_template('form.html', deck=deck)

@app.route('/new_cards/<deck>')
def draw_card(deck):
	all_info=json.loads(requests.get #запрос
	('https://deckofcardsapi.com/api/deck/'+deck+'/draw/?count=1').text)
	draw=all_info["cards"][0]["image"]
	rem =all_info['remaining'] #сколько карт осталось
	value=all_info["cards"][0]["value"] #вес карты
	if value=='JACK' or value=='QUEEN' or value=='KING': #условия для валет-король
		value=10
	elif value=='ACE':
		value=11	
	value=int(value)
	score_player.append(value)
	sum_score_player=sum(score_player)
	cardsrow.append(draw)
	if sum_score_player > 21:
		return render_template('form.html', draw=draw,deck=deck,cardsrow=cardsrow, rem=rem, 
		sum_score_player=sum_score_player, game_over=True)
	else:
		return render_template('form.html', draw=draw,deck=deck,cardsrow=cardsrow, rem=rem, 
		sum_score_player=sum_score_player, game_over=False)
		


# @app.route('&&&')


if __name__ == '__main__':
	app.run(debug=True)