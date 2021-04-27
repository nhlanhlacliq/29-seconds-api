from database import Database
import secrets
import random

class Summary():
    category = None
    summary = None
    answer = None

    def __init__(self):
        self.set_category()
        self.set_summary()


    def set_category(self):
        # List of categories created from the method names in the database file..
        databaselist = [category for category in dir(Database) if not category.startswith("__")]
        categories_menu = {}

        # Get user catagory choice
        while True:
            print("Choose category:\n")
            # enum through categories in database, build category menu and print category options
            for i, category in enumerate(databaselist):
                categories_menu[i+1] = category
                print(f"{i+1}: {category.upper()}")
            category_num = input("\n> ")

            if category_num.isdigit() and 0 < int(category_num) < max(categories_menu.keys())+1:
                break
            else:
                print("\nIncorrect input\n")

        category_num = int(category_num)
        self.category = categories_menu[category_num]

    def set_summary(self): 
        # getattr essentially calls the menthod using the chosen category(they have the same name)
        category = getattr(Database, self.get_category())
        category_dict = category()

        # get random summary from category... returns tuple.. ("naruto","initially set in konoha village what what")
        category_list = list(category_dict.items())
        random.shuffle(category_list)
        random_answer_summary_pair = secrets.choice(category_list)

        self.answer = random_answer_summary_pair[0]
        self.summary = random_answer_summary_pair[1]
  
    def get_category(self):
        return self.category

    def get_summary(self):
        return self.summary

    def get_answer(self):
        return self.answer
