from flask import Flask, render_template, request, jsonify, redirect, url_for
import database
from product import Product

db = database.conectar_base_de_datos()

app = Flask(__name__)


# Rutas de la aplicación
@app.route('/')
def home():
    products = db['products']
    productsReceived = products.find()
    return render_template('index.html', products=productsReceived)


# Método POST
@app.route('/products', methods=['POST'])
def addProduct():
    products = db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']

    if name and price and quantity:
        product = Product(name, price, quantity)
        products.insert_one(product.toDBCollection())
        result = redirect(url_for('home'))
    else:
        result = notFound()
    return result


# Método delete
@app.route('/delete/<string:product_name>')
def delete(product_name):
    products = db['products']
    products.delete_one({'name': product_name})
    return redirect(url_for('home'))


# Método edit (los formularios HTML solo permiten POST)
@app.route('/edit/<string:product_name>', methods=['POST'])
def edit(product_name):
    products = db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']

    if name and price and quantity:
        products.update_one(
            {'name': product_name},
            {'$set': {'name': name, 'price': price, 'quantity': quantity}}
        )
        result = redirect(url_for('home'))
    else:
        result = notFound()
    return result


@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ == '__main__':
    app.run(debug=True, port=4000)