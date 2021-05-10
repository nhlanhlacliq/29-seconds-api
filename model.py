import json
from random import randint, shuffle
from flask import url_for, jsonify
import matplotlib.pyplot as plt
import time
import os
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud, STOPWORDS
from pymongo import MongoClient
from bson import json_util

# connect to MongoDB
client = MongoClient("mongodb+srv://admin:octopus@29seconds.s8flw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=client["anime_db"]

# return random entry from database
def read_random(category, difficulty_lvl, page_url):
    database = []
    collection=db[category]
    results = collection.find()
    for result in results:
        database.append(result)
    # choose random selection from data
    shuffle(database)
    data_object = database[randint(0,len(database)-1)]
    data_object["category"] = category
    data_object["choices"] = add_choices(data_object)
    data_object["image"] = generate_image(data_object, difficulty_lvl, page_url)
    return jsonify(json.loads(json_util.dumps(data_object)))

# insert new data to mongo db
def create(category, answer, question):
    data_object = {"question":question,
            "answer":answer}
    # if it already exists, exit function. else insert into db.
    collection=db[category]
    results = collection.find(data_object)
    for result in results:
        if result["answer"] == answer:
            return
    return collection.insert_one(data_object)        

# Return data from mongo db
def read_all(categories):
    database = []
    for category in categories:
        collection=db[category]
        results = collection.find()
        for result in results:
            database.append(result)
    return jsonify(json.loads(json_util.dumps(database)))

# Generates and store wordcloud image from question. returns image url
def generate_image(data_object, difficulty_lvl, page_url):
    answer = data_object["answer"]
    question = data_object["question"]
    category = data_object["category"]
    difficulty_lvl = int(difficulty_lvl)

    # Make list of words in the question excluding stop words.
    words_in_question = [word for word in word_tokenize(question) if word not in STOPWORDS]
    words_freq_dist = FreqDist(words_in_question)

    # remove x = {difficulty_lvl level} most repeated words, add to clues list
    for i in range(difficulty_lvl):
        words_freq_dist.pop(words_freq_dist.max())
      
    # create string without x most repeated words 
    adjusted_question = ''
    for word in words_freq_dist.keys():
        adjusted_question += word + ' '

    # generate wordcloud from adjusted question
    wc_rand_state = randint(7, 9)
    wc = WordCloud(max_words=500,relative_scaling=0.5,
                  background_color='black',stopwords=STOPWORDS,
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

    image = f"./static/{answer}{difficulty_lvl}.png".replace(" ","")
    image = image.replace(" ","")
    # save image else return existing image of the same answer and difficulty level
    if not os.path.exists(image):
        plt.savefig(image, dpi=300, bbox_inches='tight')
    url = page_url + image[2:]

    return url

# Add other answers within same category
def add_choices(data_object):
    choices = []
    database = []
    collection=db[data_object["category"]]
    results = collection.find()
    for result in results:
        database.append(result["answer"])
    shuffle(database)    
    while len(choices) < 3:
        random_choice = database[randint(0,len(database)-1)]
        if (random_choice != data["answer"]) and (random_choice not in choices):
            choices.append(random_choice)
    
    return choices