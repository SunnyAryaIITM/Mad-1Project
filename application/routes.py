from application import app
from flask import flash, redirect, render_template, request, session, url_for
from application.database import db

from application.models import Cart, Category, Order, Product, User
from application.variables import *

@app.route('/')
def index():
    categories = Category.query.all()
    return render_template('index.html', categories = categories)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        user = User(name, phone, email, password, address, CUSTOMER)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html') 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user'] = user.to_dict()
            if user.role == "super_admin":
                return redirect(url_for('super_admin'))
            elif user.role == "admin":
                return redirect(url_for('admin'))
            elif user.role == "customer":
                return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/super_admin')
def super_admin():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != "super_admin":
        return redirect(url_for('login'))
    return render_template('superAdmin.html')

@app.route('/admin_register', methods=['POST'])
def admin_register():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] != "super_admin":
        return redirect(url_for('login'))
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    password = request.form['password']
    address = request.form['address']
    user = User(name, phone, email, password, address, ADMIN)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('super_admin'))

@app.route('/admin')
def admin():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] == CUSTOMER:
        return redirect(url_for('login'))
    categories = Category.query.all()
    return render_template('admin.html', categories=categories)

@app.route('/add_category', methods=['POST'])
def add_category():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] == CUSTOMER:
        return redirect(url_for('login'))
    name = request.form['category']
    description = request.form['description']
    category = Category(name, description)
    db.session.add(category)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/add_product', methods=['POST'])
def add_product():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] == CUSTOMER:
        return redirect(url_for('login'))
    name = request.form['product']
    description = request.form['description']
    quantity = request.form['quantity']
    price = request.form['price']
    category = request.form['category']
    product = Product(name, description, quantity, price, category)
    category = Category.query.filter_by(id=category).first()
    category.products.append(product)
    db.session.add(product)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/delete_category', methods=['POST'])
def delete_category():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] == CUSTOMER:
        return redirect(url_for('login'))
    category_id = request.form['category_id']
    category = Category.query.filter_by(id=category_id).first()
    for product in category.products:
        db.session.delete(product)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/delete_product', methods=['POST'])
def delete_product():
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] == CUSTOMER:
        return redirect(url_for('login'))
    product_id = request.form['product_id']
    product = Product.query.filter_by(id=product_id).first()
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] == CUSTOMER:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['product']
        description = request.form['description']
        quantity = request.form['quantity']
        price = request.form['price']
        product = Product.query.filter_by(id=id).first()
        product.name = name
        product.description = description
        product.quantity = quantity
        product.price = price
        db.session.commit()
        return redirect(url_for('admin'))
    product = Product.query.filter_by(id=id).first()
    print(product.category_id)
    return render_template('update.html', product=product, categories=Category.query.all(), update_type="product")

@app.route('/edit_category/<int:id>', methods=['GET', 'POST'])
def update_category(id):
    if not session.get('user'):
        return redirect(url_for('login'))
    if session.get('user')['role'] == CUSTOMER:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['category']
        description = request.form['description']
        category = Category.query.filter_by(id=id).first()
        category.name = name
        category.description = description
        db.session.commit()
        return redirect(url_for('admin'))
    category = Category.query.filter_by(id=id).first()
    return render_template('update.html', category=category, update_type="category")

@app.route('/add-to-cart', methods=['POST'])
def addToCart():
    if not session.get('user'):
        return redirect(url_for('login'))
    product_id = request.form['product_id']
    quantity = request.form['quantity']
    product = Product.query.filter_by(id=product_id).first()
    if product.quantity < int(quantity):
        flash('Quantity not available')
        return redirect(url_for('index'))
    cart = Cart.query.filter_by(user_id=session.get('user')['id'], product_id=product_id).first()
    if cart:
        cart.quantity+=int(quantity)
        product.quantity -= int(quantity)
        db.session.commit()
        flash('Item added to cart')
        return redirect(url_for('index'))
    cart = Cart(session.get('user')['id'], product_id, quantity)
    product.quantity -= int(quantity)
    db.session.add(cart)
    db.session.commit()
    flash('Item added to cart')
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    if not session.get('user'):
        return redirect(url_for('login'))
    carts = Cart.query.filter_by(user_id=session.get('user')['id'], is_ordered=False).all()
    products = Product.query.filter(Product.id.in_([cart.product_id for cart in carts])).all()
    return render_template('cart.html', carts=carts, products=products)

@app.route('/delete-from-cart/<int:id>', methods=['GET', 'POST'])
def deleteFromCart(id):
    if not session.get('user'):
        return redirect(url_for('login'))
    cart = Cart.query.filter_by(id=id).first()
    product = Product.query.filter_by(id=cart.product_id).first()
    product.quantity += cart.quantity
    db.session.delete(cart)
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/order')
def order():
    if not session.get('user'):
        return redirect(url_for('login'))
    user = User.query.filter_by(id=session.get('user')['id']).first()
    carts = Cart.query.filter_by(user_id=session.get('user')['id']).all()
    order = Order(session.get('user')['id'], 0)
    for cart in carts:
        cart.is_ordered = True
        product = Product.query.filter_by(id=cart.product_id).first()
        order.total_price += product.price * cart.quantity
        order.carts.append(cart)
        db.session.add(order)
        db.session.commit()
    return render_template('order.html', order=order)