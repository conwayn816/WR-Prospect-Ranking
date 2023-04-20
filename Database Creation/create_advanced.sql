CREATE TABLE WR_Prospects.Advanced_Stats (
    Name VARCHAR(255) REFERENCES Player(Name),
    College_Dominator_Rating FLOAT,
    DOM_Percentile FLOAT,
    Breakout_Age FLOAT,
    BA_Percentile FLOAT
    College_Level_of_Competition FLOAT,
    LOC_Percentile FLOAT,
    RAS_Score FLOAT,
    RAS_Percentile FLOAT,
    PRIMARY KEY (Name)
);
