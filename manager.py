from flask import Flask, render_template, request, redirect, session
# from wtforms import Form, StringField
from sqlalchemy import create_engine
from sqlalchemy import text
# create a connection to the MySQL database
app = Flask(__name__)
user = 'root'
password = 'Ap080602'
host = 'localhost'
port = '3306'
database = 'WR_Prospects'
engine = create_engine(f'mysql://{user}:{password}@{host}:{port}/{database}')
# test the connection
con = engine.connect()
app.secret_key = 'my_secret_key'
# DisplayPlayers.html (displays the list of players)
@app.route("/")
def list():
   con = engine.connect()

   con.execute(text('UPDATE WR_Prospects.Advanced_Stats AS a \
INNER JOIN (\
    SELECT Name, College_Dominator_Rating, \
           PERCENT_RANK() OVER (ORDER BY College_Dominator_Rating) AS DOM_Percentile \
    FROM WR_Prospects.Advanced_Stats \
    WHERE College_Dominator_Rating IS NOT NULL \
) AS b ON a.Name = b.Name \
SET a.DOM_Percentile = b.DOM_Percentile \
WHERE a.College_Dominator_Rating IS NOT NULL; \
 \
UPDATE WR_Prospects.Advanced_Stats AS a  \
INNER JOIN ( \
    SELECT Name, College_Level_of_Competition, \
           PERCENT_RANK() OVER (ORDER BY College_Level_of_Competition) AS LOC_Percentile \
    FROM WR_Prospects.Advanced_Stats \
    WHERE College_Level_of_Competition IS NOT NULL \
) AS b ON a.Name = b.Name \
SET a.LOC_Percentile = b.LOC_Percentile \
WHERE a.College_Level_of_Competition IS NOT NULL; \
 \
UPDATE WR_Prospects.Advanced_Stats AS a \
INNER JOIN ( \
    SELECT Name, RAS_Score, \
           PERCENT_RANK() OVER (ORDER BY RAS_Score) AS RAS_Percentile \
    FROM WR_Prospects.Advanced_Stats \
    WHERE RAS_Score > 0 \
) AS b ON a.Name = b.Name \
SET a.RAS_Percentile = b.RAS_Percentile \
WHERE a.RAS_Score > 0;'))
   con.execute(text('UPDATE WR_Prospects.Advanced_Stats AS a \
INNER JOIN ( \
    SELECT Name, Breakout_Age, \
           1 - PERCENT_RANK() OVER (ORDER BY Breakout_Age) AS BA_Percentile \
    FROM WR_Prospects.Advanced_Stats \
    WHERE Breakout_Age IS NOT NULL \
) AS b ON a.Name = b.Name \
SET a.BA_Percentile = b.BA_Percentile \
WHERE a.Breakout_Age IS NOT NULL; \
'))   
   con.execute(text('UPDATE WR_Prospects.Stats AS a \
INNER JOIN ( \
    SELECT Name, Receiving_Yards, \
           PERCENT_RANK() OVER (ORDER BY Receiving_Yards) AS Yards_Percentile \
    FROM WR_Prospects.Stats \
) AS b ON a.Name = b.Name \
SET a.Yards_Percentile = b.Yards_Percentile'))

   con.execute(text('UPDATE WR_Prospects.Player p \
JOIN ( \
    SELECT p.Name,  \
           SUM(s.Yards_Percentile + a.DOM_Percentile + (a.LOC_Percentile * 3) \
               + (c.Conference_Strength * 1.5) + (s.Receiving_Touchdowns * 0.0132) + a.BA_Percentile \
               + (CASE WHEN a.RAS_Score IS NULL THEN 0 ELSE a.RAS_Percentile * 2 END)) AS Score \
    FROM WR_Prospects.Player p \
    JOIN WR_Prospects.Stats s ON p.Name = s.Name \
    JOIN WR_Prospects.Advanced_Stats a ON p.Name = a.Name \
    JOIN WR_Prospects.Conferences c ON p.Conference = c.Conference_Name \
    GROUP BY p.Name \
) AS t ON p.Name = t.Name \
SET p.Score = t.Score; \
'))

   con.commit()

   player_list = session.get('player_list', [])
   rows = con.execute(text("SELECT p.Name, p.Conference, c.Conference_Strength, p.Team, \
               p.Overall_Pick, p.Draft_Class, s.Receiving_Yards, s.Receptions, s.Yards_Per_Reception, \
               s.Receiving_Touchdowns, a.College_Dominator_Rating, a.Breakout_Age, a.College_Level_of_Competition, \
               a.RAS_Score, p.Score \
               FROM WR_Prospects.Player p \
               JOIN WR_Prospects.Stats s ON p.Name = s.Name \
               JOIN WR_Prospects.Advanced_Stats a ON p.Name = a.Name \
               JOIN WR_Prospects.Conferences c ON p.Conference = c.Conference_Name \
               ORDER BY p.Name;")).fetchall()
   con.close() 
   return render_template("DisplayPlayers.html",rows=rows, player_list=player_list)


