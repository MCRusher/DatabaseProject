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
data1 = pd.read_csv("population_by_country_2020.csv", usecols=["Country (or dependency)", "Population (2020)"])
#rename columns to be compatible with database Countries table fields
data1.columns=["countryName", "population"]
#read data from csv file, only retaining Country and Population
data2 = pd.read_csv("DeltacountrySubmissionCount.csv", usecols=["Country", "Total #Delta GK (B.1.617.2+AY.*)"])
#rename columns to be compatible with database Countries table fields
data2.columns=["countryName", "DeltaCases"]
#merge two tables
data3 = data1.merge(data2, on = "countryName", how = "left")
#read data from csv file, only retaining Country and Population
data4 = pd.read_csv("AlphacountrySubmissionCount.csv", usecols=["Country", "Total #Alpha 202012/01 GRY (B.1.1.7+Q.*)"])
#rename columns to be compatible with database Countries table fields
data4.columns=["countryName", "AlphaCases"]
#merge two tables
data5 = data3.merge(data4, on = "countryName", how = "left")
#read data from csv file, only retaining Country and Population
data6 = pd.read_csv("BetacountrySubmissionCount.csv", usecols=["Country", "Total #Beta GH/501Y.V2 (B.1.351+B.1.351.2+B.1.351.3)"])
#rename columns to be compatible with database Countries table fields
data6.columns=["countryName", "BetaCases"]
#merge two tables
data7 = data5.merge(data6, on = "countryName", how = "left")
#read data from csv file, only retaining Country and Population
data8 = pd.read_csv("GammacountrySubmissionCount.csv", usecols=["Country", "Total #Gamma GR/501Y.V3 (P.1+P.1.*)"])
#rename columns to be compatible with database Countries table fields
data8.columns=["countryName", "GammaCases"]
#merge two tables
data9 = data7.merge(data8, on = "countryName", how = "left")
#read data from csv file, only retaining Country and Population
data10 = pd.read_csv("LambdacountrySubmissionCount.csv", usecols=["Country", "Total #Lambda GR/452Q.V1 (C.37+C.37.1)"])
#rename columns to be compatible with database Countries table fields
data10.columns=["countryName", "LambdaCases"]
#merge two tables
data11 = data9.merge(data10, on = "countryName", how = "left")
#read data from csv file, only retaining Country and Population
data12 = pd.read_csv("MucountrySubmissionCount.csv", usecols=["Country", "Total #Mu GH (B.1.621+B.1.621.1)"])
#rename columns to be compatible with database Countries table fields
data12.columns=["countryName", "MuCases"]
#merge two tables
data = data11.merge(data12, on = "countryName", how = "left")
#append to database
data.to_sql(name="Countries", con=con, if_exists='replace', index=False)

res = cur.execute("SELECT * FROM countries")

print(res.fetchall())