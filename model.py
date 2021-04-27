"""
model.py
--------
Implements the model for our website by simulating a database.

Note: although this is nice as a simple example, don't do this in a real-world
production setting. Having a global object for application data is asking for
trouble. Instead, use a real database layer, like
https://flask-sqlalchemy.palletsprojects.com/.
"""
import json

def db(category, difficulty):
    # get category, question, answer 
    db = {}
    db["category"] = category
    db["question"] = QnA(category)[0]
    db["answer"] = QnA(category)[1]
    db["image"] = QnA(category)[2]

def QnA(category):
    pass
    # 0: Question

def load_db(category, difficulty):
    with open(f'{category}_db.json') as f:
        # lst = [item for item in f]
        print(f[0])
        return json.load(f)

# def save_db():
#     with open('flashcards_db.json', 'w') as f:
#         return json.dump(db, f)




    
