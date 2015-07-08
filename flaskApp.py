from flask.ext.mysqldb import MySQL
from flask.ext.bcrypt import Bcrypt
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify

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
    	return render_template('layout.html')

#API Routes
@app.route('/api/products')
def show_products_api():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM product''')
	entries = [dict(prod_id=row[0], prod_name=row[1], cat_id=row[2]) for row in cur.fetchall()]
    	return jsonify(products=entries)

@app.route('/api/categories')
def show_categories_api():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM category''')
	entries = [dict(cat_id=row[0], cat_name=row[1]) for row in cur.fetchall()]
    	return jsonify(categories=entries)

@app.route('/api/suppliers')
def show_suppliers_api():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM supplier''')
	entries = [dict(supplier_id=row[0], supplier_name=row[1]) for row in cur.fetchall()]
    	return jsonify(suppliers=entries)

@app.route('/api/sales')
def show_sales_api():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT sale_id, prod_name, day, date, qtySold, salePrice FROM product, \
        sales WHERE product.prod_id = sales.prod_id ''')
	entries = [dict(sale_id=row[0], prod_name=row[1], day = row[2], date = str(row[3]),\
        qtySold = row[4], salePrice = str(row[5])) for row in cur.fetchall()]
    	return jsonify(sales=entries)

@app.route('/api/purchases')
def show_purchases_api():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT purchase_id, prod_name, date, quantity, cost, totalCost from \
        purchases, product WHERE purchases.prod_id = product.prod_id order by purchase_id''')
	entries = [dict(purchase_id=row[0], prod_name=row[1], date = str(row[2]), \
        quantity = row[3], cost = str(row[4]), totalCost = str(row[5])) for row in cur.fetchall()]
    	return jsonify(purchases=entries)

if __name__ == '__main__':

	app.run(debug=True,
	host="172.18.0.224",
    port=int("5000"))
