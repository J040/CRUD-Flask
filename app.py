from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
import jinja2

app = Flask(__name__, template_folder='templates')

app.jinja_env.filters['zip'] = zip
app.jinja_env.filters['now'] = datetime.now().date()

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.sqlite3'
db = SQLAlchemy(app)

# TABLE PRODUCTS
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.Numeric(10,2))
    price_float = db.Column(db.Float)
    image = db.Column(db.String)

    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return "<Product(name='%s', description='%s', price='%s')>" % (self.name, self.description, self.price)

# TABLE DISCOUNT
class Discount(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    begin_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    remaining_days = db.Column(db.Integer)
    discount_percent = db.Column(db.Integer)

    id_product = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product', backref=db.backref('discount', lazy=True))

    def __init__(self, **kwargs):
        super(Discount, self).__init__(**kwargs)

    def __repr__(self):
        return "<Discount(begin_date='%s', end_date='%s', discount_percent='%s')>" % (self.begin_date, self.end_date, self.discount_percent)

@app.route('/')
def index():
    products = Product.query.all()
    discounts = Discount.query.all()
    for d in discounts:
        d.remaining_days = abs( d.end_date.date() - datetime.now().date() ).days
        db.session.commit()

    return render_template('index.html', products=products, discounts=discounts, now=datetime.now().date())

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        image = request.form['image']
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        discount_percent = request.form['discount_percent']
        remaining_days = 0

        if request.form['begin_date'] == '':
            begin_date = datetime.now().date()
        else:
            begin_date = datetime.strptime(request.form['begin_date'], '%Y-%m-%d').date()

        if request.form['end_date'] == '':
            end_date = datetime.now().date()
        else:
            end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()

        if discount_percent == '':
            discount_percent = 0

        if begin_date > end_date:
            return render_template('edit_add.html', add=True, wrong_date=True)

        if price == '':
            price = 0

        price_float = float(price)
        
        product = Product(name=name, description=description, price=price, price_float=price_float, image=image)
        Discount(begin_date=begin_date, end_date=end_date, discount_percent=discount_percent, product=product, remaining_days=remaining_days)        

        db.session.add(product)
        db.session.commit()
        discounts = Discount.query.first()

        return redirect(url_for('index'))

    return render_template('edit_add.html', add=True)

@app.route('/edit/<int:id>',  methods=['GET', 'POST'])
def edit(id):

    product = Product.query.get(id)
    discount = Discount.query.filter_by(id_product=id).first()

    if request.method == "POST":
        product.image = request.form['image']
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = request.form['price']
        product.price_float = product.price

        discount.discount_percent = request.form['discount_percent']

        if request.form['end_date'] == '':
            discount.end_date = datetime.now().date()
        else:
            discount.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()

        if request.form['begin_date'] == '':
            discount.begin_date = datetime.now().date()
        else:
            discount.begin_date = datetime.strptime(request.form['begin_date'], '%Y-%m-%d').date()

        if discount.discount_percent == '':
            discount.discount_percent = 0

        if product.price == '':
            product.price = '0'
            product.price_float = '0'

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_add.html', product=product, discount=discount)


@app.route('/delete/<int:id>')
def delete(id):
    product = Product.query.get(id)
    discount = Discount.query.filter_by(id_product=id).first()
    db.session.delete(product)
    db.session.delete(discount)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)