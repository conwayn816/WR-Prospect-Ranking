
UPDATE WR_Prospects.Stats AS a
INNER JOIN (
    SELECT Name, Recieving_Yards, 
           PERCENT_RANK() OVER (ORDER BY Recieving_Yards) AS Yards_Percentile
    FROM WR_Prospects.Stats
) AS b ON a.Name = b.Name
SET a.Yards_Percentile = b.Yards_Percentile