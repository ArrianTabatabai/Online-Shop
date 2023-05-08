from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    impact = db.Column(db.Integer, nullable=False)

@app.route('/')
def home():
    sort_type = request.args.get('sort')
    if sort_type == 'name':
        products = Product.query.order_by(Product.name).all()
    elif sort_type == 'price':
        products = Product.query.order_by(Product.price).all()
    elif sort_type == 'impact':
        products = Product.query.order_by(Product.impact).all()
    else:
        products = Product.query.all()
    return render_template('front_page.html', products=products, Product=Product)

@app.route('/fidget_spinner')
def fidget_spinner():
    product = Product.query.filter_by(name='Fidget Spinner').first()
    return render_template('fidget_spinner.html', product=product)

@app.route('/fidget_cube')
def fidget_cube():
    product = Product.query.filter_by(name='Fidget Cube').first()
    return render_template('fidget_cube.html', product=product)

@app.route('/water_bottle')
def water_bottle():
    product = Product.query.filter_by(name='Water Bottle').first()
    return render_template('water_bottle.html', product=product)

@app.route('/loom_bands')
def loom_bands():
    product = Product.query.filter_by(name='Loom Bands').first()
    return render_template('loom_bands.html', product=product)

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/finished')
def finished():
    return render_template('finished.html')

@app.route('/add-to-basket', methods=['POST'])
def add_to_basket():
    product_id = request.form['product_id']
    product = Product.query.get(product_id)
    basket = session.get('basket', [])
    basket.append(product.name)
    session['basket'] = basket
    return redirect(url_for('home'))

@app.route('/clear-basket', methods=['POST'])
def clear_basket():
    session['basket'] = []
    return redirect(url_for('home'))

@app.context_processor
def calculate_total():
    def _calculate_total():
        total = 0
        basket = session.get('basket', [])
        for item in basket:
            product = Product.query.filter_by(name=item).first()
            total += product.price
        return total
    return dict(calculate_total=_calculate_total)

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        if len(Product.query.all()) != 0:
            app.run(debug=True)
        else:
            fidget_spinner = Product(name='Fidget Spinner', price=7.0, image='fidget_spinner.jpg', impact=3)
            fidget_cube = Product(name='Fidget Cube', price=9.0, image='fidget_cube.jpg', impact=2)
            water_bottle = Product(name='Water Bottle', price=2.0, image='water_bottle.jpg', impact=3)
            loom_bands = Product(name='Loom Bands', price=13.0, image='loom_bands.jpg', impact=1)
            db.session.add_all([fidget_spinner, fidget_cube, water_bottle, loom_bands])
            db.session.commit()

            app.run(debug=True)
