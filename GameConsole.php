<?php

# HANGMAN UI7
include 'Game.php';

class HangmanGameConsole extends HangmanGameCore
{


    private function drawUIhangman()
    {
        if ($this->failedCount == 1) {
            echo("Wrong readline . " . ($this->limit - $this->failedCount) . " guess remaining\n");;
            echo "   _____
  |     
  |     
  |     
  |     
  |     
__|__\n";
        } else {
            if ($this->failedCount == 2) {
                print("Wrong readline . " . ($this->limit - $this->failedCount) . " guess remaining\n");
                echo("   _____
  |     |
  |     |
  |     |
  |     
  |     
  |     
__|__\n");
            } else {
                if ($this->failedCount == 3) {
                    print("Wrong readline . " . ($this->limit - $this->failedCount) . " guess remaining\n");
                    echo("   _____
  |     |
  |     |
  |     |
  |     O
  |     
  |     
__|__\n");
                } else {
                    if ($this->failedCount == 4) {
                        print("Wrong readline . " . ($this->limit - $this->failedCount) . " guess remaining\n");
                        print("   _____
  |     |
  |     |
  |     |
  |     O
  |    /|\
  |     
__|__\n");
                    } else {
                        if ($this->failedCount == 5) {
                            print("Wrong readline . You are hanged\n");
                            print("   _____
  |     |
  |     |
  |     |
  |     O
  |    /|\
  |    / \
__|__\n");
                            return $this->againPlay();
                        }
                    }
                }
            }
        }
    }


    private function getManageHighestScore($currentWordLength, $currentFailedCount)
    {
      list($result, $currentScore) = $this->manageHighestScore($currentWordLength, $currentFailedCount);
      $resultMsg = "Good job, You have reached the highest score " . $currentScore . "\n";
      switch ($result) {
        case ScoreStatus::GREAT:
          $resultMsg = "WoOoOoW! You have broken the highest record, The new highest score is: " . $currentScore . "\n";
          break;
        case ScoreStatus::GOOD:
          $resultMsg = "Good job, You have reached the highest score " . $currentScore . "\n";
          break;
        case ScoreStatus::NOT_BAD:
          $resultMsg = "Well, Your score is: " . $currentScore 
            . ". It's not the best, where the highest score is: " 
            . $this->highestScore . "\n" . "YOU CAN DO IT, Don't give up and Play again ;) \n";
          break;  
      }
      return $resultMsg;
    }

    private function getInputResult($guessInput)
    {
        list($result, $guess) =  $this->inputController($guessInput);
        $msg = "";

        switch ($result) {
          case InputStatus::RIGHT:
            $msg .= $this->matchRightGuess($guess);
          break;
          case InputStatus::WRONG:
            $this->drawUIhangman();
          break;
          case InputStatus::EXIST:
            $msg .= "Input already guessed, try DIFFERENT input!\n";
          break;
          case InputStatus::INVALID:
            return $this->invalidInput(); // 
          break;
          }
        return $msg;
    }

    private function againPlay()
    {
        $this->playAgainInput = readline("Do You want to play again? ( y | n )  \n");;
        while (!in_array($this->playAgainInput, ["y", "n"])) {
            $this->playAgainInput = readline("Do You want to play again? ( y | n )  \n");;
        }
        if ($this->playAgainInput == "y") {
          $game = new HangmanGameConsole();
          $game->play($this->highestScore);
        } else {
            exit();
        }
    }
   
    private function invalidInput()
    {
        $guess = readline("This is Word: " . $this->wordDisplay . " Enter your guess: \n");;
        print ("Enter a single LETTER or DIGIT only\n");;
        return $this->inputController($guess);  ## calling parent's function
    }

    private function validateGameState()
    {
        if ($this->wordDisplay == $this->word) {
            print("Congrats! You have guessed it successfully...");
            print($this->getManageHighestScore($this->wordLength, $this->failedCount));
            return $this->againPlay();
        } else {
            if ($this->failedCount != $this->limit) {
                return $this->runHangmanGame();
            }
        }
    }

    private function runHangmanGame()
    {
        $guess = readline("This is Word: (" . $this->wordDisplay . ") Enter your guess: \n");;
        echo $this->getInputResult($guess);
        return $this->validateGameState();
    }

    public function play($highestScore = 0 )
    {
      $this->startGame($highestScore);
      $this->runHangmanGame();
    }
}

$game = new HangmanGameConsole();
$game->play();
