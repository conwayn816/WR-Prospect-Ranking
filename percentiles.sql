SELECT s.Name, s.Receiving_Yards,
ROUND(
    PERCENT_RANK() OVER (ORDER BY Receiving_Yards),2
) yards_percentile,
a.RAS_Score, ROUND(
    PERCENT_RANK() OVER (ORDER BY RAS_Score),2
) RAS_percentile,
a.Breakout_Age, ROUND(
    PERCENT_RANK() OVER (ORDER BY Breakout_Age),2
) BA_percentile
FROM WR_Prospects.Stats s
    INNER JOIN WR_Prospects.Advanced_Stats a
    ON s.Name = a.Name
WHERE a.RAS_Score > 0
    ORDER BY s.Name;