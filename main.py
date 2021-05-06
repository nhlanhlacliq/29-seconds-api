from flask import Flask, render_template, abort, url_for, jsonify, request, redirect
from model import load_db, view_db, update_db
from wiki_api import WikiPage

app = Flask(__name__)
categories = ['anime']

@app.route('/')
def index():
    return redirect(url_for('api'))

@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        category = request.form['category']
        difficulty = request.form['difficulty']
        url_root = request.url_root
        response = load_db(category, difficulty, url_root)
        return jsonify(response)
    else:
        return render_template('api.html', categories=categories)

@app.route('/api/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # call wiki API
        query = request.form['question']
        category = request.form['category']
        try:
            query_page = WikiPage(query)
            if query_page.has_page:
                # success
                title, plot = query_page.get_data()
                return redirect(url_for('confirm',category=category, title=title, plot=plot))
            # failure
            return f"ERROR: '{query}' Not found on wikipedia."
        except IndexError:
            return f"ERROR: '{query}' Not found on wikipedia."

    else:
        return render_template('add.html', categories=categories)

@app.route('/api/add/confirm/<category>/<title>/<plot>', methods=['GET', 'POST'])
def confirm(category, title, plot):
    if request.method == 'POST':
        if request.form.getlist('button')[0] == 'yes':
            update_db(category, title, plot)
            return "ADDED TO DATABASE"
        else: 
            return redirect(url_for('add'))
    else:
        return render_template('confirm.html', title=title, plot=plot)


@app.route('/api/view')
def view():
    return jsonify(view_db(categories=categories))

