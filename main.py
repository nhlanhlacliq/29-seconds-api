from flask import Flask, render_template, abort, url_for, request, redirect
from model import read_random, read_all, create, get_collections
from wiki_api import WikiPage

app = Flask(__name__)

categories = get_collections()

@app.route('/')
def index():
    return redirect(url_for('api'))

@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        category = request.form['category']
        difficulty = request.form['difficulty']
        url_root = request.url_root
        response = read_random(category, difficulty, url_root)
        return response
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
                return redirect(url_for('confirm',category=category, title=title, plot=plot[:2750]))
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
            create(category, title, plot)
            return "ADDED TO DATABASE"
        else: 
            return redirect(url_for('add'))
    else:
        return render_template('confirm.html', title=title, plot=plot)

# view one catergory
@app.route('/api/view/<category>')
def view(category):
    return read_all(categories=[category])

# view all categories
@app.route('/api/view')
def view_all():
    return read_all(categories=categories)