LOAD DATA LOCAL INFILE 'WR Advanced Statistics.csv'
INTO TABLE WR_Prospects.Advanced_Stats
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;