from dbconn import *
import pandas as pd

t2teamquery = "SELECT * FROM schools WHERE abbrev = '%s'" % t2

t2team_df = pd.read_sql(t2teamquery,dbconn)