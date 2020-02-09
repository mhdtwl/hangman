<?php

 
// abstract class GameStatus // as enum
// {
//     public const STARTED = 'STARTED';
//     public const AGAIN = 'AGAIN';
//     public const WON = 'WON';
//     public const LOST = 'LOST';
//     public const EXIT = 'EXIT';
// }

abstract class InputStatus // as enum
{
    public const RIGHT = 'RIGHT'; // right input, keep playing
    public const WRONG = 'WRONG'; // wrong input, depends on status  
    
    public const EXIST = 'EXIST'; // char already exist 
    public const INVALID = 'INVALID'; // invalid input not digit or letter
}

abstract class ScoreStatus // as enum
{
    public const GOOD = 'GOOD';
    public const GREAT = 'GREAT';
    public const NOT_BAD = 'NOT_BAD';
}


abstract class HangmanGameCore
{
    ## fruits
    protected $secretWord = ["apple", "orange", "strawberry", "berry", "banana", "pineapple"];
    protected $limit = 5; // ## limit of failures (attempts);

    ## data members
    protected $alreadyGuessed = [];
    protected $failedCount = 0;
    protected $wordLength = 0;
    protected $highestScore = 0;
    protected $wordDisplay = "";
    protected $word = "";

    protected function startGame($highestScore = 0)
    {
        $this->highestScore = $highestScore;
        $this->word = $this->secretWord[array_rand($this->secretWord)];
        $this->wordLength = strlen($this->word);
        $this->failedCount = 0;
        for ($i = 0; $i < $this->wordLength; $i++) {
            $this->wordDisplay .= '*';
        }
        $this->alreadyGuessed = [];
    }
   
    private function getIndices($string, $char)
    {
        $lastPos = 0;
        $positions = array();

        while (($lastPos = strpos($string, $char, $lastPos)) !== false) {
            $positions[] = $lastPos;
            $lastPos = $lastPos + strlen($char);
        }

        return $positions;
    }

    protected function matchRightGuess($guess)
    {
        //print_r([$this->alreadyGuessed, $guess , $this->word, $this->wordDisplay]);
        $this->alreadyGuessed[] = $guess;
        $indexes = $this->getIndices($this->word, $guess);
        $newWordArray = str_split($this->wordDisplay);
        for ($i = 0; $i < count($newWordArray); $i++) {
            if (in_array($i, $indexes)) {
                $newWordArray[$i] = $guess;
            }
        }
        $this->wordDisplay = implode('', $newWordArray);
        $msg = $this->wordDisplay . "\n";
        return $msg;
    }

    #### End Hangman possibility ####

    protected function manageHighestScore($currentWordLength, $currentFailedCount)
    {
        $resultMsg = "";
        $currentScore = (($currentWordLength - $currentFailedCount) * 100);
        if ($this->highestScore < $currentScore) {
            $scoreState = ScoreStatus::GREAT;
            $this->highestScore = $currentScore;
        } else {
            if ($this->highestScore == $currentScore) {
                $scoreState = ScoreStatus::GOOD;
                $this->highestScore = $currentScore;
            } else {
                $scoreState = ScoreStatus::NOT_BAD;
            }
        }
        return [$scoreState, $currentScore];
    }

    protected function inputController($guessedInput)
    {
        $guess = trim($guessedInput);
        $msg = "";
        if (strlen($guess) == 0 or strlen($guess) >= 2) {
            $inputStatus = InputStatus::INVALID;
        } else {
            if (in_array($guess, str_split($this->word))) {
                $inputStatus = InputStatus::RIGHT;
            } else {
                if (in_array($guess, $this->alreadyGuessed)) {
                    $inputStatus = InputStatus::EXIST;
                } else {
                    $this->failedCount += 1;
                    $inputStatus = InputStatus::WRONG;
                }
            }
        }
        return [$inputStatus, $guess];
    }
}