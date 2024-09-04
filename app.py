from flask import Flask, render_template
import json
import requests
cardsrow = []
dealer_cards = []
score_player=[]
score_dealer=[]
app = Flask(__name__)

@app.route('/')
def start():
	return render_template('index.html')

@app.route('/form/')
def get_deck():
	deck = json.loads(requests.post
	('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1').text)["deck_id"]
	cardsrow.clear()
	score_player.clear()
	dealer_cards.clear()
	score_dealer.clear()
	return render_template('form.html', deck=deck)

@app.route('/new_cards/<deck>')
def draw_card(deck):
	all_info=json.loads(requests.get #запрос
	('https://deckofcardsapi.com/api/deck/'+deck+'/draw/?count=1').text)
	draw = all_info["cards"][0]["image"] #картинка карты
	rem = all_info['remaining'] #сколько карт осталось
	value = all_info["cards"][0]["value"] #вес карты
	if value =='JACK' or value == 'QUEEN' or value == 'KING': #условия для валет-туз
		value = 10
	elif value == 'ACE':
		value = 11	
	value = int(value)  
	score_player.append(value) #включение в список значения карты
	sum_score_player = sum(score_player) #сумма списка
	cardsrow.append(draw) #включение картинки в список
	if sum_score_player > 21: #условия проигрыша
		return render_template('form.html', draw=draw,deck=deck,cardsrow=cardsrow, rem=rem, 
		sum_score_player=sum_score_player, game_over=True)
	else:
		return render_template('form.html', draw=draw,deck=deck,cardsrow=cardsrow, rem=rem, 
		sum_score_player=sum_score_player, game_over=False)

@app.route('/dealer/<deck>')
def dealer(deck):
	while sum(score_dealer) <= 17: 
		all_info = json.loads(requests.get #запрос
	('https://deckofcardsapi.com/api/deck/'+deck+'/draw/?count=1').text)
		draw = all_info["cards"][0]["image"] #картинка карты
		rem = all_info['remaining'] #сколько карт осталось
		value = all_info["cards"][0]["value"] #вес карты
		if value=='JACK' or value=='QUEEN' or value=='KING': #условия для валет-туз
			value=10
		elif value=='ACE':
			value=11	
		value=int(value)
		score_dealer.append(value)
		dealer_cards.append(draw)
		
	sum_score_dealer=sum(score_dealer)
	sum_score_player=sum(score_player)
	if sum_score_player > 21:
		message = "Ты проиграл, лох"
	elif sum_score_dealer > 21:
		message = "Дилер лох! Ты победил!"
	elif sum_score_player > sum_score_dealer:
		message = "Ты победил!"
	elif sum_score_player < sum_score_dealer:
		message = "Дилер победил!"
	else:
		message = "Ничья!"
	return render_template('form.html', draw=draw, deck=deck, cardsrow=cardsrow, rem=rem, 
                           sum_score_player=sum_score_player, sum_score_dealer=sum_score_dealer, 
                           game_over=True, dealer_cards=dealer_cards, message=message)


# @app.route('&&&')


if __name__ == '__main__':
	app.run(debug=True)