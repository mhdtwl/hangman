# HANGMAN UI
import time
from hangman_game_core import HangmanGameCore 


class HangmanGameUI(HangmanGameCore):

  
  def __init__(self):
    super(HangmanGameUI, self).__init__()
    name = input("What is your name: ")
    print("Welcome " + name + "! Good Luck..." + "\n")
    time.sleep(1)

  def manage_highest_score(self, current_word_length, current_failed_count):
      return super(HangmanGameUI,self).manage_highest_score(current_word_length, current_failed_count)

  def again_play(self):
      self.play_again = input("Do You want to play again? ( y | n )  \n")
      
      while self.play_again not in ["y", "n"]:
          self.play_again = input("Do You want to play again? ( y | n )  \n")

      if self.play_again == "y":
        self.start_game()
      else:
        exit()

  ## Override parent's function        
  def unvalid_input(self):
      guess = input("This is Word: " + self.word_display + " Enter your guess: \n")
      print ("Enter a single LETTER or DIGIT only\n")
      self.hangman_contoller(guess)

  ## Override parent's function
  def draw_hangman(self):
      self.draw_ui_hangman(self.failed_count)

  def draw_ui_hangman(self, failed_count):
      if self.failed_count == 1:
                print("Wrong input. " + str(self.limit - self.failed_count) + " guess remaining\n")
                print("   _____ \n"
                      "  |      \n"
                      "  |      \n"
                      "  |      \n"
                      "  |      \n"
                      "  |      \n"
                      "  |      \n"
                      "__|__\n")

      elif self.failed_count == 2:
            print("Wrong input. " + str(self.limit - self.failed_count) + " guess remaining\n")
            print("   _____ \n"
                  "  |     | \n"
                "  |     |\n"
                "  |     | \n"
                "  |      \n"
                "  |      \n"
                "  |      \n"
                "__|__\n")
      
      elif self.failed_count == 3:
        print("Wrong input. " + str(self.limit - self.failed_count) + " guess remaining\n")
        print("   _____ \n"
              "  |     | \n"
              "  |     |\n"
              "  |     | \n"
              "  |     O \n"
              "  |      \n"
              "  |      \n"
              "__|__\n")            

      elif self.failed_count == 4:
        print("Wrong input. " + str(self.limit - self.failed_count) + " guess remaining\n")
        print("   _____ \n"
              "  |     | \n"
              "  |     |\n"
              "  |     | \n"
              "  |     O \n"
              "  |    /|\ \n"
              "  |      \n"
              "__|__\n")  

      elif self.failed_count == 5:
          print("Wrong input. You are hanged\n")
          print("   _____ \n"
                "  |     | \n"
                "  |     |\n"
                "  |     | \n"
                "  |     O \n"
                "  |    /|\ \n"
                "  |    / \ \n"
                "__|__\n")
          self.again_play()

  def validate_game_state(self):
      if self.word == '*' * self.word_length:
        print("Congrats! You have guessed it successfully...")
        print( self.manage_highest_score(self.word_length, self.failed_count) )
        self.again_play()

      elif self.failed_count != self.limit:
        self.run_hangman_game()
  
  def run_hangman_game(self):
   
    
    guess = input("This is Word: " + self.word_display + " Enter your guess: \n")
    result_msg = self.hangman_contoller(guess)
    print(result_msg)
    self.validate_game_state()
