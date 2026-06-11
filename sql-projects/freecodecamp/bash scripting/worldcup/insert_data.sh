#! /bin/bash

if [[ $1 == "test" ]]
then
  PSQL="psql --username=postgres --dbname=worldcuptest -t --no-align -c"
else
  PSQL="psql --username=freecodecamp --dbname=worldcup -t --no-align -c"
fi

# Do not change code above this line. Use the PSQL variable above to query your database.
while IFS=',' read -r year round winner opponent winner_goals opponent_goals
do 
  if [[ $year != "year" ]]; 
  then
    TEAM1=$($PSQL "INSERT INTO teams(name) VALUES('$winner') ON CONFLICT DO NOTHING")
    TEAM2=$($PSQL "INSERT INTO teams(name) VALUES('$opponent') ON CONFLICT DO NOTHING")
    TEAM1_ID=$($PSQL "SELECT team_id FROM teams WHERE name='$winner'")
    TEAM2_ID=$($PSQL "SELECT team_id FROM teams WHERE name='$opponent'")
    $PSQL "INSERT INTO games(year, round, winner_id, opponent_id, winner_goals, opponent_goals) VALUES($year, '$round', $TEAM1_ID, $TEAM2_ID, $winner_goals, $opponent_goals)"
  fi
done < games.csv