# add a new player to the database
@app.route("/Add_Stats", methods=["POST", "GET"])
def add():
   con = engine.connect()
   if request.method == "POST":
        
      session['Name'] = request.form["Name"]
      session['Conference'] = request.form["Conference"]
      session['Team'] = request.form["Team"]
      session['Overall_Pick'] = request.form["Overall_Pick"]
      session['Draft_Class'] = request.form["Draft_Class"]
      session['Receiving_Yards'] = request.form["Receiving_Yards"]
      session['Receptions'] = request.form["Receptions"]
      session['Yards_Per_Reception'] = request.form["Yards_Per_Reception"]
      session['Receiving_Touchdowns'] = request.form["Receiving_Touchdowns"]
      session['College_Dominator_Rating'] = request.form["College_Dominator_Rating"]
      session['Breakout_Age'] = request.form["Breakout_Age"]
      session['College_Level_of_Competition'] = request.form["College_Level_of_Competition"]
      session['RAS_Score'] = request.form["RAS_Score"]

      player_query = "INSERT INTO Player(Name, Conference, Team, Overall_Pick, Draft_Class) VALUES(:Name, :Conference, :Team, :Overall_Pick, :Draft_Class)"
      stats_query = "INSERT INTO Stats(Name, Receiving_Yards, Receptions, Yards_Per_Reception, Receiving_Touchdowns) VALUES(:Name, :Receiving_Yards, :Receptions, :Yards_Per_Reception, :Receiving_Touchdowns)"
      advanced_query = "INSERT INTO Advanced_Stats(Name, College_Dominator_Rating, Breakout_Age, College_Level_of_Competition, RAS_Score) VALUES(:Name, :College_Dominator_Rating, :Breakout_Age, :College_Level_of_Competition, :RAS_Score)"


      with engine.connect() as con:
         con.execute(text(player_query), session)
         con.execute(text(stats_query), session)
         con.execute(text(advanced_query), session)
         con.commit()
   
      con.close()
      return redirect("/")
   else:
      return render_template("AddStats.html")
    
# search for a player in the database
@app.route("/search", methods = ["POST", "GET"])
def search():

   con = engine.connect()
   if request.method == "POST":
      session['Name'] = request.form['Name'] + '%'
   

      player_list = session.get('player_list', [])

      rows = con.execute(text("SELECT p.Name, p.Conference, c.Conference_Strength, p.Team, \
               p.Overall_Pick, p.Draft_Class, s.Receiving_Yards, s.Receptions, s.Yards_Per_Reception, \
               s.Receiving_Touchdowns, a.College_Dominator_Rating, a.Breakout_Age, a.College_Level_of_Competition, \
               a.RAS_Score, p.Score \
               FROM WR_Prospects.Player p \
               JOIN WR_Prospects.Stats s ON p.Name = s.Name \
               JOIN WR_Prospects.Advanced_Stats a ON p.Name = a.Name \
               JOIN WR_Prospects.Conferences c ON p.Conference = c.Conference_Name \
            WHERE p.Name LIKE :Name"), session).fetchall()
      
      con.close()
      return render_template("/searchResults.html", rows = rows, player_list = player_list)
   else:
      return render_template('search.html')

@app.route("/delete", methods = ["POST", "GET"])
def delete():
   con = engine.connect()

   if request.method == "POST":
      session['Name'] = request.form["Name"]

      query = "DELETE FROM WR_Prospects.Player WHERE Name = :Name"
      query2 = "DELETE FROM WR_Prospects.Advanced_Stats WHERE Name = :Name"
      query3 = "DELETE FROM WR_Prospects.Stats WHERE Name = :Name"
     
       
      with engine.connect() as con:
         con.execute(text(query), session)
         con.commit()
         con.execute(text(query2), session)
         con.commit()
         con.execute(text(query3), session)
         con.commit()
      con.close()
      return redirect("/")
   else:
      return render_template("delete.html")

@app.route("/update", methods = ["POST", "GET"])
def update_player():
   con = engine.connect()
   if request.method == "POST":
      # Get the form data
      session['Name'] = request.form['Name']
      session['Draft_Class'] = request.form['Draft_Class']
      session['Conference'] = request.form['Conference']
      session['Team'] = request.form['Team']
      session['Overall_Pick'] = request.form['Overall_Pick']


      update_query = 'UPDATE Player SET Draft_Class=:Draft_Class, Conference=:Conference, \
                  Team=:Team, Overall_Pick=:Overall_Pick WHERE Name =:Name'
               
      # Update the database
      con.execute(text(update_query), session)
      con.commit()
      con.close()
      # Redirect back to the player page
      return redirect('/')
   else: 
      return render_template("update.html")

@app.route("/max", methods = ["POST", "GET"])
def max():
   con = engine.connect()
   
   player_list = session.get('player_list', [])
   rows = con.execute(text("SELECT Conferences.Conference_Name, Player.Name, Player.Score \
                           FROM Player \
                           INNER JOIN Conferences ON Player.Conference = Conferences.Conference_Name \
                           WHERE Player.Score = ( \
                           SELECT MAX(Score) \
                           FROM Player AS p \
                           WHERE p.Conference = Player.Conference) ORDER BY Conferences.Conference_Name;")).fetchall()
   con.close()
   return render_template("max.html", rows = rows, player_list = player_list)


#main
if __name__ == "__main__":
    app.run(debug = True)