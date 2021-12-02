from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3 as sql
app = Flask(__name__)

@app.route("/")
def home(): 
	return render_template('page2.html', hide_table = True)
    
@app.route("/next2/", methods = ['GET','POST'])
def next2():
    if request.method == "GET":
        searched = request.args.get("user_input")
        con = sql.connect('data.db')
        cur = con.cursor()
        if searched == None or len(searched)<=0:
            print("No input")
            return render_template('page2.html', show_table = False)
        else:
            countries = cur.execute("""
            SELECT countryName
            FROM Countries
            WHERE countryName LIKE ?
            """,('%'+searched+'%',)).fetchall()
            if(len(countries)<=0):
                error = "SORRY ! NO COUNTRY FOUND."
                return render_template('page2.html', error = error, show_table = False)
            return render_template('page2.html', similar = countries, show_table = True)
    
    
@app.route("/next3/<string:c_name>")
def next3(c_name): 
        con = sql.connect('data.db')
        cur = con.cursor()
        
        (c_pop, c_vaccinated, c_deaths) = con.execute("SELECT population, vaccinated, deaths FROM Countries WHERE countryName = ?", (c_name,)).fetchone()
        
        #provide sensible default values for possibly null fields
        c_vaccinated = c_vaccinated or "Unknown"
        c_deaths = c_deaths or "Unknown"
        
        variant_data = con.execute("""
        SELECT V.variantName, V.dateOfDiscovery, VS.cases
        FROM Countries AS C
        JOIN VariantSpreadInCountries AS VS
            ON C.countryId = VS.countryId
        JOIN Variants AS V
            ON VS.variantId = V.variantId
        WHERE C.countryName = ?
        """,(c_name,)).fetchall()
        
        max_variant = con.execute("""
        SELECT V.variantName, V.dateOfDiscovery, MAX(VS.cases)
        FROM Countries AS C
        JOIN VariantSpreadInCountries AS VS
            ON C.countryId = VS.countryId
        JOIN Variants AS V
            ON VS.variantId = V.variantId
        WHERE C.countryName = ?
        """,(c_name,)).fetchone()
       
        return render_template('page3.html', name=c_name, pop=c_pop, vaccinated=c_vaccinated, deaths=c_deaths, variants=variant_data, max=max_variant)

if __name__ == "__main__":
    app.run(debug=True)