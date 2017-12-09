from flask import Flask, url_for, render_template
app = Flask(__name__)

# url_for('static', filename='index.html')
@app.route('/')
def root():
	return render_template("index.html")
