from flask.ext.mysqldb import MySQL
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

app.secret_key = 'd4rthV4d3rIsYourF4th3r'

mysql = MySQL(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'coder123'
app.config['MYSQL_DB'] = 'nelisaFlask'
#	app.config['MYSQL_CHARSET'] = 'utf-8'

@app.route('/')
def show_landing():
	if request.method == 'POST':
		data = {username: request.form['username'],
				password: request.form['password']}
		cur = mysql.connection.cursor()
		cur.execute('''INSERT INTO users SET %s ''' %data)
		entries = [dict(password=row[0]) for row in cur.fetchall()]
	else:	
    		return render_template('land.html')

@app.route('/signUp', methods = ['GET', 'POST'])
def signUp():
	if request.method == 'POST':
		cur = mysql.connection.cursor()
		cur.execute('''INSERT INTO users VALUES (%s, %s) ''', (request.form['username'], request.form['password']))
		mysql.connection.commit()
		return redirect(url_for('login'))
	else:	
    		return render_template('signUp.html')    

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		cur = mysql.connection.cursor()
		cur.execute('''SELECT password FROM users WHERE username = \"%s\" ''' %request.form['username'])
		entries = [dict(password=row[0]) for row in cur.fetchall()]
		
		if entries != [] and request.form['username'] != None and request.form['password'] != None:
			if request.form['password'] == entries[0]['password']:
			    session['name'] = request.form['username']
			    # And then redirect the user to the main page
			    return redirect(url_for('show_menu'))
			elif request.form['password'] != entries[0]['password']:
				return render_template('login.html', msg = "Incorrect Login")
	    	else:
	    		return render_template('login.html', msg = "Incorrect Login")			
	else:
		if session:
			return redirect(url_for('show_menu'))
		else:
			return render_template('login.html')
	    		return render_template('login.html')
        

@app.route('/menu')
def show_menu():
    return render_template('menu.html')

@app.route('/products')
def show_products():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM product''')
	entries = [dict(prod_id=row[0], prod_name=row[1], cat_id=row[2]) for row in cur.fetchall()]
    	return render_template('show_products.html', entries=entries)

@app.route('/categories')
def show_categories():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM category''')
	entries = [dict(cat_id=row[0], cat_name=row[1]) for row in cur.fetchall()]
    	return render_template('show_categories.html', entries=entries)    

@app.route('/suppliers')
def show_suppliers():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM supplier''')
	entries = [dict(supplier_id=row[0], supplier_name=row[1]) for row in cur.fetchall()]
    	return render_template('show_suppliers.html', entries=entries)    	    		

@app.route('/clear')
def clearsession():
    # Clear the session
    session.clear()
    # Redirect the user to the main page
    return redirect(url_for('login'))

if __name__ == '__main__':
	
	app.run(debug=True, 
	host="172.18.0.224",
    port=int("5000"))