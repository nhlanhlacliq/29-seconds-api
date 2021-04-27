class Score:
  def __init__(self):
    self.value = 0

  def add_point(self):
    self.value += 1
  
  def get_score(self):
    return int(self.value)
