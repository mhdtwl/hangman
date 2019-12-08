# HANGMAN /api
import random, string, json, os
from http import HTTPStatus
from hangman_game_core import HangmanGameCore 


class HangmanGameAPI(HangmanGameCore):

  def __init__(self):
    super(HangmanGameAPI, self).__init__()
    self.fname = 'data.txt'

  def manage_highest_score(self, current_word_length, current_failed_count):
    return super(HangmanGameAPI,self).manage_highest_score(current_word_length, current_failed_count)
 
  def randomString(self, stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_letters 
    return ''.join(random.choice(letters) for i in range(stringLength))

  ##########    Json data update   ##########
  def get_json_user_data(self, user_token):
      data =  {
      "word_to_guess"   :  self.word_display,
      "highest_score"   :  self.highest_score,
      "word_length"     :  self.word_length,
      "already_guessed" :  self.already_guessed,
      "failed_count"    :  self.failed_count,
      "word"            :  self.word,
      "user_token"      :  user_token}  
      return data

  def set_json_user_data(self, user_token, user_data):
      data = {
                    "word_to_guess" :  user_data["word_to_guess"],
                    "highest_score" :  user_data["highest_score"],
                    "word_length" : user_data["word_length"],
                    "already_guessed" : user_data["already_guessed"],
                    "failed_count" : user_data["failed_count"],
                    "word" : user_data["word"],
                    "user_token" : user_data["user_token"],
                  }  
      return data
  def fill_user_msg_data(self, user_data, user_token):
      """Update Global var"""
      self.msg_data = self.set_json_user_data(user_token, user_data)
      pass   

  ##########   Local  Files  Writing   ##########
  def add_user_data(self, json_file_path, user_entry, user_token, file_data):
        file_data[user_token] = user_entry
        with open(json_file_path, mode='w') as f:
          f.write(json.dumps(file_data, indent=2))
   
  def get_user_data(self, user_token):
    with open(self.fname, "r") as feedsjson:
         feeds = json.load(feedsjson)
    if user_token in feeds:
      return feeds[user_token]
    else:
      return {}

  def write_user_into_file(self,user_token):
      a = []
      file_data = { }
      fname = self.fname
      if not os.path.isfile(fname):  ## add to none-existed file
        self.add_user_data(fname, self.msg_data, user_token, file_data )
      else:
          with open(fname, "r") as feedsjson:
              feeds = json.load(feedsjson)
          if user_token in  feeds: ## update data
              self.update_user_date(fname, self.msg_data, user_token, file_data)
          else:   ## add to existing file
            file_data = feeds
            self.add_user_data(fname, self.msg_data, user_token, file_data)

  def update_user_data(self, json_file_path, user_entry, user_token, file_data):
    with open(json_file_path, "r") as jsonFile:
      data = json.load(jsonFile)
      tmp = data[user_token]
    data[user_token] = user_entry
    with open(json_file_path, "w") as jsonFile:
        json.dump(data, jsonFile)
  
  ##########    Game control  ##########
  def lunch_game(self):
      # self.user_token = self.randomString(25)
      super(HangmanGameAPI,self).start_game()
      user_token = self.randomString(10)
      self.msg_data =  self.get_json_user_data(user_token)
      self.write_user_into_file(user_token) 
      rc = RestContent(HTTPStatus.OK, "Game has stated...", self.msg_data)
      return rc.get_content()
      #return self.msg_data
  def validate_requested_data(self, requested_data):
      ## make sure letter exist
      return requested_data
  def validate_game_state(self):
      if self.word == '*' * self.word_length:
        msg = "Congrats! You have guessed it successfully..."
        msg +=  self.manage_highest_score(self.word_length, self.failed_count) 

      elif self.failed_count != self.limit:
        self.update_user_date()

      return msg 
  def play_game(self, user_token, requested_data):
    # self.user_token = self.randomString(25)
    self.validate_requested_data(requested_data)
    user_input = requested_data['letter']
    user_data = self.get_user_data(user_token)
    #return user_data["already_guessed"]
    self.fill_user_msg_data(user_data, user_token)
    msg = self.hangman_contoller(user_input)
    # update after apply game algorithm
    self.msg_data = self.get_json_user_data(user_token)

    #self.write_user_into_file(user_token) = "Game has stated..."
    rc = RestContent(HTTPStatus.OK, msg , self.msg_data)
    return rc.get_content()
  
  ##########  APIs control  ##########
  def get_user(self, user_id):
    user_data = self.get_user_data(user_id) 
    if len(user_data) < 1:
      rc = RestContent(HTTPStatus.NOT_FOUND, "User Not found" , user_data)
    else:
      rc = RestContent(HTTPStatus.OK, "Exist" , user_data)
    return rc.get_content()
  
class RestContent(object):
      """docstring for RestContent"""
      def __init__(self, code, msg, data):
        super(RestContent, self).__init__()
        self.msg = msg
        self.code = code
        self.data = data

      def get_content(self):
        return {"code" : self.code, "msg" : self.msg, "data" : self.data}
