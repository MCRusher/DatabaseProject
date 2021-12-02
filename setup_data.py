import sqlite3 as sql
import pandas as pd
from os.path import exists
from os import remove

#removes existing database if it exists
if exists("data.db"):
    remove("data.db")

#creates new database
con = sql.connect("data.db")

cur = con.cursor()

#loads sql script file for initializing the database
with open("schema.sql", "r") as sql_file:
    sql_script = sql_file.read()
    #executes intialization script to create the intial database tables
    cur.executescript(sql_script)

#read data from csv file, only retaining Country and Population
data = pd.read_csv("datasets/population_by_country_2020.csv", usecols=["Country (or dependency)", "Population (2020)"])
#rename columns to be compatible with database Countries table fields
data.columns=["countryName", "population"]
#fill countries table with names and populations from csv file
data.to_sql(name="Countries", con=con, if_exists="append", index=False)

#add covid cases and deaths info to tables
data = pd.read_csv("datasets/country_wise_latest.csv", usecols=["Country/Region", "Deaths"])
for row in data.iterrows():
    c_name = row[1][0]
    deaths = row[1][1]
    if c_name == "US":#prevent different name for the United States from breaking database
        c_name = "United States"
    cur.execute("""
    UPDATE Countries
    SET deaths = ?
    WHERE countryName = ?;
    """, (deaths, c_name,))

data = pd.read_csv("datasets/vaccinations.csv", usecols=["location", "people_vaccinated"]).groupby("location").max()

for row in data.iterrows():
    c_name = row[0]
    vaccinated = row[1][0]
    cur.execute("""
    UPDATE Countries
    SET vaccinated = ?
    WHERE countryName = ?;
    """, (vaccinated, c_name,))

#discovery date data manually pulled from
# https://www.who.int/en/activities/tracking-SARS-CoV-2-variants/
# data on gh/490r is limited and the discovery date is approximated using gisaid
cur.execute("""
INSERT INTO Variants(variantName, dateOfDiscovery)
VALUES
("omicron", "11/24/2021"),
("gh490r", "9/13/2021"),
("delta", "4/4/2021"),
("alpha", "12/18/2020"),
("beta", "12/18/2020"),
("gamma", "1/11/2021"),
("lambda", "6/14/2021"),
("mu", "8/30/2021");
""")

variants = ["omicron", "gh490r", "delta", "alpha", "beta", "gamma", "lambda", "mu"]

for variant in variants:
    data = pd.read_csv("datasets/%s.csv" % variant, usecols=[0, 1])
    for row in data.iterrows():
        #country: row[1][0]
        #total cases: row[1][1]
        c_name = row[1][0]
        total_cases = str(row[1][1]).replace(",","")
        print("total: %s" % total_cases)
        if c_name == "USA":#prevent different name for the United States from breaking database
            c_name = "United States"
        #print("c_name: %s" % c_name)
        try:
            cur.execute("""
            INSERT INTO VariantSpreadInCountries(variantID, countryID, cases)
            VALUES
            (
                (SELECT variantID FROM Variants WHERE variantName = ?),
                (SELECT countryID FROM Countries WHERE countryName = ?),
                ?
            );
            """, (variant, c_name, total_cases,))
        except sql.IntegrityError:#country doesn't exist in the countries table, so skip it
            continue
con.commit()
