SELECT p.Name, 
       SUM(s.Yards_Percentile + a.DOM_Percentile + (a.LOC_Percentile * 3) 
           + (c.Conference_Strength * 1.5) + (s.Receiving_Touchdowns * 0.0132) + a.BA_Percentile 
           + (CASE WHEN a.RAS_Score IS NULL THEN 0 ELSE a.RAS_Percentile * 2 END)) AS Score
FROM WR_Prospects.Player p
JOIN WR_Prospects.Stats s ON p.Name = s.Name
JOIN WR_Prospects.Advanced_Stats a ON p.Name = a.Name
JOIN WR_Prospects.Conferences c ON p.Conference = c.Conference_Name
GROUP BY p.Name;
