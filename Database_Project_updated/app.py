from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3 as sql
app = Flask(__name__)

@app.route("/")
def home(): 
	return render_template('search.html')


@app.route("/next/", methods = ['GET','POST'])
def next(): 
    if request.method == "GET": 
        con = sql.connect('data.db')
        cur = con.cursor()
        user_input = request.args.get("user_input")
        if len(user_input)<=0:
            print("No input")
            return render_template('search.html')
        else:
            query ="SELECT * FROM Countries WHERE countryName LIKE ?"
            result = cur.execute(query, ('%'+user_input+'%',))
            con.commit()
            result = cur.fetchall()	
            if(len(result)<=0):
                error = "SORRY ! NO DATA FOUND."
                return render_template('page2.html', error = error)
                
            return render_template('page2.html', result = result)
    
@app.route("/next2/", methods = ['GET','POST'])
def next2(): 
    if request.method == "GET": 
        con = sql.connect('data.db')
        cur = con.cursor()
        user_input2 = request.args.get("user_input2")
        if len(user_input2)<=0:
            print("No input")
            return render_template('page2.html')
        else:
            query ="SELECT * FROM Countries WHERE countryName LIKE ?"
            result = cur.execute(query, ('%'+user_input2+'%',))
            con.commit()
            result = cur.fetchall()	
            if(len(result)<=0):
                error = "SORRY ! NO DATA FOUND."
                return render_template('page2.html', error = error)
                
            return render_template('page2.html', result = result)
    
    
@app.route("/next3/<string:c_name>")
def next3(c_name): 
        con = sql.connect('data.db')
        link = c_name
       # return "okay: from here nad ----> %s" %c_name
        cur_link = con.cursor()
        cur_variant = con.cursor()
        query = "SELECT *  FROM Countries WHERE countryName = ?"
        query_variant = "SELECT CAST(DeltaCases AS money), CAST(AlphaCases AS money), CAST(BetaCases AS money), CAST(GammaCases AS money), CAST(LambdaCases AS money), CAST(MuCases AS money) as okay FROM Countries where countryName = ?" 
        
 
        result = cur_link.execute(query, (link,))
        highest_variant = cur_variant.execute(query_variant, (link,))
        con.commit()
        result = cur_link.fetchall()
        highest = 0
        delta_var = 0
        alpha_var = 0
        beta_var = 0 
        gamma_var = 0
        lambda_var = 0
        mu_var = 0
        
        count  = 0
       
        highest_variant = cur_variant.fetchall()
       
        return render_template('page3.html', result = result, link = link, most_var = highest_variant)
    

if __name__ == "__main__":
    app.run(debug=True)