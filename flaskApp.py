from flask.ext.mysqldb import MySQL
from flask.ext.bcrypt import Bcrypt
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

app = Flask(__name__)
bcrypt = Bcrypt(app)
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
    return render_template('land.html')

@app.route('/signUp', methods = ['GET', 'POST'])
def signUp():
	if request.method == 'POST':
		if(request.form['password'] == request.form['password2']):
			pw_hash = bcrypt.generate_password_hash(request.form['password'],10)
			cur = mysql.connection.cursor()
			cur.execute('''INSERT INTO users VALUES (%s, %s) ''', (request.form['username'], pw_hash))
			mysql.connection.commit()
			return redirect(url_for('login'))
		else:
			return render_template('signUp.html', msg = "Passwords do not match")
	else:
    		return render_template('signUp.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		cur = mysql.connection.cursor()
		cur.execute('''SELECT password FROM users WHERE username = \"%s\" ''' %request.form['username'])
		entries = [dict(password=row[0]) for row in cur.fetchall()]

		if entries != [] and request.form['username'] != None and request.form['password'] != None:
			pw_hash = entries[0]['password']
			if bcrypt.check_password_hash(pw_hash, request.form['password']):
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

@app.route('/products', methods=['GET', 'POST'])
def show_products():
    if request.method == 'POST':
    	if(request.form['prod_name'] != ""):
    			cur = mysql.connection.cursor()
    			cur.execute('''INSERT INTO product SET prod_name = %s, cat_id = %s''', (request.form['prod_name'], request.form["cat_id"] ))
    			mysql.connection.commit()
    			return redirect(url_for('show_products'))
        else:
                cur = mysql.connection.cursor()
            	cur.execute('''SELECT * FROM product''')
            	entries = [dict(prod_id=row[0], prod_name=row[1], cat_id=row[2]) for row in cur.fetchall()]
                cur.execute('''SELECT * FROM category''')
                catEntries = [dict(cat_id=row[0], cat_name=row[1]) for row in cur.fetchall()]
            	return render_template('show_products.html', entries=entries, catEntries = catEntries, msg = "field cannot be blank")
    else:
        	cur = mysql.connection.cursor()
        	cur.execute('''SELECT * FROM product''')
        	entries = [dict(prod_id=row[0], prod_name=row[1], cat_id=row[2]) for row in cur.fetchall()]
                cur.execute('''SELECT * FROM category''')
                catEntries = [dict(cat_id=row[0], cat_name=row[1]) for row in cur.fetchall()]
                return render_template('show_products.html', entries=entries, catEntries = catEntries)

@app.route('/categories', methods=['GET', 'POST'])
def show_categories():
    if request.method == 'POST':
    	if(request.form['cat_name'] != ""):
    			cur = mysql.connection.cursor()
    			cur.execute('''INSERT INTO category VALUES (%s) ''' %(request.form['cat_name']))
    			mysql.connection.commit()
    			return redirect(url_for('show_categories'))
        else:
                cur = mysql.connection.cursor()
            	cur.execute('''SELECT * FROM category''')
            	entries = [dict(cat_id=row[0], cat_name=row[1]) for row in cur.fetchall()]
                return render_template('show_categories.html', entries=entries, msg = "field cannot be blank")
    else:
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

@app.route('/sales')
def show_sales():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT sale_id, prod_name, day, date, qtySold, salePrice FROM product, sales WHERE product.prod_id = sales.prod_id ''')
	entries = [dict(sale_id=row[0], prod_name=row[1], day = row[2], date = row[3], qtySold = row[4], salePrice = row[5]) for row in cur.fetchall()]
    	return render_template('show_sales.html', entries=entries)

@app.route('/purchases')
def show_purchases():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT purchase_id, prod_name, date, quantity, cost, totalCost from purchases, product WHERE purchases.prod_id = product.prod_id order by purchase_id''')
	entries = [dict(purchase_id=row[0], prod_name=row[1], date = row[2], quantity = row[3], cost = row[4], totalCost = row[5]) for row in cur.fetchall()]
    	return render_template('show_purchases.html', entries=entries)

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
