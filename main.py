from flask import Flask, render_template, abort, url_for, jsonify, request, redirect
from model import load_db
from wiki_api import has_wiki_page

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('api'))

categories = ['anime']
@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        category = request.form['category']
        difficulty = request.form['difficulty']
        response = load_db(category, difficulty)
        return jsonify(response)
    else:
        return render_template('api.html', categories=categories)

@app.route('/api/add')
def add():
    if request.method == 'POST':
        # call wiki API
        query = request.form['question']
        category = request.form['category']
        pass
    else:
        return render_template('add.html', categories=categories)