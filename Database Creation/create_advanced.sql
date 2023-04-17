CREATE TABLE WR_Prospects.Advanced_Stats (
    Name VARCHAR(255) REFERENCES Player(Name),
    College_Dominator_Rating FLOAT,
    Breakout_Age FLOAT,
    College_Level_of_Competition FLOAT,
    RAS_Score FLOAT,
    PRIMARY KEY (Name)
);
