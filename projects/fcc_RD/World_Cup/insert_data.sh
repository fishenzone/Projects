#! /bin/bash

if [[ $1 == "test" ]]
then
  PSQL="psql --username=postgres --dbname=worldcuptest -t --no-align -c"
else
  PSQL="psql --username=freecodecamp --dbname=worldcup -t --no-align -c"
fi

# Do not change code above this line. Use the PSQL variable above to query your database.
echo "$($PSQL "TRUNCATE TABLE games, teams;")"

function ADDTEAM () {
  RESULT_TEAM_ID=$($PSQL "SELECT team_id FROM teams WHERE name='$1';")
  if [[ -z $RESULT_TEAM_ID ]]
  then 
    INSERT_TEAM_RESULT=$($PSQL "INSERT INTO teams(name) VALUES('$1');")
    if [[ $INSERT_TEAM_RESULT == 'INSERT 0 1' ]]
    then
      echo TEAM ADDED $1
    fi
  fi
  RESULT_TEAM_ID=$($PSQL "SELECT team_id FROM teams WHERE name='$1';")
}

cat games.csv | while IFS=, read YEAR ROUND WINNER OPPONENT WINNER_GOALS OPPONENT_GOALS
do
  if [[ $YEAR != 'year' ]]
  then
    ADDTEAM "$WINNER"
    WINNER_ID=$RESULT_TEAM_ID
    ADDTEAM "$OPPONENT"
    OPPONENT_ID=$RESULT_TEAM_ID
    
    INSERT_GAME_RESULT=$($PSQL "INSERT INTO games(year, round, winner_id, opponent_id, \
    winner_goals, opponent_goals) VALUES($YEAR, '$ROUND', $WINNER_ID, $OPPONENT_ID, $WINNER_GOALS,\
     $OPPONENT_GOALS);")
    if [[ $INSERT_GAME_RESULT == 'INSERT 0 1' ]]
    then
      echo GAME ADDED: $YEAR, $ROUND, $WINNER_ID, $OPPONENT_ID
    fi
  fi
done