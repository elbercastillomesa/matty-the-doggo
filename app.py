from flask import Flask, jsonify, render_template, request, Response, jsonify, redirect, url_for
from pymongo import MongoClient
import database as dbase
from product import Product

app = Flask(__name__)
client = MongoClient('mongo-db', 27017)
db = dbase.dbConnection()
# db = client.test_database

@app.route('/')
def home():
    products = db['products']
    productsReceived = products.find()
    return render_template('index.html', products = productsReceived)

# Application Routes

## POST Method
@app.route('/products', methods=['POST'])
def addProduct():
    products = db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']

    if name and price and quantity:
        product = Product(name, price, quantity)
        products.insert_one(product.toDBCollection())
        response = jsonify(
            {
                'name': name,
                'price': price,
                'quantity': quantity,
            }
        )
        return redirect(url_for('home'))
    else:
        return notFound()

## DELETE Method
@app.route('/delete/<string:product_name>')
def delete(product_name):
    products = db['products']
    products.delete_one(
        {
            'name': product_name
        }
    )
    return redirect(url_for('home'))

## PUT Method
@app.route('/edit/<string:product_name>', methods=['POST'])
def edit(product_name):
    products = db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']

    if name and price and quantity:
        products.update_one(
            {
                'name': product_name,
            },
            {
                '$set':
                {
                    'name': name,
                    'price': price,
                    'quantity': quantity,
                }                
            }
        )
        response = jsonify(
            {
                'message': 'Product ' + product_name + ' Updated.'
            }
        )
        return redirect(url_for('home'))
    else:
        return notFound()   

@app.errorhandler(404)
def notFound(error = None):
    message = {
        'message': 'Not found ' + request.url,
        'status': '404 Not Found',
    }
    response = jsonify(message)
    response.status_code = 404
    return response

@app.route('/users')
def get_users():
    users = list(db.users.find())
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
