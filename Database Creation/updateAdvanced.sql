UPDATE WR_Prospects.Advanced_Stats AS a
INNER JOIN (
    SELECT Name, College_Dominator_Rating, 
           PERCENT_RANK() OVER (ORDER BY College_Dominator_Rating) AS DOM_Percentile
    FROM WR_Prospects.Advanced_Stats
    WHERE College_Dominator_Rating IS NOT NULL
) AS b ON a.Name = b.Name
SET a.DOM_Percentile = b.DOM_Percentile
WHERE a.College_Dominator_Rating IS NOT NULL;

UPDATE WR_Prospects.Advanced_Stats AS a
INNER JOIN (
    SELECT Name, College_Level_of_Competition, 
           PERCENT_RANK() OVER (ORDER BY College_Level_of_Competition) AS LOC_Percentile
    FROM WR_Prospects.Advanced_Stats
    WHERE College_Level_of_Competition IS NOT NULL
) AS b ON a.Name = b.Name
SET a.LOC_Percentile = b.LOC_Percentile
WHERE a.College_Level_of_Competition IS NOT NULL;

UPDATE WR_Prospects.Advanced_Stats AS a
INNER JOIN (
    SELECT Name, RAS_Score, 
           PERCENT_RANK() OVER (ORDER BY RAS_Score) AS RAS_Percentile
    FROM WR_Prospects.Advanced_Stats
    WHERE RAS_Score > 0
) AS b ON a.Name = b.Name
SET a.RAS_Percentile = b.RAS_Percentile
WHERE a.RAS_Score > 0;


