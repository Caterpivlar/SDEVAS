from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
import random
def new_game():
    usercount = 0
    dilercount = 0
    cards = [6,7,8,9,10,2,3,4,11] * 4
	random.shuffle(cards)
def draw_card():
    currentcard = cards.pop() #тащим последний элемент списка - карту
    print('Ваша карта', current)
def test():
	result='Test OK'
	return result

if __name__ == '__main__':
	app.run(debug=True)