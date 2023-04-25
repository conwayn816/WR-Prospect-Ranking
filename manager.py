from flask import Flask, render_template, request, redirect, url_for, session
import _mysql_connector as myconn
import mysql 
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
#from wtforms import Form, StringField
import mysql.connector
from mysql.connector import errorcode
from sqlalchemy import create_engine
from sqlalchemy import text

from sqlalchemy.orm import sessionmaker
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
#DisplayPlayers.html (displays the list of players)
@app.route("/")
def list():
   con = engine.connect()
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


#add a new player to the database
@app.route("/Add_Stats", methods=["POST", "GET"])
def add():
   con = engine.connect()
   if request.method == "POST":
      '''
      Name = request.form["Name"]
      Conference = request.form["Conference"]
      Team = request.form["Team"]
      Overall_Pick = request.form["Overall_Pick"]
      Draft_Class = request.form["Draft_Class"]
      Receiving_Yards = request.form["Receiving_Yards"]
      Receptions = request.form["Receptions"]
      Yards_Per_Reception = request.form["Yards_Per_Reception"]
      Receiving_Touchdowns = request.form["Receiving_Touchdowns"]
      College_Dominator_Rating = request.form["College_Dominator_Rating"]
      Breakout_Age = request.form["Breakout_Age"]
      College_Level_of_Competition = request.form["College_Level_of_Competition"]
      RAS_Score = request.form["RAS_Score"]
      '''
        
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

   
      
#search for a player in the database
@app.route("/search", methods = ["POST", "GET"])
def search():

   con = engine.connect()
   if request.method == "POST":
      Name = request.form["Name"]
      session['Name'] = Name
      # session['Name'] = request.form['Name']
      
      '''
      query = "SELECT * \
            FROM Player \
            LEFT JOIN Stats ON Player.Name = Stats.Name \
            LEFT JOIN Advanced_Stats ON Player.Name = Advanced_Stats.Name \
            LEFT JOIN Conferences ON Player.Conference = Conferences.Conference_Name \
            WHERE Player.Name LIKE ':Name';"
      '''
      #thomas attempt without wildcard

      player_list = session.get('player_list', [])

      rows = con.execute(text("SELECT * \
            FROM Player \
            LEFT JOIN Stats ON Player.Name = Stats.Name \
            LEFT JOIN Advanced_Stats ON Player.Name = Advanced_Stats.Name \
            LEFT JOIN Conferences ON Player.Conference = Conferences.Conference_Name \
            WHERE Player.Name = :Name")).fetchall()
      '''
      with engine.connect() as con:
         results = con.execute(text(query), session).fetchall()
         con.commit()
      '''
      con.close()
      return render_template("/searchResults.html", Name=Name, rows = rows, player_list = player_list)
   else:
      return render_template('search.html')
'''
#displays a single player when he is searched for 
@app.route("/display_single_player", methods = ["POST", "GET"])
def display_single_player(Name):

   rows = "SELECT * \
            FROM Player \
            LEFT JOIN Stats ON Player.Name = Stats.Name \
            LEFT JOIN Advanced_Stats ON Player.Name = Advanced_Stats.Name \
            LEFT JOIN Conferences ON Player.Conference = Conferences.Conference_Name \
            WHERE Player.Name LIKE '%s';"


   #with engine.connect() as con:
    #    result = con.execute(rows, name=f"%{Name}%").fetchall()

   return render_template("searchResults.html",rows=rows)

'''

@app.route("/delete", methods = ["POST", "GET"])
def delete():
   con = engine.connect()

   if request.method == "POST":
      session['Name'] = request.form["Name"]

      query = "DELETE FROM Player WHERE Name = :Name"
       
      with engine.connect() as con:
         con.execute(text(query),session)
         con.commit()
      con.close()
      return redirect("/")
   else:
      return render_template("delete.html")

@app.route("/update_player", methods = ["POST", "GET"])
def update_player():
   con = engine.connect()
   # Get the form data
   Name = request.form['Name']
   Draft_Class = request.form['Draft_Class']
   Conference = request.form['Conference']
   Team = request.form['Team']
   Overall_Pick = request.form['Overall_Pick']

   # Update the database
   con.execute('UPDATE Player SET Draft_Class=?, Conference=?, Team=?, Overall_Pick=? WHERE Name =?',
               (Draft_Class, Conference, Team, Overall_Pick, Name))
  
   con.close()
   # Redirect back to the player page
   return redirect(url_for('DisplayPlayers.html', Name = Name))



#main
if __name__ == "__main__":
    app.run(debug = True)