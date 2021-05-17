from flask import jsonify
import json
import matplotlib.pyplot as plt
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud, STOPWORDS
import os
from pymongo import MongoClient
from bson import json_util
from random import randint, shuffle

# connect to MongoDB
client = MongoClient("mongodb+srv://admin:octopus@29seconds.s8flw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=client["29seconds_db"]

def get_collections():
    collection_list = []
    collection = db.collection_names(include_system_collections=False)
    for collect in collection:
        collection_list.append(collect)
    return collection_list

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
    freq_dist = FreqDist(words_in_question)

    # remove {difficulty_lvl} most repeated words in question, add to removed list
    removed = []
    for i in range(difficulty_lvl):
        removed.append(freq_dist.pop(freq_dist.max()))
    temp_question = ''
    for word in freq_dist.keys():
        temp_question += f"{word} "
    question = temp_question

    # generate wordcloud using words in question
    wc_rand_state = randint(7, 9)
    wc = WordCloud(max_words=500,relative_scaling=0.5,
                  background_color='black',stopwords=STOPWORDS,
                  margin=2,random_state=wc_rand_state,contour_width=0.5,
                  contour_color='white', colormap='Accent')
    wc.generate(question)
    colors = wc.to_array()

    # prepare plot 
    # plt.ion()
    plt.figure()
    plt.title(f"Which {category} is this?\n", fontsize=20, color='black')
    plt.imshow(colors, interpolation="bilinear")
    plt.axis('off')
    # generate image name
    image = f"./static/{answer}{difficulty_lvl}.png"
    image = image.replace(" ","")
    # save plot as image else return existing image (same answer and difficulty level)
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
        if (random_choice != data_object["answer"]) and (random_choice not in choices):
            choices.append(random_choice)
    
    return choices