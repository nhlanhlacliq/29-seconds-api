import matplotlib.pyplot as plt
from time import sleep
from os import sys
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS
import random
import string
from difficulty import Difficulty
from database import Database
from summary import Summary
from score import Score

class Game():
  """Countdown timer"""
  def countdown_timer(self, time):
    for i in range(time):
      print(time - i)
      sleep(1)

  """Generates and shows a wordcloud from a chosen category. 
  The summary contains the synopsis which the WC is generated from"""
  def show_wordcloud(self, summary_object, difficulty_object):
    # get time limit and difficulty level from difficulty object
    time_limit = difficulty_object.get_time_limit()
    difficulty_level = difficulty_object.get_difficulty()

    # get category and summary from summary object
    category = summary_object.get_category()
    summary = summary_object.get_summary()

    # stop words ("and", "the", "we", etc.)
    stops = set(stopwords.words('english')) #Set used for speed
    more_stops= STOPWORDS

    # will need this for plotting too
    # Make list of words in the summary. dont add word if its a stop word..
    words_in_summary = [word for word in word_tokenize(summary) if ((word not in stops) and (word not in more_stops))]
    words_freq_dist = FreqDist(words_in_summary)

    # remove x = {difficulty level} most repeated words, add to clues list
    # clues not yet working.. returns int of word counts instead of actual word
    clues = []
    for i in range(difficulty_level):
      clue = words_freq_dist.pop(words_freq_dist.max())
      clues.append(clue)
      
    # print(f"These would be the clues {clues}")
    # adjusted summary is summary without x most repeated words 
    adjusted_summary = ''
    for word in words_freq_dist.keys():
      adjusted_summary += word + ' '
    # generate wordcloud from adjusted summary
    wc_rand_state = random.randint(7, 9)
    wc = WordCloud(max_words=500,relative_scaling=0.5,
                  background_color='black',stopwords=more_stops,
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

  """Displays questions. Actual answer, mixed with random questions from same category"""
  def display_questions(self, summary_object):
    category = summary_object.get_category()
    answer = summary_object.get_answer()
    # getattr essentially calls the method using the category(they have the same name)
    category_list = getattr(Database, category)
    category_list = category_list()
    category_list = list(category_list.keys()) 
    # add actual answer to questions. add 3 random questions from category
    questions = []
    questions.append(answer)
    while len(questions) < 4:
      random_question = random.choice(category_list)
      if random_question not in questions:
        questions.append(random_question)
    # shuffle questions list. create dictionary representing number : question 
    random.shuffle(questions)
    questions_menu = {}
    for i in range(1, len(questions) + 1):
      questions_menu[i] = questions.pop() 
    # display question menu
    print()
    for question_num, question_name in questions_menu.items():
      print(f"{question_num}: {string.capwords(question_name)}")

    return questions_menu

  """Gets and checks user answer to actual answer. updates score/ ends game if wrong"""
  def check_answer(self, questions_menu, summary_object, score_object):
    while True:
      user_answer = input("\n> ")
      if user_answer.isdigit() and 0 < int(user_answer) < len(questions_menu) + 1:
        break
      else:
        print("\nTry again\n")
    category = summary_object.get_category()
    answer = summary_object.get_answer()
    # if correct, add point
    if questions_menu[int(user_answer)] == answer:
      print("Hmm..")
      sleep(1)
      print("CORRECTO!")
      score_object.add_point()
      if category == 'book':
        score_object.add_point()
    # if wrong, end game. display score
    else:
      print("Hmm..")
      sleep(2)
      # print(f"Correct answer: {string.capwords(actual_answer)}")
      print("Game over")
      print(f"Score: {score_object.get_score()}")
      sys.exit(1)

  """Get difficulty mode from user. Modes are just combinations of different time limits and difficulty levels."""
  def get_difficulty_mode(self) -> int:
    print("Choose Difficulty: \n")
    while True:
      difficulty_mode = input("1. Dynamic Difficulty - All's fair in love and war. \n2. Easy but Hard - Let's Dance. \n3. Custom Difficulty.\n> ")
      if difficulty_mode.isdigit() and 0 < int(difficulty_mode) < 4:
        break
      else:
        print("\nIncorrect input (1 - 3).\n")
    difficulty_mode = int(difficulty_mode)
    return difficulty_mode

  """Adding a new show"""
  def add_show(self):
    while True:
      databaselist = [category for category in dir(Database) if not category.startswith("__")]
      category_choices = {}
      print("Category to add in:\n")
      for i, category in enumerate(databaselist):
        print(f"{i+1}. {category.upper()}")
        category_choices[i+1] = category

      choice = input("\n> ")
      if choice.isdigit() and 0 < int(choice) < i+1:
        break
      else:   
        print("\nIncorrect input\n")

      choice = int(choice)
      chosen_category = category_choices[choice]
      name = input(f"Enter {chosen_category} name:\n> ")
      desc = input(f"Enter {name}'s summary/plot:\n> ")
      print(chosen_category)

      category = getattr(Database, chosen_category)
      category_dict = category()

      #   chosen_category = setattr(chosen_category, category_dict[name], desc)
      category_dict[name] = desc
      print(f"{name} added!")
      return self.main_menu()

  """main menu. shown first"""
  def main_menu(self):
    while True:
      print("1. Play \n2. Add new show\n")
      choice = input("> ")
      if choice.isdigit() and 0 < int(choice) < 3:
        break
      else:
        print("Invalid Input")
    choice = int(choice)
    print(choice)
    if choice == 1:
      return
    elif choice == 2:
      return self.add_show()

  """main method"""
  def main(self, difficulty_object, score_object):
    # get category, summary and answer from summary object
    summary_object = Summary()
    
    # show word cloud of summary, adjust by difficulty
    self.show_wordcloud(summary_object, difficulty_object)

    # show questions, get and check answer
    questions_menu = self.display_questions(summary_object)
    self.check_answer(questions_menu, summary_object, score_object)
    print(f"Score: {score_object.get_score()}")

  """game loop"""
  def run(self):
    self.main_menu()
    mode = self.get_difficulty_mode()
    difficulty_object = Difficulty(mode)
    score_object = Score()
    while True:
      difficulty_object.update(mode)
      self.main(difficulty_object, score_object)


if __name__ == '__main__':
  game = Game()
  game.run()