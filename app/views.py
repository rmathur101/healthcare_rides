from flask import Flask, url_for, render_template, request

from app import app

@app.route('/')
def root():
	return render_template("index.html")

@app.route('/clinic')
def clinic():
	return render_template("clinic.html")

@app.route('/dashboard')
def dashboard():
	return render_template("dashboard.html")

# @app.route("/generate_voucher", methods=["POST"])
# def generate_voucher():
# 	print request.form
# 	return "success"

@app.route("/check_in_voucher", methods=["POST"])
def check_in_voucher():
	print request.form
	return "success"

def ccc_admin():
	return

def ride_austin_admin():
	return

