SELECT s.Name, s.Receiving_Yards,
ROUND(
    PERCENT_RANK() OVER (ORDER BY Receiving_Yards),2
) yards_percentile,
a.College_Dominator_Rating, ROUND(
    PERCENT_RANK() OVER (ORDER BY College_Dominator_Rating),2
) DOM_percentile,
a.Breakout_Age, ROUND(
    PERCENT_RANK() OVER (ORDER BY Breakout_Age),2
) BA_percentile
FROM WR_Prospects.Stats s
    INNER JOIN WR_Prospects.Advanced_Stats a
    ON s.Name = a.Name
WHERE a.Breakout_Age IS NOT NULL
    ORDER BY s.Name;