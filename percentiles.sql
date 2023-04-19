SELECT s.Name, s.Receiving_Yards,
ROUND(
    PERCENT_RANK() OVER (ORDER BY Receiving_Yards),2
) yards_percentile,
a.College_Dominator_Rating, ROUND(
    PERCENT_RANK() OVER (ORDER BY College_Dominator_Rating),2
) DOM_percentile,
a.College_Level_of_Competition, ROUND(
    PERCENT_RANK() OVER (ORDER BY College_Level_of_Competition),2
) LOC_percentile
FROM WR_Prospects.Stats s
    INNER JOIN WR_Prospects.Advanced_Stats a
    ON s.Name = a.Name;
