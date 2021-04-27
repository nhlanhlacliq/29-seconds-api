def db(category, difficulty):
    # get category, question, answer 
    db = {}
    db["category"] = category
    db["question"] = QnA(category)[0]
    db["answer"] = QnA(category)[1]
    db["image"] = QnA(category)[2]

def QnA(category):
    # 0: Question
    pass


    
