from flask import Flask, render_template, request
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
   
   cur.execute("SELECT * FROM Player")
   
   #send the returned table as a list of rows to the front end
   rows = cur.fetchall()
   return render_template("DisplayPlayers.html",rows = rows)

#add a new player to the database
@app.route("/Add Stats", methods = ["POST", "GET"])
def add():
    if request.method == 'POST':
      try:
         #team info
         TeamName = request.form['TeamName']
         QBrating = request.form['QBrating']
         #conference info
         ConferenceName = request.form['ConferenceName']
         ConferenceStrength = request.form['ConferenceStrength']
         #player info
         PlayerName = request.form['PlayerName']
         PlayerClass = request.form['PlayerClass']
         RAS = request.form["RAS"]
         #player stats
         RecTD = request.form["RecTD"]
         ThirdDown= request.form["ThirdDown"]
         TeamYards = request.form["TeamYards"]
         RecYards = request.form["RecYards"]
         Dominator = request.form["Dominator"]
         Breakout = request.form["Breakout"]


         # connect to the database and aquire a "cursor"
         with mysql.connect("database.db") as con:
            cur = con.cursor()
            # insert the form values in the database

            cur.execute("INSERT INTO team (Name,Classes,Major,GPA) VALUES (?,?,?,?)",(nm,cla,maj,gpa) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

#search for a player in the database
@app.route("/search", methods = ["POST", "GET"])
def search():

   return render_template("search.html")

#returns the results of the player search
@app.route("/results", methods = ["POST", "GET"])
def results():

   # get the search input from the form
   search_input = request.form["search_input"]
    
   query = "SELECT * FROM Player WHERE name LIKE %s"
   params = ("%" + search_input + "%",) #add the %% onto the string so we can wildcard search

   # execute the query with the parameterized search input
   cur.execute(query, params)
    
   # retrieve the results from the cursor object
   search_results = cur.fetchall()

   return render_template("searchResults.html", results=search_results)

@app.route("/delete", methods = ["POST", "GET"])
def delete():

   delete_search = request.form["delete_search"]

   query = "DELETE FROM Player WHERE name LIKE %s"
   params = params = ("%" + delete_search + "%",)  
   cur.execute(query, params)

   return render_template("DisplayPlayers.html")


@app.route("/update", methods = ["POST", "GET"])
def update():

   query = "UPDATE Player "

#main
if __name__ == "__main__":
    app.run(debug = True)