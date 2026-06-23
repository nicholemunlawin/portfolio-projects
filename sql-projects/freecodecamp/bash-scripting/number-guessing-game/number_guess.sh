#!/bin/bash

PSQL="psql --username=freecodecamp --dbname=number_guess -t --no-align -c"

SECRET_NUMBER=$(( RANDOM % 1000 + 1 ))


# get username
echo "Enter your username:"
read USERNAME


# user check logic
USER_INFO=$($PSQL "SELECT user_id, games_played, best_game FROM users WHERE username='$USERNAME'")

if [[ -z $USER_INFO ]]
then
  echo "Welcome, $USERNAME! It looks like this is your first time here."

  INSERT_USER=$($PSQL "INSERT INTO users(username, games_played, best_game) VALUES('$USERNAME', 0, NULL)")
  USER_ID=$($PSQL "SELECT user_id FROM users WHERE username='$USERNAME'")
else
  IFS="|" read USER_ID GAMES_PLAYED BEST_GAME <<< "$USER_INFO"

  echo "Welcome back, $USERNAME! You have played $GAMES_PLAYED games, and your best game took $BEST_GAME guesses."
fi


# game introduction message
echo "Guess the secret number between 1 and 1000:"


# main logic for random number and guessing game
GUESSES=0

while true
do
  read GUESS
  ((GUESSES++))

  if ! [[ $GUESS =~ ^[0-9]+$ ]]
  then
    echo "That is not an integer, guess again:"
    continue
  fi

  if (( GUESS < SECRET_NUMBER ))
  then
    echo "It's higher than that, guess again:"
  elif (( GUESS > SECRET_NUMBER ))
  then
    echo "It's lower than that, guess again:"
  else
    break
  fi
done

echo "You guessed it in $GUESSES tries. The secret number was $SECRET_NUMBER. Nice job!"

CURRENT_INFO=$($PSQL "SELECT games_played, best_game FROM users WHERE user_id=$USER_ID")

IFS="|" read GAMES BEST <<< "$CURRENT_INFO"

NEW_GAMES=$((GAMES + 1))

if [[ -z $BEST || $GUESSES -lt $BEST ]]
then
  UPDATE_USER=$($PSQL "UPDATE users SET games_played=$NEW_GAMES, best_game=$GUESSES WHERE user_id=$USER_ID")
else
  UPDATE_USER=$($PSQL "UPDATE users SET games_played=$NEW_GAMES WHERE user_id=$USER_ID")
fi