# HANGMAN
import random
import time
from enum import Enum

class GameStatus(Enum):
  STARTED = 0
  WON = 1
  KEEP_PLAYING = 2
  LOST = 3

class ScoreStatus(Enum):
  NOT_BAD = 0
  GOOD = 1 
  GREAT = 2 
  
  
    


class HangmanGameCore(object):

  ## constants
  secret_word = ["3dhubs", "marvin", "print", "filament", "order", "layer"]

  ## data members
  
  already_guessed = []
  limit = 5 ## limit of failures (attempts)
  failed_count  = 0
  word_length   = 0
  highest_score = 0
  play_again   = "y"
  word_display = ""
  word         = ""

  """docstring for HangmanGame"""
  def __init__(self):
    super(HangmanGameCore, self).__init__()

  def start_game(self):
      self.game_state = GameStatus.STARTED
      self.word = random.choice(self.secret_word)
      self.word_length = len(self.word)
      self.failed_count = 0
      self.word_display = '*' * self.word_length
      self.already_guessed = []
      self.play_again = ""
      self.run_hangman_game()

  def manage_highest_score(self, current_word_length, current_failed_count):
    """Showing the score compare to the highest record"""
    result_msg = ""
    current_score = ((current_word_length - current_failed_count) * 100)
    highest_score = self.highest_score
    if highest_score < current_score:
      self.score_state = ScoreStatus.GREAT
      result_msg = "WoOoOoW! You have broken the highest record, The new highest score is: " + str(current_score) + "\n"
      self.highest_score = current_score
    elif highest_score == current_score:
      self.score_state = ScoreStatus.Good
      result_msg = "Good job, You have reached the highest score " + str(current_score) + "\n"
      self.highest_score = current_score        
    else:
      self.score_state = ScoreStatus.NOT_BAD
      result_msg  = "Well, Your score is: "+  str(current_score) + ". It's not the best, where the highest score is: "+  str(highest_score) + "\n"
      result_msg += "YOU CAN DO IT, Don't give up and Play again ;) \n" 
    return result_msg
      
  def get_indexes(self, string, char):
      return [i for i, ltr in enumerate(string) if ltr == char]

  # ## Needes to be overrided to define the way of drawing
  def draw_hangman(self):
    pass

  # ## Needes to be overrided to add the input 
  def run_hangman_game(self):
    pass  

  # #### Hangman status possibilities ####
  # ## Needes to be overrided to show 
  def unvalid_input(self):
      pass

  def match_guess(self, guess):
      self.already_guessed.extend([guess])
      indexes = self.get_indexes(self.word, guess)
      for index in indexes:
        self.word = self.word[:index] + "*" + self.word[index + 1:]
        self.word_display = self.word_display[:index] + guess + self.word_display[index + 1:]
        pass
      msg = self.word_display + "\n"
      return msg

  def wrong_guess(self):
     self.failed_count += 1
     self.draw_hangman()
  #### End Hangman possibility ####

  def hangman_contoller(self, guessed_input):
    guess = guessed_input.strip()
    msg = ""
    if len(guess) == 0 or len(guess) >= 2:
      self.unvalid_input()

    elif guess in self.word:
      msg += self.match_guess(guess)
      self.game_state =  GameStatus.KEEP_PLAYING
  
    elif guess in self.already_guessed:
      msg += "Input already guessed, try DIFFERENT input!\n"

    else:
        self.wrong_guess()
        self.game_state =  GameStatus.LOST
    return msg

