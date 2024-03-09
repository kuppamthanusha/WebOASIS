from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"

# Create database tables within the application context
with app.app_context():
    db.create_all()

# Dummy database for storing user credentials
users = {'user1': 'password1', 'user2': 'password2'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login1')
def login1():
    return render_template('secured.html')

@app.route('/logout1')
def logout1():
    session.pop('username', None)
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('secured'))
        else:
            return render_template('login.html', message='Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            users[username] = password
            return redirect(url_for('login'))
        else:
            return render_template('register.html', message='Username already exists')
    return render_template('register.html')

@app.route('/secured')
def secured():
    if 'username' in session:
        return render_template('secured.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)