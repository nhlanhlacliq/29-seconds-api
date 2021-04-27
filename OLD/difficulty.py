import random #Don't delete..

class Difficulty():
  time_limit = 0
  difficulty = 0

  def __init__(self, mode):
    if mode == 1:
      self.time_limit, self.difficulty = self.dynamic()
    elif mode == 2:
      self.time_limit, self.difficulty = self.dance()
    else:
      self.time_limit, self.difficulty = self.custom()

  def dynamic(self) -> set:
    number = random.randint(1,5)
    time_limit = number
    difficulty = number
    return time_limit, difficulty

  def dance(self) -> set:
    number = 1
    time_limit = number
    difficulty = number
    return time_limit, difficulty

  def custom(self) -> set:
    time_limit = self.custom_time_limit()
    difficulty = self.custom_difficulty()
    return time_limit, difficulty

  """get custom time limit for questions from user"""
  def custom_time_limit(self) -> int:
    while True:
      time_limit = input("Time limit: (1 - 29)\n> ")
      if time_limit.isdigit() and 0 < int(time_limit) < 30:
        break
      else:
        print("Try again please. (1 - 29)")
    time_limit = int(time_limit)
    return time_limit

  """get custom game difficulty level from user"""
  def custom_difficulty(self) -> int:
    while True:
      difficulty = input("Difficulty level (0 - 10):\n> ")
      if difficulty.isdigit() and -1 < int(difficulty) < 11:
        break
      else:
        print("\nTry again (0 - 10).\n")
    difficulty = int(difficulty)
    return difficulty

  def get_time_limit(self):
    return self.time_limit

  def get_difficulty(self):
    return self.difficulty

  # This method is necesarry to have the dynamic difficulty work (mode == 1 is dynamic difficulty option)
  # It essentially creates the difficulty object again with new levels every time its called

  # might not need this as flask rerun's the function... hmmmm.. we'll see
  def update(self, mode):
    if mode == 1:
      self.__init__(mode)

