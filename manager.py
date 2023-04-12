from flask import Flask, render_template, request
import _mysql_connector as myconn
import mysql 

app = Flask(__name__)

#DisplayPlayers.html (displays the list of players)
@app.route("/Player List")
def list():
    # connect to the database 
   con = mysql.connect("database.db")
   con.row_factory = mysql.Row

   # aquire a cursor and excute the query
   cur = con.cursor()
   cur.execute("select * from players")
   
   #send the returned table as a list of rows to the front end
   rows = cur.fetchall()
   return render_template("DisplayPlayers.html",rows = rows)


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


#main
if __name__ == "__main__":
    app.run(debug = True)