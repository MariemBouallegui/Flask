from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/iset'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), unique=True, nullable=False)
    pwd = db.Column(db.String(255), nullable=False)
    nom = db.Column(db.String(255), nullable=False)
    prenom = db.Column(db.String(255), nullable=False)

@app.route('/adduser', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(login=data['login'], pwd=data['pwd'], nom=data['nom'], prenom=data['prenom'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'}), 201

@app.route('/checkuser', methods=['POST'])
def check_user():
    data = request.get_json()
    user = User.query.filter_by(login=data['login'], pwd=data['pwd']).first()
    if user:
        return jsonify({'nom': user.nom, 'prenom': user.prenom}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
