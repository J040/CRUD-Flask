import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test2.sqlite3'
db = SQLAlchemy(app)

# TABLE PRODUCTS
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.Float)
    discount_percent = db.Column(db.Integer)
    image = db.Column(db.String)

    def __init__(self, name, description, price, discount_percent, image):
        self.name = name
        self.description = description
        self.price = price
        self.discount_percent = discount_percent
        self.image = image

    def __repr__(self):
        return "<Product(name='%s', description='%s', price='%s', discount_percent='%s')>" % (self.name, self.description, self.price, self.discount_percent)

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        discount_percent = request.form['discount_percent']
        image = request.form['image']
        
        if price == '':
            price = 0
        if discount_percent == '':
            discount_percent = 0
                        
        product = Product(name, description, price, discount_percent, image)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>',  methods=['GET', 'POST'])
def edit(id):
    product = Product.query.get(id)
    if request.method == "POST":
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = request.form['price']
        product.discount_percent = request.form['discount_percent']
        product.image = request.form['image']

        if product.price == '':
            product.price = 0
        if product.discount_percent == '':
            product.discount_percent = 0

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', product=product)


@app.route('/delete/<int:id>')
def delete(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)