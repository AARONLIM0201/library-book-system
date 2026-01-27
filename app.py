from flask import Flask, render_template, session, redirect, url_for, request
from database import init_db
from routes import api
from flask_cors import CORS
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_demo_purposes' # Required for sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app) # Enable CORS for frontend flexibility

init_db(app)
app.register_blueprint(api, url_prefix='/api')


# Authentication Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- AUTH ROUTES ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hardcoded credentials as requested
        if username == 'admin' and password == 'pa$$wOrd':
            session['logged_in'] = True
            session['user'] = username
            return redirect(url_for('index'))
        else:
            error = 'Invalid Credentials. Please try again.'
            
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/books')
@login_required
def books_page():
    return render_template('books.html')

@app.route('/borrowers')
@login_required
def borrowers_page():
    return render_template('borrowers.html')

@app.route('/audit')
@login_required
def audit_page():
    return render_template('audit.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
