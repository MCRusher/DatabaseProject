from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3 
app = Flask(__name__)
app.secret_key = "#$%#$%^%^BFGBFGBSFGNSGJTNADFHH@#%$%#T#FFWF$^F@$F#$FW"


@app.route("/")
def home(): 
	return render_template('search.html')


@app.route('/my-link/')
def my_link():
  print ('I got clicked!')
  return 'Click.'
 
@app.route('/searched/',methods = ["POST","GET"])
def searched(): 
	try: 
		if request.method == "GET":
			form = request.args.get("query")
			conn = sqlite3.connect('countries.db')
			mycursor = conn.cursor()
			sql = "SELECT Country, Population FROM countries WHERE Country LIKE '%{n}%'".format(n = form)
			result = mycursor.execute(sql)
			result = mycursor.fetchall()	
			return render_template("nextPage.html",result=result)
	except:
		return render_template("nextPage.html", result = "")

		#rows = cursor.fetchall()
	#return render_template("nextPage.html", rows=rows)
	
 
  
if __name__ == "__main__":
	app.run(debug=True)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	