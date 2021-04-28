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
import matplotlib.pyplot as plt
# from os import sys
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS

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
        data = json.load(f)
        random = randint(0,len(data)-1)
        data = data[random]
        # generate_image(data['question'], category, difficulty)
        return data

# def save_db():
#     with open('flashcards_db.json', 'w') as f:
#         return json.dump(db, f)

# Generates and stores a wordcloud from question
def generate_image(question, category, difficulty):

    # stop words ("and", "the", "we", etc.)
    stopwords= STOPWORDS

    # will need this for plotting too
    # Make list of words in the question. dont add word if its a stop word..
    words_in_question = [word for word in word_tokenize(question) if word not in stopwords]
    words_freq_dist = FreqDist(words_in_question)

    # remove x = {difficulty level} most repeated words, add to clues list
    # clues not yet working.. returns int of word counts instead of actual word
    clues = []
    for i in range(difficulty):
      clue = words_freq_dist.pop(words_freq_dist.max())
      clues.append(clue)
      
    # adjusted summary is summary without x most repeated words 
    adjusted_question = ''
    for word in words_freq_dist.keys():
      adjusted_question += word + ' '
    # generate wordcloud from adjusted question
    wc_rand_state = random.randint(7, 9)
    wc = WordCloud(max_words=500,relative_scaling=0.5,
                  background_color='black',stopwords=stopwords,
                  margin=2,random_state=wc_rand_state,contour_width=0.5,
                  contour_color='white', colormap='Accent')
    wc.generate(adjusted_summary)
    colors = wc.to_array()
    # plotting frequency distribution of words in summary synopsis.. not really needed. I just wanted to see..
    # words_freq_dist.plot(15, linestyle='-', title="LOL words")
    # plt.legend()

    # show wordcloud 
    plt.ion()
    plt.figure()
    plt.title(f"Which {category} is this?\n", fontsize=20, color='black')
    plt.imshow(colors, interpolation="bilinear")
    plt.axis('off')
    plt.show()
    plt.pause(0.001)
    # countdown timer
    self.countdown_timer(time_limit)
    plt.close(1)
    print("Time's up!")


    
