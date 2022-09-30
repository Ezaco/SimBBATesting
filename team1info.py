from dbconn import *
import pandas as pd

t1teamquery = "SELECT * FROM schools WHERE abbrev = '%s'" % t1

t1team_df = pd.read_sql(t1teamquery,dbconn)