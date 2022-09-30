from dbconn import *
import pandas as pd

#t2cur = dbconn.cursor()

t2rosterquery = "SELECT shooting+finishing+ballwork+rebounding+defense AS 'ovr', fname, lname, home_city, home_state, stars, shooting, finishing, ballwork, rebounding, defense, stamina, minutes, shooting*minutes AS 'adjshooting', finishing*minutes AS 'adjfinishing', ballwork*minutes AS 'adjballwork', rebounding*minutes AS 'adjrebounding', defense*minutes AS 'adjdefense' FROM players WHERE school = '%s'" % t2


#t2cur.execute(t2query)

"""print("\nUniversity of Kentucky Wildcats Men's SimBBA Testing Roster:\n")

for (fname, lname, home_city, home_state, stars, shooting, finishing, ballwork, rebounding, defense) in cur:
    ovr = shooting + finishing + ballwork + rebounding + defense
    print("({}) {} {}, {} star from {}, {}".format(ovr, fname,lname,stars,home_city,home_state))"""
    
t2roster_df = pd.read_sql(t2rosterquery,dbconn)