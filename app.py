from flask import Flask, render_template, session
 
from flask_session import Session

import json
import requests
cardsrow = []
dealer_cards = []
score_player=[]
score_dealer=[]
app = Flask(__name__)

app.config['SECRET_KEY'] = 'biocad'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_THRESHOLD'] = 500

Session(app)

@app.route('/')
def start():
	return render_template('index.html')

@app.route('/form/')
def get_deck():
	cardsrow.clear()
	score_player.clear()
	dealer_cards.clear()
	score_dealer.clear()
	deck_id = json.loads(requests.post
	('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1').text)["deck_id"]
	session['deck_id'] = deck_id
	return render_template('form.html', deck_id=deck_id)

@app.route('/new_cards')
def draw_card():
	deck_id=session.get('deck_id')
	
	if cardsrow == []: # определение перерменной для вытягивания карт
		ctd = 2
	else:
		ctd = 1
	i=0
	
	all_info = json.loads(requests.get #запрос
	('https://deckofcardsapi.com/api/deck/'+deck_id+'/draw/?count='+str(ctd)).text)
	session['all_info'] = all_info
	all_info = session.get('all_info')
	#session['all_info'].insert(0, all_info)
	
	for i in range(ctd): # Цикл для вытягивания 1 или 2 карт в зависимости от необходимости (кол-во ctd)
		
		#session.get('all_info')
		
		draw = all_info["cards"][i]["image"]
		#draw = session['all_info']["cards"][i]["image"]   #картинка карты 1
		rem = all_info['remaining'] #сколько карт осталось
		value = all_info["cards"][i]["value"] #вес карты
		
		if value =='JACK' or value == 'QUEEN' or value == 'KING': #условия для валет-туз
			value = 10
		elif value == 'ACE':
			value = 11
		
		value = int(value)
		
		score_player.append(value) #включение в список значения карты
		sum_score_player = sum(score_player) #сумма списка
		cardsrow.insert(0, draw) #включение картинки в список
		i=i+1
	
	if sum_score_player > 21: #условия проигрыша
		message = "Ты проиграл, лох"
		return render_template('form.html', draw=draw, cardsrow=cardsrow, rem=rem, 
                           sum_score_player=sum_score_player,message=message,
                           game_over=True, loser=True, deck_id=deck_id)
	else:
		return render_template('form.html', draw=draw,cardsrow=cardsrow, rem=rem, 
		sum_score_player=sum_score_player, game_over=False, deck_id=deck_id)


@app.route('/dealer/<deck>')
def dealer(deck):
	while sum(score_dealer) <= 17: 
		all_info = json.loads(requests.get #запрос
	('https://deckofcardsapi.com/api/deck/'+deck+'/draw/?count=1').text)
		draw = all_info["cards"][0]["image"] #картинка карты
		rem = all_info['remaining'] #сколько карт осталось
		value = all_info["cards"][0]["value"] #вес карты
		if value == 'JACK' or value == 'QUEEN' or value == 'KING': #условия для валет-туз
			value = 10
		elif value == 'ACE':
			value = 11	
		value=int(value)
		score_dealer.append(value)
		dealer_cards.insert(0, draw)
		
	sum_score_dealer = sum(score_dealer)
	sum_score_player = sum(score_player)
	if sum_score_player > 21 or (sum_score_player <= sum_score_dealer and sum_score_dealer <= 21):
		message = "Ты проиграл, лох"
		return render_template('form.html', draw=draw, deck=deck, cardsrow=cardsrow, rem=rem, 
                           sum_score_player=sum_score_player, sum_score_dealer=sum_score_dealer, 
                           game_over=True, dealer_cards=dealer_cards, message=message, loser=True)
	elif sum_score_dealer > 21 or sum_score_dealer < sum_score_player:
		message = "Дилер лох! Ты победил!"
		return render_template('form.html', draw=draw, deck=deck, cardsrow=cardsrow, rem=rem, 
                           sum_score_player=sum_score_player, sum_score_dealer=sum_score_dealer, 
                           game_over=True, dealer_cards=dealer_cards, message=message, winner=True)


# @app.route('&&&')


if __name__ == '__main__':
	app.run(debug=True)