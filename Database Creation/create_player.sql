CREATE TABLE WR_Prospects.Player (
    Name VARCHAR(255) PRIMARY KEY,
    Conference VARCHAR(255) REFERENCES Conferences(Conference_Name),
    Team VARCHAR(255),
    Overall_Pick INT,
    Draft_Class INT
);
