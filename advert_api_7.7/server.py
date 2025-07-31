from flask import Flask, request, jsonify
from models import db, Advert, AdvertSchema
from errors import InvalidAPIUsage
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adverts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
advert_schema = AdvertSchema()
adverts_schema = AdvertSchema(many=True)

@app.route('/adverts', methods=['GET'])
def get_adverts():
    adverts = Advert.query.all()
    return jsonify(adverts_schema.dump(adverts))

@app.route('/adverts/<int:advert_id>', methods=['GET'])
def get_advert(advert_id):
    advert = Advert.query.get(advert_id)
    if advert is None:
        raise InvalidAPIUsage('Advert not found', 404)
    return jsonify(advert_schema.dump(advert))

@app.route('/adverts', methods=['POST'])
def create_advert():
    data = request.get_json()
    if not data or 'title' not in data or 'description' not in data or 'owner' not in data:
        raise InvalidAPIUsage('Missing required fields', 400)
    
    new_advert = Advert(
        title=data['title'],
        description=data['description'],
        owner=data['owner'],
        created_at=datetime.datetime.now()
    )
    
    db.session.add(new_advert)
    db.session.commit()
    
    return jsonify(advert_schema.dump(new_advert)), 201

@app.route('/adverts/<int:advert_id>', methods=['PUT'])
def update_advert(advert_id):
    advert = Advert.query.get(advert_id)
    if advert is None:
        raise InvalidAPIUsage('Advert not found', 404)
    
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('No data provided', 400)
    
    if 'title' in data:
        advert.title = data['title']
    if 'description' in data:
        advert.description = data['description']
    if 'owner' in data:
        advert.owner = data['owner']
    
    db.session.commit()
    return jsonify(advert_schema.dump(advert))

@app.route('/adverts/<int:advert_id>', methods=['DELETE'])
def delete_advert(advert_id):
    advert = Advert.query.get(advert_id)
    if advert is None:
        raise InvalidAPIUsage('Advert not found', 404)
    
    db.session.delete(advert)
    db.session.commit()
    return '', 204

@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)