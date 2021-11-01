import sqlite3 as sql
import pandas as pd
from os.path import exists

db_exists = exists("data.db")

#creates new database if it doesn't exist
con = sql.connect("data.db")

cur = con.cursor()

#enables foreign keys checking in sqlite
cur.execute("PRAGMA foreign_keys=ON")

#creates the intial database tables if they don't exist
if not db_exists:
    #loads sql script file for initializing the database
    with open('schema.sql', 'r') as sql_file:
        sql_script = sql_file.read()
    #executes intialization script
    cur.executescript(sql_script)

#read data from csv file, only retaining Country and Population
data = pd.read_csv("countries_of_world.csv", usecols=["Country", "Population"])
#rename columns to be compatible with database Countries table fields
data.columns=["countryName", "population"]
#append to database
data.to_sql(name="Countries", con=con, if_exists='replace', index=False)

res = cur.execute("SELECT * FROM countries")

print(res.fetchall())