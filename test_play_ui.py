import unittest
from hangman_game_ui	 import HangmanGameUI


class TestHangmanUi(unittest.TestCase):
	"""docstring for TestHangmanUi"""
	def __init__(self, arg):
		super(TestHangmanUi, self).__init__()
		self.game = HangmanGameUI()

	def test_draw_ui_hangman(self):
		# self.assertEqual(2,2,"Yes")	
		#self.game.manage_highest_score(5,2)
		pass		
		
 