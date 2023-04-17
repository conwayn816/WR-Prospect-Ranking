CREATE TABLE WR_Prospects.Stats (
    Name VARCHAR(255) REFERENCES Player(Name),
    Receiving_Yards INT,
    Receptions INT,
    Yards_Per_Reception FLOAT,
    Receiving_Touchdowns INT,
    PRIMARY KEY (Name)
);
