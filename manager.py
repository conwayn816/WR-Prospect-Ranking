from flask import Flask, render_template, request, redirect, url_for
import _mysql_connector as myconn
import mysql 
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
#from wtforms import Form, StringField
import mysql.connector
from mysql.connector import errorcode
'''

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'Thomas'
app.config['MYSQL_PASSWORD'] = 'Percy24!'
app.config['MYSQL_DB'] = 'WR_Prospects'
 # connect to the database 
con = mysql.connector.connect("WR_Prospects.db")
con.row_factory = mysql.Row
# aquire a cursor and excute the query
cur = con.cursor()



'''

try:
                              #use your username and password here...
   #cnx = mysql.connector.connect(user='Thomas', password='Percy24!',
    #                          host='127.0.0.1',
     #                         database='WR_Prospects')
   cnx = mysql.connector.connect(host = "localhost", user = "Thomas", passwd = "Percy24!")
   cur = mysql.cursor()

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()

app = Flask(__name__)
mysql = MySQL(app)


#DisplayPlayers.html (displays the list of players)
@app.route("/Player List")
def list():
   
   cur.execute("SELECT p.Name, p.College_Conference, c.Conference_Strength, p.College_Team, \
               p.Overall_Pick, p.Draft_Class, s.Receiving_Yards, s.Receptions, s.Yards_Per_Reception, \
               s.Receiving_Touchdowns, a.College_Dominator_Rating, a.Breakout_Age, a.College_Level_of_Competition, \
               a.RAS_Score \
               FROM WR_Prospects.Player p \
               JOIN WR_Prospects.Stats s ON p.Name = s.Name \
               JOIN WR_Prospects.Advanced_Stats a ON p.Name = a.Name \
               JOIN WR_Prospects.Conferences c ON p.College_Conference = c.Conference_Name \
               ORDER BY p.Name;")
   
   #send the returned table as a list of rows to the front end
   rows = cur.fetchall()
   return render_template("DisplayPlayers.html",rows = rows)

#add a new player to the database
@app.route("/Add_Stats", methods = ["POST", "GET"])
def add():
   if request.method == 'POST':
         #Conference
         Conference_Name = request.form['Conference_Name']
         Conference_Strength = request.form['Conference_Strength']
         #Player
         Name = request.form['Name']
         Conference = request.form["Conference"]
         Team = request.form["Team"]
         Overall_Pick = request.form["Overall_Pick"]
         Draft_Class = request.form['Draft_Class']
         Score = request.form["Score"] #advanced function 
         #Stats
         Receiving_Yards = request.form["Receiving_Yards"]
         #Yards_Percentile = request.form["Yards_Percentile"]
         Receptions = request.form["Receptions"]
         Yards_Per_Reception = request.form["Yards_Per_Reception"]
         Receiving_Touchdowns = request.form["Receiving_Touchdowns"]
         #Advanced_Stats
         College_Dominator_Rating = request.form["College_Dominator_Rating"]
         #DOM_Percentile = request.form["DOM_Percentile"]
         Breakout_Age = request.form["Breakout_Age"]
         #BA_Percentile = request.form["BA_Percentile"]
         College_Level_of_Competition = request.form["College_Level_of_Competition"]
         #LOC_Percentile = request.form["LOC_Percentile"]
         RAS_Score = request.form["RAS_Score"]
         #RAS_Percentile = request.form["RAS_Percentile"]

         player_query = "INSERT INTO Player(Name, Conference) VALUES(%s, %s)"
         stats_query = "INSERT INTO Stats() VALUES()"

         cur.execute(player_query, Name, Conference)

         return "Player added successfully!"
   else:
      return render_template('AddStats.html')


#search for a player in the database
@app.route("/search", methods = ["POST", "GET"])
def search():

   Name = request.form['search_input']
   player_data = single_player(Name) #get info about the player we just searched
   
   if player_data:
      return render_template('search.html', player_found=True, Name = Name)
   else:
      return render_template('search.html')


#returns the results of the player search
@app.route("/results", methods = ["POST", "GET"])
def results():

   # get the search input from the form
   search_input = request.form["search_input"]
    
   query = "SELECT * FROM Player WHERE Name LIKE %s"
   params = ("%" + search_input + "%",) #add the %% onto the string so we can wildcard search

   # execute the query with the parameterized search input
   cur.execute(query, params)
    
   # retrieve the results from the cursor object
   search_results = cur.fetchall()

   return render_template("searchResults.html", results=search_results)

#displays a single player when he is searched for 
@app.route("/single_player", methods = ["POST", "GET"])
def single_player(Name):

   query = "SELECT * \
            FROM Player \
            LEFT JOIN Stats ON Player.Name = Stats.Name \
            LEFT JOIN Advanced_Stats ON Player.Name = Advanced_Stats.Name \
            LEFT JOIN Conferences ON Player.College_Conference = Conferences.Conference_Name \
            WHERE Player.Name LIKE '%s';"
   
   Name = ("%" + Name + "%")

   cur.execute(query, Name)
   result = cur.fetchone()
   return result

@app.route('/name_check', methods=['POST'])
def name_check():
    # retrieve the player name from the search form
    player_name = request.form['player_name']
    
    # check if the player exists in the database
    cur.execute("SELECT * FROM Player WHERE Name = %s", (player_name,))
    player = cur.fetchone()
    if not player:
        return render_template('search.html', message='Player not found.')
    
    # pass the player's data to the update form
    return redirect('/update_player/{}'.format(player['Name']))

@app.route("/delete", methods = ["POST", "GET"])
def delete():

   delete_search = request.form["delete_search"]

   query = "DELETE FROM Player WHERE Name LIKE %s"
   params = params = ("%" + delete_search + "%",)  
   cur.execute(query, params)

   return render_template("DisplayPlayers.html")

@app.route("/update_player", methods = ["POST", "GET"])
def update_player():

   # Get the form data
   Name = request.form['Name']
   Draft_Class = request.form['Draft_Class']
   Conference = request.form['Conference']
   Team = request.form['Team']
   Overall_Pick = request.form['Overall_Pick']

   # Update the database
   cur.execute('UPDATE Player SET Draft_Class=?, Conference=?, Team=?, Overall_Pick=? WHERE Name =?',
               (Draft_Class, Conference, Team, Overall_Pick, Name))
  

   # Redirect back to the player page
   return redirect(url_for('DisplayPlayers.html', Name = Name))



#main
if __name__ == "__main__":
    app.run(debug = True)