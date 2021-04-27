from flask import Flask, render_template, abort, url_for, jsonify, request, redirect
from model import load_db

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('api'))

@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        difficulty = request.form['difficulty']
        category = request.form['category']
        response = load_db(category, difficulty)
        return jsonify(response)
    else:
        return render_template('api.html')
