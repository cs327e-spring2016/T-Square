# T-Square
<<<<<<< Updated upstream
#Main file are:Playerposition_player_player_stats.py Game.py and team_team_stats.py
=======
>>>>>>> Stashed changes
#create database
CREATE DATABASE nba;

#all the querries to creat 6 tables
#player table:
CREATE TABLE player (
  player_id varchar(20) NOT NULL,
  name varchar(50) ,
  height varchar(20) ,
  weight smallint(7) ,
  PRIMARY KEY (player_id)

#player_position table
CREATE TABLE  player_position  (
   id  int(11) NOT NULL AUTO_INCREMENT,
   player_id  varchar(20),
   position  varchar(20),
  PRIMARY KEY ( id ),
  KEY  player_id  ( player_id ),
  CONSTRAINT  player_position_ibfk_1  FOREIGN KEY ( player_id ) REFERENCES  player  ( player_id )

#player_stats table
CREATE TABLE player_stats (
  player_id varchar(20) NOT NULL,
  assistant smallint(6) ,
  block smallint(6) ,
  fieldg smallint(6) ,
  fieldg3 smallint(6) ,
  fieldg3_pct decimal(4,3) ,
  freet_attemp smallint(6) ,
  minute_played time ,
  offrebound smallint(6) ,
  personal_foul smallint(6) ,
  points smallint(6) ,
  steal smallint(6) ,
  turnover smallint(6) ,
  total_reb smallint(6) ,
  fieldg_attempt smallint(6) ,
  freethrow smallint(6) ,
  fieldg3_attempt smallint(6) ,
  fieldg_pct decimal(4,3) ,
  freethrow_pct decimal(4,3) ,
  game_date date NOT NULL,
  derebound smallint(6) ,
  PRIMARY KEY (player_id,game_date),
  KEY fk_game (game_date),
  CONSTRAINT fk_game FOREIGN KEY (game_date) REFERENCES game (date),
  CONSTRAINT fk_player FOREIGN KEY (player_id) REFERENCES player (player_id)
);


#game table
CREATE TABLE game (
 date date NOT NULL,
 host varchar(20) NOT NULL,
 guest varchar(20) ,
 host_score bigint(7) ,
 guest_score bigint(7) ,
 PRIMARY KEY (date,host));


#team table
CREATE TABLE team (
 name varchar(50) ,
 abbrev varchar(20) NOT NULL,
 PRIMARY KEY (abbrev));


#team_stats table
CREATE TABLE team_stats (
  game date NOT NULL,
  team varchar(50) NOT NULL,
  tassistant smallint(6) ,
  tblock smallint(6) ,
  tfieldg smallint(6) ,
  tfieldg3 smallint(6) ,
  tfieldg3_pct decimal(4,3) ,
  tfreethrow_attempt smallint(6) ,
  toffebound smallint(6) ,
  tpersonal_foul smallint(6) ,
  tpoints smallint(6) ,
  tsteal smallint(6) ,
  tturnover smallint(6) ,
  ttotal_reb smallint(6) ,
  tfieldg_attempt smallint(6) ,
  tfreethrow smallint(6) ,
  tfieldg3_attempt smallint(6),
  tfreethrow_pct decimal(4,3),
  tfieldg_pct decimal(4,3),
  PRIMARY KEY (game,team),
  KEY fk_team_stats_team (team),
  CONSTRAINT fk_team_stats_game FOREIGN KEY (game) REFERENCES game (date)
  CONSTRAINT fk_team_stats_team FOREIGN KEY (team) REFERENCES team (abbrev)
);

#For the player and player_stats table, we used a jason file downloaded online 
<<<<<<< Updated upstream
#Pandas module
#requests module
=======
>>>>>>> Stashed changes
