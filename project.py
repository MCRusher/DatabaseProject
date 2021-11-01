from flask import Flask, render_template, request
import pandas as pd
import pyodbc
import csv

import sqlite3 
app = Flask(__name__)



#Creating database Table countires
conn = sqlite3.connect('countries.db')
print ("Opened database successfully"); 
conn.execute('''CREATE TABLE if not exists  countries
			( Country TEXT PRIMARY KEY NOT NULL,
			Population BIGINT NOT NULL, 
			ID INT FORIEGN KEY NOT NULL);''')

print ("Table created successfully"); 


#opening CSV file
cur = conn.cursor()
csv_file = pd.read_csv('countries_of_world.csv')
df = pd.DataFrame(csv_file)
print(df)

#inserting selective data into countries database from CSV file
for row in df.itertuples():
	cur.execute("INSERT INTO countries(Country,Population,ID) VALUES (?,?,?)",
				(row.Country,row.Population,row.ID)
				)
conn.commit()
cur.execute("SELECT Country FROM countries WHERE ID = 0")
print(cur.fetchall())

conn.close()















