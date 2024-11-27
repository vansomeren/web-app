from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create tables at startup
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/register', methods=['POST'])
def register():
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    username = request.form.get('username')
    password = request.form.get('password')
    if username and password:
        new_user = User(firstname=firstname,lastname=lastname,username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/api/users', methods=['GET'])
def api_get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username} for user in users])

if __name__ == '__main__':
    app.run(debug=True)
