UPDATE WR_Prospects.Advanced_Stats AS a
INNER JOIN (
    SELECT Name, Breakout_Age, 
           1 - PERCENT_RANK() OVER (ORDER BY Breakout_Age) AS Breakout_Percentile
    FROM WR_Prospects.Advanced_Stats
    WHERE Breakout_Age IS NOT NULL
) AS b ON a.Name = b.Name
SET a.Breakout_Percentile = b.Breakout_Percentile
WHERE a.Breakout_Age IS NOT NULL;
