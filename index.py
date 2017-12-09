from flask import Flask, url_for, render_template, request
app = Flask(__name__)
app.debug = True

# url_for('static', filename='index.html')
@app.route('/')
def root():
	return render_template("index.html")

@app.route('/clinic')
def clinic():
	return render_template("clinic.html")

@app.route("/generate_voucher", methods=["POST"])
def generate_voucher():
	print request.form
	return "success"

def ccc_admin():
	return

def ride_austin_admin():
	return

