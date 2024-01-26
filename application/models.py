from application.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(10), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=True)
    role = db.Column(db.String(50), nullable=False, default="customer")

    def __init__(self, name, phone, email, password, address, role):
        self.name = name
        self.phone = phone
        self.email = email
        self.password = password
        self.address = address
        self.role = role

    def __repr__(self):
        return '<User %r>' % self.name
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'password': self.password,
            'address': self.address,
            'role': self.role
        }

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    products = db.relationship('Product', backref='category', lazy=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Category %r>' % self.name
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __init__(self, name, description, quantity, price, category_id):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.price = price
        self.category_id = category_id

    def __repr__(self):
        return '<Product %r>' % self.name
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'quantity': self.quantity,
            'price': self.price,
            'category_id': self.category_id
        }
    
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    is_ordered = db.Column(db.Boolean, nullable=False, default=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=True)

    def __init__(self, user_id, product_id, quantity):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity

    def __repr__(self):
        return '<Cart %r>' % self.id
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'is_ordered': self.is_ordered
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    carts = db.relationship('Cart', backref='order', lazy=True)

    def __init__(self, user_id, total_price):
        self.user_id = user_id
        self.total_price = total_price

    def __repr__(self):
        return '<Order %r>' % self.id
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'total_price': self.total_price
        }