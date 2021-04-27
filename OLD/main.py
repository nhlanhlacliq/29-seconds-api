from website import create_app
from website.difficulty import Difficulty as diff
from website.score import Score as score
from website.database import Database as db
from website.datalist import DataList as DataList
from website import views
from flask import Flask, render_template, request, url_for, Response, redirect, flash


app = create_app()

level = 0
time = 0

@app.route('/difficulty-mode/<int:difficulty_mode>')
def difficulty_mode(difficulty_mode):
    # dm is 'Difficulty mode'
    dm = diff(difficulty_mode)
    global level 
    global time
    level = dm.get_difficulty()
    time = dm.get_time_limit()
    
    return redirect('/category')

@app.route('/category')
def category_select():
    flash(f"Just to see {time} and {level}.. This is hard 😭😭")
    return redirect(url_for(views.category))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port = 8080, debug=True)