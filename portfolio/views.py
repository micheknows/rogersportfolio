from flask import Flask, request, jsonify
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)

class PortfolioItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(50), nullable=True)

@app.route('/portfolio', methods=['GET'])
def portfolio_list():
    portfolio_items = PortfolioItem.query.all()
    return jsonify([{'id': item.id, 'title': item.title} for item in portfolio_items])

@app.route('/portfolio', methods=['POST'])
@login_required
def portfolio_create():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    image_url = data.get('image_url')
    category = data.get('category')
    item = PortfolioItem(title=title, description=description, image_url=image_url, category=category)
    db.session.add(item)
    db.session.commit()
    return jsonify({'id': item.id, 'title': item.title})

@app.route('/portfolio/<int:item_id>', methods=['GET'])
def portfolio_get(item_id):
    item = PortfolioItem.query.get_or_404(item_id)
    return jsonify({'id': item.id, 'title': item.title, 'description': item.description,
                    'image_url': item.image_url, 'category': item.category})

@app.route('/portfolio/<int:item_id>', methods=['PUT'])
@login_required
def portfolio_update(item_id):
    item = PortfolioItem.query.get_or_404(item_id)
    data = request.json
    item.title = data.get('title', item.title)
    item.description = data.get('description', item.description)
    item.image_url = data.get('image_url', item.image_url)
    item.category = data.get('category', item.category)
    db.session.commit()
    return jsonify({'id': item.id, 'title': item.title})

@app.route('/portfolio/<int:item_id>', methods=['DELETE'])
@login_required
def portfolio_delete(item_id):
    item = PortfolioItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return '', 204
