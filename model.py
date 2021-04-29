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
from random import randint
from flask import url_for
import matplotlib.pyplot as plt
import time
import os
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud, STOPWORDS

def load_db(category, difficulty):
    with open(f'{category}_db.json') as f:
        # lst = [item for item in f]
        data = json.load(f)
        # choose random selection from data
        data = data[randint(0,len(data)-1)]
        data["category"] = category
        data["choices"] = add_choices(data)
        data["image_url"] = generate_image(data, difficulty)
        return data

# def save_db():
#     with open('flashcards_db.json', 'w') as f:
#         return json.dump(db, f)

# Generates and stores a wordcloud from question
def generate_image(data, difficulty):
    answer = data["answer"]
    question = data["question"]
    category = data["category"]
    difficulty = int(difficulty)

    # stop words ("and", "the", "we", etc.)
    stopwords= STOPWORDS

    # Make list of words in the question. dont add word if its a stop word..
    words_in_question = [word for word in word_tokenize(question) if word not in stopwords]
    words_freq_dist = FreqDist(words_in_question)

    # remove x = {difficulty level} most repeated words, add to clues list
    # clues not yet working.. returns int of word counts instead of actual word
    clues = []
    for i in range(difficulty):
      clue = words_freq_dist.pop(words_freq_dist.max())
      clues.append(clue)
      
    # adjusted question is question without x most repeated words 
    adjusted_question = ''
    for word in words_freq_dist.keys():
      adjusted_question += word + ' '

    # generate wordcloud from adjusted question
    wc_rand_state = randint(7, 9)
    wc = WordCloud(max_words=500,relative_scaling=0.5,
                  background_color='black',stopwords=stopwords,
                  margin=2,random_state=wc_rand_state,contour_width=0.5,
                  contour_color='white', colormap='Accent')
    wc.generate(adjusted_question)
    colors = wc.to_array()
    # plotting frequency distribution of words in question.. Uncomment to verify..
    # words_freq_dist.plot(15, linestyle='-', title="FreqDist of words")
    # plt.legend()

    # save wordcloud image, return link 
    plt.ion()
    plt.figure()
    plt.title(f"Which {category} is this?\n", fontsize=20, color='black')
    plt.imshow(colors, interpolation="bilinear")
    plt.axis('off')

    filename = f"./static/{answer}{difficulty}.png"
    # save image else return existing one if it already exists
    if not os.path.exists(filename):
        plt.savefig(filename, dpi=300, bbox_inches='tight')

    return filename[1:]

# Add other answers within same category
def add_choices(data):
    category = data["category"]

    choices = []
    with open(f'{category}_db.json') as f:
      db = json.load(f)
      while len(choices) <= 3:
        random_choice = db[randint(0,len(db)-1)]["answer"]
        if (random_choice != data["answer"]) and (random_choice not in choices):
          choices.append(random_choice)
    
    return choices
    
