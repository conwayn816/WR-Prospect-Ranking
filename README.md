# WR Prospect Ranking Application

Our application is a database focused on storing college football wide receivers that are either currently
in the NFL or are planning on it. The aim is to grade player performance in college in order to predict how successful their NFL career will be. It utilizes a local MySQl database to store player information. All database schema is located in
the "Database Creation" folder. The "templates" folder contains all of the HTML templates for the front end of the application.
The application uses Python and Flask to interface with the database and the front end.

# Functions

LISTING - The application has a home page that displays all forward facing data for each player.

SEARCH - The application allows for the searching of players by name.

ADD - The application allows the user to input their own players. The application will calculate their score/recalculate existing
players score based on ranking.

DELETE - The application allows the user to delete players from the records.

UPDATE - The application allows the user to update player records.

TOP SCORE - The application will list the top scored player from each Power 5 Conference.


# A Glimpse into the Application

Here is a sampling of the application with a database loaded with all WR in the 2021 and 2022 draft class:
!["Home Page"](https://github.com/conwayn816/WR-Prospect-Ranking/blob/0bd4fe2c92096918717b018400468000221a1035/images/Screenshot%202023-05-08%20at%2011.34.12%20PM.png)

Here is a look at a page that displays the current top scored player in each Power 5 conference: !["Top Scores"](https://github.com/conwayn816/WR-Prospect-Ranking/blob/0bd4fe2c92096918717b018400468000221a1035/images/Screenshot%202023-05-08%20at%2011.34.22%20PM.png)

Here is a look at the search page returning players with a name starting with 'a': !["Search"](https://github.com/conwayn816/WR-Prospect-Ranking/blob/0bd4fe2c92096918717b018400468000221a1035/images/Screenshot%202023-05-08%20at%2011.36.21%20PM.png)
