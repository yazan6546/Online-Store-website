from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'  # or your MySQL server address
app.config['MYSQL_USER'] = 'root'  # your MySQL username
app.config['MYSQL_PASSWORD'] = 'osaid'  # your MySQL password
app.config['MYSQL_DB'] = 'store'  # your database name

mysql = MySQL(app)


@app.route('/')
def index():
    # Using context manager to handle the connection and cursor
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Product')
    products = cursor.fetchall()
    return render_template('index.html', products=products)


@app.route('/add', methods=['POST'])
def add_product():
    if request.method == 'POST':
        product_name = request.form['product_name']
        stock_quantity = request.form['stock_quantity']
        price = request.form['price']
        category_ID = request.form['category_ID']
        description = request.form['description']

        try:
            # Using context manager to handle connection and cursor automatically
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Product (product_name, stock_quantity, price, category_ID, description)
                VALUES (%s, %s, %s, %s, %s)
            ''', (product_name, stock_quantity, price, category_ID, description))
            conn.commit()
        except Exception as e:
            print(f"Error: {e}")
        return redirect(url_for('index'))


@app.route('/update/<int:id>', methods=['POST'])
def update_product(id):
    if request.method == 'POST':
        product_name = request.form['product_name']
        stock_quantity = request.form['stock_quantity']
        price = request.form['price']
        category_ID = request.form['category_ID']
        description = request.form['description']

        try:
            # Using context manager to handle connection and cursor automatically
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE Product
                SET product_name = %s, stock_quantity = %s, price = %s, category_ID = %s, description = %s
                WHERE product_ID = %s
            ''', (product_name, stock_quantity, price, category_ID, description, id))
            conn.commit()
        except Exception as e:
            print(f"Error: {e}")
        return redirect(url_for('index'))


@app.route('/delete/<int:id>', methods=['GET'])
def delete_product(id):
    try:
        # Using context manager to handle connection and cursor automatically
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Product WHERE product_ID = %s', (id,))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
    return redirect(url_for('index'))


@app.route('/search', methods=['GET'])
def search_product():
    search_query = request.args.get('query')

    if search_query:
        try:
            # Using context manager to handle connection and cursor automatically
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM Product
                WHERE product_name LIKE %s OR description LIKE %s
            ''', ('%' + search_query + '%', '%' + search_query + '%'))
            products = cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            products = []
    else:
        products = []

    return render_template('index.html', products=products)


if __name__ == '__main__':
    app.run(debug=True)
