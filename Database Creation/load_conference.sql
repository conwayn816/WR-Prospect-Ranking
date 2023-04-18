LOAD DATA LOCAL INFILE '/Users/nathanconway/Desktop/COP4710/WR-Prospect-Ranking/WRData/conferences.csv'
INTO TABLE WR_Prospects.Conferences
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
