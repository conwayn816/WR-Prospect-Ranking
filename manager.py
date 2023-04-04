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


@app.route("/Add Stats")
def add():
    if request.method == 'POST':
      try:
         nm = request.form['Name']
         cla = request.form['Classes']
         maj = request.form['Major']
         gpa = request.form['GPA']
         
         # connect to the database and aquire a "cursor"
         with mysql.connect("database.db") as con:
            cur = con.cursor()
            # insert the form values in the database
            cur.execute("INSERT INTO students (Name,Classes,Major,GPA) VALUES (?,?,?,?)",(nm,cla,maj,gpa) )
            
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