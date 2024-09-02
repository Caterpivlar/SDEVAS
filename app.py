from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def start():
	return render_template('index.html',result='Карт нет')
	
@app.route('/draw')
def test():
	result='Test OK'
	return render_template('index.html',result=result)
if __name__ == '__main__':
	app.run(debug=True)