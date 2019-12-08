import json

# GET::  Start game OR Play again: 
# response :  create user + show  word _ _ _ _ 

# POST::  Guess a letter: 
# response : 
#   invalid :  show word + show message
#   match :    show updated word + msg 
#   mismatch: 
#     < 5 -> show word + msg + fail_counter 
#     = 5 -> mssg[ Game Over]

from flask import Flask, request
from hangman_game_api import HangmanGameAPI 

app = Flask(__name__)
game_api = HangmanGameAPI()

@app.route("/")
def lunch_new_game():
    return  game_api.lunch_game()  


@app.route('/user/<user_id>', methods = ['GET', 'POST'])
def user(user_id):
    if request.method == 'GET':
        """return the information for <user_id>"""
        return  game_api.get_user(user_id) 

    if request.method == 'POST':
      """modify/update the information for <user_id>"""
      req_data = request.get_json() ## { 'letter' : '$CHAR' }
      return  game_api.play_game(user_id, req_data ) 

if __name__ == '__main__':
     app.run(port='5000')
     