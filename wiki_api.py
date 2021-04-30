from wikipediaapi import Wikipedia
import matplotlib.pyplot as plt
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud, STOPWORDS
from random import randint

search = input("Search query:\n> ")

wiki = Wikipedia('en')
page_py = wiki.page(search)
print("Page - Exists: %s" % page_py.exists())
# print("Page - Title: %s" % page_py.title)
print("Page - Summary: %s" % page_py.sections[0])


def print_sections(sections, level=0):
    data = ''
    for s in sections:
        print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:40]))
        print_sections(s.sections, level + 1)
    return data

def print_summary(sections, level=0):
    data = ''
    # for s in sections:
    #     print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:40]))
    #     continue
    print(sections[0])

    return data

# print_sections(page_py.sections)
print_summary(page_py.sections)

# Generates and stores a wordcloud from question
def generate_image(question, difficulty, category="xxxx"):
    difficulty = int(difficulty)

    # stop words ("and", "the", "we", etc.)
    stops= ["Section","Plot","Subsections"]
    stopwords= STOPWORDS + stops

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

    # time_stamp = time.time()
    # filename = f"./static/{answer}.png"
    # save image else return existing one if it already exists
    # if not os.path.exists(filename):
    plt.savefig('test', dpi=300, bbox_inches='tight')

    # plt.show()
    # return filename[1:]


# print(question)
# generate_image(question, 1)
# replace('\\n','')